"""Magen Client creates a Flask instance in order to perform authorization requests to Magen ID Service"""
from .magen_client_handler import MagenClientAppHandler

__author__ = "michowdh@cisco.com"
__copyright__ = "Copyright(c) 2015, Cisco Systems, Inc."
__version__ = "0.2"
__status__ = "alpha"


class MagenClient(object):
    """
    This is MagenClient to secure services.
    This server provides an authorize handler and a token handler,
    Like many other Flask extensions, there are two usage modes. One is

    binding the Flask app instance::

        app = Flask(__name__)
        oid = MagenClient(app)
    """

    def __init__(self, app=None):
        self.remote_apps = {}
        self.app = app

    def register_client_app(self, name, register=True, **kwargs):
        """
        This function creates the instance of remote connected app

        :param name: This contains the app name
        :param register: This contains the boolean value of the dynamic registration
        :type name: string
        :type register: boolean
        :return: remote object
        :rtype: remote object
        """
        remote = MagenClientAppHandler(name, **kwargs)
        if register:
            assert name not in self.remote_apps
            self.remote_apps[name] = remote
        return remote
