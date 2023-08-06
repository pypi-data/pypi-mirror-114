import os


class BaseConfig(object):
    SECRET_KEY = os.environ.get("SECRET_KEY", "SUPERSECRETKEYIFYOUKNOWWHATIMEAN")