#! /usr/bin/python3

import argparse

import os
import sys

from magen_statistics_server.metrics_server import MetricsApp
from magen_statistics_server.source_counter_rest_api import sourced_counters

__author__ = "alifar@cisco.com"
__copyright__ = "Copyright(c) 2015, Cisco Systems, Inc."
__version__ = "0.1"
__status__ = "alpha"
__date__ = "10/24/2016"

METRICS_HOST = '0.0.0.0'
METRICS_PORT = 8002


def signal_handler(signal, frame):
    print("Statistics got signal, terminating")
    sys.exit(0)


def save_pid_to_file():
    """
    We save PID to file. The test harness needs this value in order
    to kill the server.

    :rtype: void
    """
    fd = open("server.PID", "w+")
    fd.write(str(os.getpid()) + "\n")
    fd.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Magen Statistics Server',
                                     usage=("\npython3 statistics_main.py "
                                            "--test"
                                            "\n\nnote:\n"
                                            "root privileges are required "))

    parser.add_argument('--test', action='store_true',
                        help='Run server in test mode. Used for unit tests'
                             'Default is to run in production mode)')

    #: parse CMD arguments ----------------------------------------------------
    args = parser.parse_args()

    save_pid_to_file()

    metrics_app = MetricsApp().metrics
    metrics_app.register_blueprint(sourced_counters)

    if args.test:
        metrics_app.run(host=METRICS_HOST, port=METRICS_PORT, debug=True, use_reloader=False)
    else:
        metrics_app.run(host=METRICS_HOST, port=METRICS_PORT)
