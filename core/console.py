""" Logging and console interface with autocomplete by tab """

import sys
import datetime
from multiprocessing import Process
from multiprocessing import Queue
import rlcompleter  # this does python autocomplete by tab

try:
    import readline
except ModuleNotFoundError:  # windows support
    import pyreadline as readline

from core.config import cfg


class Console:
    alive = True
    user_input_queue = Queue()
    user_input_process = None

    @classmethod
    def user_input_loop(cls):
        readline.parse_and_bind("tab: complete")
        while True:
            try:
                input_cmd = input('>')
                cls.user_input_queue.put(input_cmd)
            except EOFError:
                break

    @classmethod
    def terminate(cls):
        """ Set cls.alive flag to False, that should trigger the program termination from __main__ """
        cls.alive = False
        cls.user_input_process.terminate()
        cls.user_input_process.join()

    @classmethod
    def init(cls):
        """
        Init console interface.
        After running this function all application output should be handled via Log.
        """

        # Init user console
        cls.user_input_process = Process(target=cls.user_input_loop, name="user_input")
        cls.user_input_process.daemon = True
        cls.user_input_process.start()


class Log:

    LogLevelToInt = {
        'CHAT': 0,
        'DEBUG': 1,
        'COMMANDS': 2,
        'INFO': 3,
        'ERRORS': 4,
        'NOTHING': 5
    }

    file = open(datetime.datetime.now().strftime("logs/log_%Y-%m-%d-%H:%M"), 'w')
    loglevel = LogLevelToInt[cfg.LOG_LEVEL]

    @staticmethod
    def display(string):
        """ Print the string without messing the user input buffer """

        # Have to do this encoding/decoding bullshit because python fails to encode some symbols by default
        string = string.encode(sys.stdout.encoding, 'ignore').decode(sys.stdout.encoding)

        # Save user input line, print string and then user input line
        line_buffer = readline.get_line_buffer()
        sys.stdout.write("\r\n\033[F\033[K" + string + '\r\n>' + line_buffer)

    @classmethod
    def log(cls, data, log_level):
        """ Perform formatting, run cls.display() and write to file """

        # some characters may break the application, so re-encoding is needed
        string = str(data).encode(sys.stdout.encoding, 'ignore').decode(sys.stdout.encoding)

        string = "{}|{}> {}".format(
            datetime.datetime.now().strftime("%d.%m.%Y (%H:%M:%S)"),
            log_level,
            string)
        cls.display(string)
        cls.file.write(string + '\r\n')

    @classmethod
    def close(cls):
        cls.file.close()

    @classmethod
    def chat(cls, data):
        if cls.loglevel <= 0:
            cls.log(data, 'CHAT')

    @classmethod
    def debug(cls, data):
        if cls.loglevel == 1:
            cls.log(data, 'DEBUG')

    @classmethod
    def command(cls, data):
        if cls.loglevel <= 2:
            cls.log(data, 'COMMANDS')

    @classmethod
    def info(cls, data):
        if cls.loglevel <= 3:
            cls.log(data, 'INFO')

    @classmethod
    def error(cls, data):
        if cls.loglevel <= 4:
            cls.log(data, 'ERROR')
