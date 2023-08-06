"""
Module to intercept outputs.

Using this module you can check what your functions prints to screen.
"""
from __future__ import annotations
import contextlib
import sys
from typing import List


class OutputLogger(object):
    """ Class to log every output to console from your methods.

    You use it through a context manager. While inside context manager scope
    console output is stored at OutputLogger. You can print a logger instance to get
    its stored output and you can get it too through its output property.

    When context manager scope ends, then sys.stdout is restored to work back as usual again.

    :Example:

    with OutputLogger.get_logger() as logger:
        print("Hello world")
        print("Bye")
        assert "Hello world" in logger.output
        assert logger.output == ["Hello world", "Bye"]
    """

    def __init__(self):
        self._stdout = sys.stdout
        self._logged_output = []

    def write(self, text):
        if text != "\n":
            self._logged_output.append(text)

    def __repr__(self):
        return "OutputLogger()"

    def __str__(self):
        return self.output

    @property
    def output(self) -> List[str]:
        """ Stored output so far.

        Each output entry is an element of returned list.
        """
        return self._logged_output

    @staticmethod
    @contextlib.contextmanager
    def get_logger() -> OutputLogger:
        """ Context manager to get a listening instance of OutputLogger.

        When context manager scope ends sys.stdout is restored and output works
        back as usual.
        """
        logger = OutputLogger()
        sys.stdout = logger
        yield logger
        sys.stdout = logger._stdout

