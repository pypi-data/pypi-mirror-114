"""
Copyright 2021 Charles McMarrow
"""


# backrooms
from backrooms.translator import StringHandler

NAME = "vars"

SCRIPT = """"""


def get_handler() -> StringHandler:
    return StringHandler(NAME, SCRIPT)
