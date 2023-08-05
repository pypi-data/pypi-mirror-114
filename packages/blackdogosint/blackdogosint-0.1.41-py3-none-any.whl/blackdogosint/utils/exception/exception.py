# -*- coding: utf-8 -*-
__all__ = ['OsintlibException','MissingKey']

import sys
import traceback
from typing import Optional


class OsintlibException(Exception):
    """Exception thrown by :func:.

     functions that encounters unrecoverable errors should call the
    :func:`r` function instead of throwing this exception directly.
    """

    def __init__(self, msg, reason=None, exit_code=None):
        """bar."""
        Exception.__init__(self, msg)
        self.reason = reason
        self.exit_code = exit_code
        self.message = msg

    def __repr__(self):
        s = 'OsintlibException: %s' % self.message
        if self.reason:
            s += '\nReason:\n'
            s += ''.join(traceback.format_exception(*self.reason))
        elif sys.exc_info()[0] not in [None, KeyboardInterrupt]:
            s += '\n'
            s += ''.join(traceback.format_exc())
        return s


class MissingKey(Exception):
    """
    :raise: When there is a module that has not been provided its API key
    """

    def __init__(self, source: Optional[str]):
        if source:
            self.message = f'\n\033[93m[!] Missing API key for {source}. \033[0m'
        else:
            self.message = '\n\033[93m[!] Missing CSE id. \033[0m'

    def __str__(self) -> str:
        return self.message
