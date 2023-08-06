"""Base Error classes."""
import functools
import io
import logging
# import subprocess
# from asyncio.streams import StreamReader
# from asyncio.subprocess import Process
# from enum import Enum
# from typing import Optional, Union

def aggregate(error_cls):
    class Aggregate(error_cls):
        """Aggregate multiple sub-exceptions."""

        def __init__(self, exceptions: []):
            self.exceptions = exceptions

        def __str__(self):
            return "\n".join(str(e) for e in self.exceptions)

    if error_cls != Exception:
        error_cls.Aggregate = Aggregate

    return error_cls


AggregateError = aggregate(Exception)

class DialectNotSupportedError(Exception):
    def exit_code(self):
        return ExitCode.FAIL