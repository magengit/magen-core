import datetime
import sys
import importlib.util

from flask import Flask
from flask_cors import CORS
from flask.json import JSONEncoder


class CustomJSONEncoder(JSONEncoder):
        def default(self, obj):
            try:
                if isinstance(obj, datetime.datetime):
                    # print(str(obj))
                    return str(obj)
                iterable = iter(obj)
            except TypeError:
                pass
            else:
                return list(iterable)
            return JSONEncoder.default(self, obj)


class MagenApp(object):
    __instance = None

    def __init__(self, template_path):
        self.__magen = Flask(__name__, template_folder=template_path)
        self.__magen.json_encoder = CustomJSONEncoder
        CORS(self.__magen)

    @classmethod
    def get_instance(cls, template_path='templates'):
        if cls.__instance is None:
            cls.__instance = cls(template_path)
        return cls.__instance

    def app_source_version(main_fname, dir="dev", file="magen_env"):
        """
        Is this main file being run from a workspace?

        :param main_fname: __fname__ for service main file
        :param dir: directory containing workspace-only (not installed) file
        :param file: workspace-only (not installed) file
        :type main_fname: __fname__ string
        :type dir: string
        :type file: string
        :return: true if running from workspace
        :rtype: bool

        Expectations:
        - this method is called only from <svc>_server.py files
        - sys.path[0] is current directory

        Tests:
        - is this file being run directly (name is __main__)?
        - if so, is file being run from workspace vs installed (e.g. /usr/local/bin?)

        Implementation is to check for presence of a file (dev/magen_env.py by default) that is in the workspace but is not installed.
        """
        if main_fname != "__main__":
            return False
        path_save = sys.path
        sys.path = [sys.path[0] + "/" + dir]
        src_ver = importlib.util.find_spec(file)
        sys.path = path_save
        return src_ver

    @property
    def magen(self):
        return self.__magen

    @magen.setter
    def magen(self, value):
        pass
