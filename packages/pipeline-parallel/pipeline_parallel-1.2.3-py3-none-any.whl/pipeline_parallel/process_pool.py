import sys
import psutil
import multiprocessing
import logging
import time
import resource
from functools import wraps
import pickle
import os

from . import utils
from . import arg_list

LOG = logging.getLogger('pipeline_parallel.ProcessPool')


class ProcessPool(object):
    """
    Manage processes given a total number of RAM and CPU allowed

    Print Pool info in LOG_FILE, you can print update on screen with:
    > watch cat pool.log
    """

    RAM_SAFETY = 0.3  # ratio of total RAM kept as security (we don't want to use all the RAM, just in case)
    LOG_FILE = "pool.log"
    UPDATE_FREQUENCY = 2  # [s] Time between two update in the main loop
    DEFAULT_DELAY = 2  # [s] Time between 2 consecutive process start (to avoid saturating disks)
    RESTART_FILENAME = "pool.restart"

    def __init__(self, func, params, cpu=None, ram=None, delay=None):
        """

        :param func: Function to be launched in parallel
        :type func: Python function
        :param ArgList params: list of parameters for each process to launch. This parameter is ignored if a non
                               finished pool is detected
        :param int cpu: Number of CPU allowed (by default, all but one of them)
        :param float ram: RAM allowed [GB] (by default total minus a RAM_SAFETY value
        :param float delay: [optional] Number of seconds (by default, 2s delay) between to consecutive process launches.
                            A non-zero value prevent freeze due to all processes initializing at once
        """

        self.done = []  # List of first argument for each process that worked
        self.failed = []  # List of tuple (args, ram) for each failed process
        self.tstart = None
        self.tstop = None
        self.processes = []
        self.p_instant_ram = {}  # Key is process name (p.name)
        self.task_completed = {}  # Key is filename

        # Add a decorator to retrieve total time and memory consumption for stats
        self.func = self.profile(func)

        # Try to restart an existing pool
        if os.path.isfile(self.RESTART_FILENAME):
            # This function will fail if the function defined in the previous pool is different than the one actually
            # used
            self.params = self.__read_restart_file()
            LOG.info("Continue previous pool instead of input parameter")
        else:
            self.params = params

        # We keep one CPU available as safety. 
        cpu_count = psutil.cpu_count() - 1
        if cpu:
            self.max_cpu = cpu
        else:
            self.max_cpu = cpu_count

        if self.max_cpu > cpu_count:
            LOG.exception(
                "Pool asked to use more CPU than physically available ({} > {})".format(self.max_cpu, cpu_count))
            raise ValueError("Pool asked to use more CPU than physically available.")

        mem = psutil.virtual_memory()
        ram_count = mem.total / 1024 ** 3
        if ram:
            self.max_ram = ram
        else:
            self.max_ram = ram_count * (1 - self.RAM_SAFETY)

        LOG.debug("Pool running with {} CPUs and {:.1f} GB".format(self.max_cpu, self.max_ram))

        if self.max_ram > ram_count:
            LOG.exception("Pool asked to use more RAM than physically available ({:.1f} > {:.1f})".format(self.max_ram,
                                                                                                          ram_count))
            raise ValueError("Pool asked to use more RAM than physically available.")

        if any(ram > self.max_ram for ram in self.params.weight):
            LOG.exception("Task asked to use more ram than allocated to ProcessPool ({:.1f} > {:.1f} GB)".format(
                max(self.params.weight), self.max_ram))
            raise ValueError("Task asked to use more ram than allocated to ProcessPool ({:.1f} > {:.1f} GB)".format(
                max(self.params.weight), self.max_ram))

        self.delay = self.DEFAULT_DELAY  # [s]
        if delay is not None:
            if delay < 0:
                raise ValueError("delay must be a positive float (number of seconds). You used {}".format(delay))
            self.delay = delay

        self.ram_remaining = self.max_ram
        self.queue = multiprocessing.Queue()

    def __add_process(self, arg: tuple, ram: float):
        """
        :param arg: args for that function
        :type arg: tuple
        :param ram: RAM expected to be used by that process
        :type ram: float

        :return:
        :rtype:
        """

        # We add the queue in front, for the decorator self.profile()
        tmp_argv = (self.queue,) + arg

        process = multiprocessing.Process(target=self.func, args=tmp_argv)

        process.start()
        self.processes.append((process, ram, arg))
        self.ram_remaining -= ram
        self.p_instant_ram[process.name] = utils.get_process_ram(process)

        LOG.debug(
            "Launch func={} ({}) for {:.1f} GB. args={}".format(self.func.__name__, process.name, ram, arg))

    def __update_status(self):
        """
        Clean process list if some finished

        :return:
        :rtype:
        """

        for (i, (p, ram, arg)) in enumerate(self.processes):
            if not p.is_alive():
                # add newly freed RAM, and delete old process

                self.ram_remaining += ram

                # We assume 1st argument is the filename
                if p.exitcode is 0:
                    self.done.append(arg[0])

                    (filename, runtime, memory_use) = self.queue.get()
                    self.task_completed[filename] = [runtime, memory_use]

                else:
                    self.failed.append((arg, ram))

                    # Add arguments to list of files scheduled for restart

                self.processes.pop(i)

                # Update restart file only if one process died (failure or completion)
                self.__write_restart_file()
            else:
                self.p_instant_ram[p.name] = utils.get_process_ram(p)

        return 0

    def __write_restart_file(self):
        """
        Write a restart file to continue the pool in case of a problem
        """

        old_file = f"{self.RESTART_FILENAME}.bak"

        # Existing version is moved to a backup version in case something goes wrong when writing this one
        if os.path.isfile(self.RESTART_FILENAME):
            os.rename(self.RESTART_FILENAME, old_file)

        args = []
        rams = []

        # Waiting list
        args.extend(self.params.args)
        rams.extend(self.params.weight)

        # Failed files
        if self.failed:
            tmp_args, tmp_ram = map(list, zip(*self.failed))

            args.extend(tmp_args)
            rams.extend(tmp_ram)

        # Running files
        if self.processes:
            dummy, tmp_ram, tmp_args = map(list, zip(*self.processes))

            args.extend(tmp_args)
            rams.extend(tmp_ram)

        # Only write the file if the number of potential restart is non-zero
        if len(args) > 0:
            with open(self.RESTART_FILENAME, 'wb') as obj:
                pickle.dump((self.func.__name__, args, rams), obj, protocol=pickle.HIGHEST_PROTOCOL)

            # Try to delete backup file if it exists
            if os.path.isfile(old_file):
                os.remove(old_file)

    def __read_restart_file(self):
        """
        Read a restart file and replace existing data with new one

        Note that this only works if all arguments are strings (no int, float or anything else), and without spaces
        especially for filenames

        :return: ArgList object containing all files that need to be restarted
        :rtype: arg_list.ArgList
        """

        # If pool is running/finished, we prevent the user to change parameters. He needs to create a brand new object
        if self.tstart is not None:
            LOG.error("Pool is running, cannot overwrite parameter list.")
            return 1

        with open(self.RESTART_FILENAME, "rb") as f:
            func_name, args, rams = pickle.load(f)

        if func_name != self.func.__name__:
            raise ValueError(f"Trying to use a restart.pool whose function '{func_name}' was different than "
                             f"the one currently declared in this pool ('{self.func.__name__}').")

        # Replace Pool parameters with new one:
        params = arg_list.ArgList(args=args, ram=rams)

        return params

    def __update_log(self):
        """
        Store Pool status in a log file LOG_FILE (processes finished, running and pending)
        """

        msg = ""
        msg += "Function: {}\n".format(self.func.__name__)

        if self.is_running():
            msg += "Pool Usage: RAM {:.1f}/{:.1f} GB ; CPUs {} / {}\n".format(self.max_ram - self.ram_remaining,
                                                                              self.max_ram,
                                                                              len(self.processes), self.max_cpu)

            ttime = time.time() - self.tstart
            completion = 100. * (
                        len(self.failed) + len(self.task_completed.keys())) / self.params.initial_size  # percentage
            eta = ttime * (100. / completion - 1) if completion != 0 else None  # Estimated remaning time in s
            msg += "Ellapsed time: {} ; Completion: {:.1f} % ; ETA {}\n".format(utils.strtime(ttime), completion,
                                                                                utils.strtime(eta))

            msg += "Process running: {}\n".format(len(self.processes))
            for (p, ram, arg) in self.processes:
                msg += "\t{} ({} ; {:.1f} / {:.1f} GB): {}\n".format(p.name, p.pid, self.p_instant_ram[p.name], ram,
                                                                     arg)

            msg += "Tasks waiting {}/{}\n".format(len(self.params.args), self.params.initial_size)
        else:
            msg += "Pool ressources: {} CPUs and {:.1f} GB of RAM\n".format(self.max_cpu, self.max_ram)
            ttime = self.tstop - self.tstart
            msg += "Total time: {}\n".format(utils.strtime(ttime))

        msg += "Files completed {}/{}:\n".format(len(self.task_completed.keys()), self.params.initial_size)
        for (filename, values) in self.task_completed.items():
            msg += "\t {} in {:.1f} s ({:.2f} GB)\n".format(filename, *values)

        msg += "Files failed {}/{}:\n".format(len(self.failed), self.params.initial_size)
        for args, ram in self.failed:
            msg += "\t {}\n".format(args[0])

        obj_file = open(self.LOG_FILE, 'w')
        obj_file.write(msg)
        obj_file.close()

        return msg

    def __fill_space(self):
        """
        Fill RAM/CPU with the remaining tasks to launch
        """

        while self.ram_remaining > 0. and len(self.processes) < self.max_cpu:
            (argv, ram) = self.params.get_next_item(max_weight=self.ram_remaining)

            if argv != "":
                # Create a one element tuple if there's not several arguments
                tmp_argv = argv if type(argv) is tuple else (argv,)

                self.__add_process(arg=tmp_argv, ram=ram)

                time.sleep(self.delay)

            else:
                # No more files to launch
                break

        return 0

    def is_running(self):
        """
        Return True if any Processes are still running, False if the Pool is finished

        Update self.tstop when it first find that Pool ended.
        """

        if self.tstart is None:
            running = False

        elif len(self.processes) != 0:
            running = True

        elif self.params.size != 0:
            running = True

        else:
            running = False
            self.tstop = time.time()

        return running

    @staticmethod
    def profile(f):
        @wraps(f)  # Keep function name and doc as if the decorator did not exist
        def wrapper(*args, **kwargs):
            """
            Add Total execution time in s and
            memory use in GB to the return of the function.

            First argument is a queue that has been artificially added to the function arguments

            Original:
            res = f(param)

            Modified:
            (res, total_time, memory_use) = f(param)
            """

            # The queue is added artificially and deleted here for the real function call
            q = args[0]
            args = args[1:]

            start = time.time()
            res = f(*args, **kwargs)
            tot_time = time.time() - start
            memory_use = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024. ** 2

            # args[0] is expected to be the filename of the fits file when alone
            key = str(args[0]) if len(args) == 1 else str(args)

            LOG.info("Runtime: {:.2f} s ({:.2f} GB) ; Pipeline: {} ; args: {}".format(
                tot_time, memory_use, f.__name__, key))

            q.put([key, tot_time, memory_use])

            return res

        return wrapper

    def run(self):
        """
        Launch the ProcessPool until no files left

        Main method that handle process creation, log file and everything

        :return: 0 if everything went well.
                 1 if some files failed
        :rtype:
        """

        running = True
        self.tstart = time.time()
        while running:
            self.__update_status()
            self.__fill_space()

            # Update log file
            self.__update_log()

            # Wait to avoid looping furiously without giving to processes time to complete
            time.sleep(self.UPDATE_FREQUENCY)

            running = self.is_running()

        # Init log and restart file
        self.__update_log()
        self.__write_restart_file()

        if len(self.failed) != 0:
            sys.exit(os.EX_SOFTWARE)

        return 0
