"""Magen Logger Configuration"""
import logging
import os
import time


class LogDefaults:
    """Log Default Configurations"""
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
        converted = self.converter(record.created)
        if datefmt:
            time_string = time.strftime(datefmt, converted)
        else:
            formatted_time = time.strftime("%Y-%m-%dT%H:%M:%S", converted)
            time_string = "%s.%03d" % (formatted_time, record.msecs)
        return time_string


def get_log_level(inputt):
    """Get Log Level"""
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
    except PermissionError as error:
        print("No rights to create logging directory: %s. Using default dir: %s" % (error, LogDefaults.default_dir))
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
