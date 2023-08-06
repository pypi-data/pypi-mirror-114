import colored_traceback
from pprint import pprint
from blackdogosint.utils import exception


#################
#osintlib-import#
#################
from blackdogosint.utils.coreosint import *
from pwn import getLogger
log = getLogger("blackdogosint")
error   = log.error
warning = log.warning
warn    = log.warning
info    = log.info
debug   = log.debug
success = log.success
colored_traceback.add_hook()