import logging
import os
import time


class LogDefaults:
    DEFAULT_LOG_IP_PORT = "localhost:5000"
    default_log_name = "Magen_Logger"
    default_dir = os.getcwd() + "/magen_logs/"
    default_error_file = "magen_error.log"
    default_all_file = "magen_all.log"
    default_console_level = logging.ERROR
    default_format = '%(process)d ' \
                     '%(asctime)12s UTC ' \
                     '%(name)s: ' \
                     '%(module)s.%(funcName)-12s ' \
                     '%(levelname)s: %(message)s'


class MyFormatter(logging.Formatter):
    """ Gives us a dot instead of a comma in the log printout """
    converter = time.gmtime

    def formatTime(self, record, datefmt=None):
        ct = self.converter(record.created)
        if datefmt:
            s = time.strftime(datefmt, ct)
        else:
            t = time.strftime("%Y-%m-%dT%H:%M:%S", ct)
            s = "%s.%03d" % (t, record.msecs)
        return s


def get_log_level(inputt):
    if inputt == 'debug':
        log_level = logging.DEBUG
    elif inputt == 'info':
        log_level = logging.INFO
    elif inputt == 'error':
        log_level = logging.ERROR
    else:
        log_level = LogDefaults.default_console_level
    return log_level


def initialize_logger(console_level="error",
                      output_dir=None,
                      name=None, logger=None):
    """
    :param logger: log object
    :type console_level: int
    :type name: str
    :type output_dir: str
    """

    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

    if not logger:
        logger = logging.getLogger(name)

    try:
        print("Creating custom logging directory is: %s" % output_dir)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    except PermissionError as e:
        print("No rights to create logging directory: %s. Using default dir: %s" % (e, LogDefaults.default_dir))
        if os.access(LogDefaults.default_dir, os.W_OK):
            if not os.path.exists(LogDefaults.default_dir):
                os.makedirs(output_dir)
        else:
            raise

    c_level = get_log_level(console_level)

    # create console handler and set level to info
    handler = logging.StreamHandler()
    handler.setLevel(c_level)
    formatter = MyFormatter(LogDefaults.default_format)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # create error file handler and set level to error
    handler = logging.FileHandler(os.path.join(output_dir, LogDefaults.default_error_file), "w", encoding=None,
                                  delay="true")
    handler.setLevel(logging.ERROR)
    formatter = MyFormatter(LogDefaults.default_format)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # create debug file handler and set level to debug
    handler = logging.FileHandler(os.path.join(output_dir, LogDefaults.default_all_file), "w", encoding=None,
                                  delay="true")
    handler.setLevel(logging.DEBUG)
    formatter = MyFormatter(LogDefaults.default_format)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
