import numpy as np
import logging

LOG = logging.getLogger('pipeline_parallel.FakeServer')


class FakeServer(object):
    def __init__(self, rams, times, total_ram, total_cpu):

        self.rams = list(rams)
        self.times = list(times)
        self.total_ram = total_ram
        self.total_cpu = total_cpu

        self.ram_remaining = total_ram
        self.processes = []

    def get_file(self):
        try:
            first_id = np.where(np.array(self.rams) <= self.ram_remaining)[0][0]

            ram = self.rams.pop(first_id)
            time = self.times.pop(first_id)

        except IndexError:
            ram = None
            time = None
        return [time, ram]

    def fill_ram(self):
        while self.ram_remaining > 0. and len(self.processes) < self.total_cpu:
            (time, ram) = self.get_file()

            # If time is not None
            if time:
                self.processes.append([time, ram])
                self.ram_remaining -= ram
            else:
                break

    def end_shortest_sim(self):
        """
        We find the shortest simulation in the list,
        update the total time and delete it from the processes list
        :return:
        :rtype:
        """
        # We sort from lower to higher time
        self.processes.sort()

        (time, ram) = self.processes.pop(0)
        self.ram_remaining += ram

        return time

    def update_process_time(self, p_time):
        # Substract p_time amount of time to all running processes
        for (i, (time, ram)) in enumerate(self.processes):
            self.processes[i] = [time - p_time, ram]

    def predict_parallel_time(self):
        """
        :return: expected total time in h
        :rtype: float
        """

        runtime = 0.

        if np.max(self.rams) > self.total_ram:
            # Can run the pipeline, not enough ram
            return np.NaN

        while len(self.rams) > 0:
            self.fill_ram()
            p_time = self.end_shortest_sim()
            self.update_process_time(p_time)
            runtime += p_time

        # Finally we take the longest simulation remaining
        if self.processes:
            (p_time, ram) = max(self.processes)
            runtime += p_time

        return runtime
