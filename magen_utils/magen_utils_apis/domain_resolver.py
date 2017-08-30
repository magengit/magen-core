#! /usr/bin/python3

import requests
from pathlib import Path

__author__ = "Alena Lifar"
__copyright__ = "Copyright(c) 2015, Cisco Systems, Inc."
__version__ = "0.2.0"
__status__ = "alpha"
__email__ = "alifar@cisco.com"
__date__ = "4/5/2017"

MONGO_PORT = 27017
MONGO_IP = '127.0.0.1'
MONGO_NAME = 'magen_mongo'

LOCAL_MONGO_LOCATOR = "{ip}:{port}".format(ip=MONGO_IP, port=MONGO_PORT)


def parse_resolv(file_path='/etc/resolv.conf'):
    """
    this function looks up a domain name for a service

    :param: file_path: str, by default is /etc/resolv.conf
    :return: domain_name
    :rtype: string
    """
    domain = 'localhost'  # default domain name
    domain_line = None
    try:
        with open(file_path) as f:
            for line in f:
                if line.startswith('search') or line.startswith('domain'):  # looking up domain entry in the file
                    domain_line = line
    except FileNotFoundError as e:
        print(e)
        return domain
    if domain_line:
        for word in domain_line.split():
            if 'magen.' in word:  # if domain name is valid
                domain = word
                return domain
    return domain  # return default domain


def inside_docker():
    docker_env = Path('/.dockerenv')
    return docker_env.is_file()


def mongo_locator():
    mongo_ip, mongo_port = mongo_host_port()
    return '{ip}:{port}'.format(ip=mongo_ip, port=mongo_port)


def mongo_host_port():
    magen_mongo = MONGO_IP if not inside_docker() else MONGO_NAME
    return magen_mongo, MONGO_PORT

