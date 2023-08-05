# Promote useful stuff to toplevel
from __future__ import absolute_import

from pwn import pwnlib,log
from platform import architecture
from blackdogosint.utils.toplevel import *
pwnlib.args.initialize()
pwnlib.log.install_default_handler()
pwnlib.config.initialize()
args = pwnlib.args.args
if not architecture()[0].startswith('64'):
    """Determines if the current Python interpreter is supported by blackdogosint.
    """
    log.warn_once('blackdogosint does not support 32-bit Python.  Use a 64-bit release.')


"""with context.local(log_console=sys.stderr):
    pwnlib.update.package_name = 'blackdogosint'
    pwnlib.update.package_repo = 'darkcode357/blackdogosint'
    pwnlib.update.update_freq = 10
    pwnlib.update.check_automatically()"""
