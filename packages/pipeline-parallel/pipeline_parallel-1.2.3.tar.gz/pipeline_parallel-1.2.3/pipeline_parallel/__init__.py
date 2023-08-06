import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())

__version__ = "1.2.3"

from .process_pool import ProcessPool
from .arg_list import ArgList
from .utils import init_log, force_single_thread, generate_example_script
