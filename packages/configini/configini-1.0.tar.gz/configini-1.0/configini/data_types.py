from typing import Optional, Union
from .casting import fetch
import decimal
import configparser
import os

__config = configparser.ConfigParser()


def read(filename):
    __config.read(filename)


def fetch(chapter: str, key: str, default=None):
    return os.environ.get(f"{chapter.upper()}_{key.upper()}") or \
            __config[chapter][key] or \
            default


def String(*args, **kwargs):
    return DataType()


class Integer(DataType):
    data_type = int


class Decimal(DataType):
    data_type = decimal.Decimal


class List(DataType):
    data_type = list


class Boolean(DataType):
    data_type = bool
