###########################################
#import orders must follow the class model#
###########################################
##############################
# blackdogrequest            #
##############################
from blackdogosint.utils.blackdogrequest.dogrequest import BlackDogRequest

##############################
# utils-data-file import     #
##############################
from blackdogosint.utils.data import useragents
from blackdogosint.utils.data import apikeys
from blackdogosint.utils.data import ipranges
from blackdogosint.utils.data import resolvers

##############################
# utils-main-class           #
##############################
from blackdogosint.utils.to_ast import TOAST
from blackdogosint.utils.blackdogrequest.dogrequest import BlackDogRequest
from blackdogosint.utils.convertall import ConvertAllTo
from blackdogosint.utils.constants import Constants


##############################
#method list                 #
##############################
from blackdogosint.utils.useragents import getall
from blackdogosint.utils.useragents import useragentrandom

##############################
#database                    #
##############################

##############################
#exceptions-class            #
##############################
from blackdogosint.utils.exception.exception import OsintlibException
from blackdogosint.utils.exception.exception import MissingKey
##############################
#exceptions-method           #
##############################

##############################
#parsers-class               #
##############################
from blackdogosint.utils.parsers.intelxparser import Parser
from blackdogosint.utils.parsers.intelxparser import Parser2

##############################
#parsers-method              #
##############################
from blackdogosint.utils.parsers.generic.myparser import is_valid_hostname
from blackdogosint.utils.parsers.generic.myparser import mail_parser
from blackdogosint.utils.parsers.generic.myparser import phone_parser
from blackdogosint.utils.parsers.generic.myparser import localizacao_cep
from blackdogosint.utils.parsers.generic.myparser import cpf

##############################
#proxy                       #
##############################
from blackdogosint.utils.proxy.init_proxy import __LISTPROXYOK
from blackdogosint.utils.proxy.init_proxy import __LISTPROXY
from blackdogosint.utils.proxy.init_proxy import __init_proxy_list
from blackdogosint.utils.proxy.init_proxy import __check_proxy
from blackdogosint.utils.proxy.init_proxy import proxyrandom
#todo:criar um metodo de população da database
