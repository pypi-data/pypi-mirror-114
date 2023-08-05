import configparser
import os

__config = configparser.ConfigParser()


def read(filename):
    __config.read(filename)


def fetch(chapter: str, key: str, default=None):
    return os.environ.get(f"{chapter.upper()}_{key.upper()}") or \
            __config[chapter][key] or \
            default
