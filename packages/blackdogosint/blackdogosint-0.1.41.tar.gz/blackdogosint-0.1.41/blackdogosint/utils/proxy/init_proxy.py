from blackdogosint.utils.database.db import session_factory
from blackdogosint.utils.database.tabelas.proxy import ProxyTable
import random as randommod
from Proxy_List_Scrapper import Scrapper, Proxy, ScrapperException
import sys
import urllib.request, socket
from threading import Thread

__LISTPROXY = []
__LISTPROXYOK = []


def __init_proxy_list():
    scrapper = Scrapper(category='PROXYLIST_DOWNLOAD_HTTPS', print_err_trace=False)
    data = scrapper.getProxies()
    for item in data.proxies:
        __LISTPROXY.append('{}:{}'.format(item.ip, item.port))


def __check_proxy():
    socket.setdefaulttimeout(3)
    __init_proxy_list()
    print(__LISTPROXY)
    meuip="127.0.0.1"
    for proxy in __LISTPROXY:
        proxy_handler = urllib.request.ProxyHandler({'https': proxy})
        opener = urllib.request.build_opener(proxy_handler)
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)
        try:
            sock = urllib.request.urlopen('https://www.icanhazip.com')  # change the url address here
            #todo
            if sock == meuip:
                continue
            print(f'proxy =>{proxy.read()}\nip => {sock.read()}\n')
            __LISTPROXYOK.append(proxy.read())
        except Exception:
            pass


def proxyrandom():
    __check_proxy()
    """random() -> str
         Get a random user agent string.
            Arguments:
                None
            Returns:
                A random user agent string selected from :func:`getall`.
            >>> import random as randommod
            >>> randommod.seed(1)
            >>> random() # doctest: +SKIP
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; FunWebProducts; FunWebProducts-MyTotalSearch; iebar)'
    """

    return iter(__LISTPROXYOK)

