# coding=utf-8
import ssl
import urllib.error
import certifi
import requests
from typing import Set, Union, Any, Tuple, List
from requests import Request, Session
import yaml
import asyncio
import aiohttp
import random
import ssl
import certifi
import http
import socket
import re
from bs4 import BeautifulSoup
# blackdog import
from blackdogosint.utils.useragents import useragentrandom
from blackdogosint.utils.proxy.init_proxy import proxyrandom


class BlackDogRequest:

    def __init__(self, url: str, headers: str = '', data: str = '', json: bool = False,
                 proxy: bool = False, timeout: int = 10):

        """
        :param url: url do site que vai ser feito a request
        :param headers: cabeça adicional
        :param data: para solicitação post
        :param json: retorno em forma de json
        :param proxy: proxy para request
        :param timeout: tempo para request
        """
        self.url = url
        self.headers = headers
        self.data = data
        self.json = json
        self.proxy = proxy
        self.timeout = timeout

    def __is_website_online(self):
        """ This function checks to see if a host name has a DNS entry by checking
            for socket info. If the website gets something in return,
            we know it's available to DNS.
        """
        try:
            socket.gethostbyname(self.url)
        except socket.gaierror:
            return False
        else:
            return True

    def __is_page_available(self, path="/"):
        """ This function retreives the status code of a website by requesting
            HEAD data from the host. This means that it only requests the headers.
            If the host cannot be reached or something else goes wrong, it returns
            False.
        """
        try:
            conn = http.HTTPStatus.HTTPConnection(self.url)
            conn.request("HEAD", path)
            if re.match("^[23]\d\d$", str(conn.getresponse().status)):
                return True
        except Exception:
            return None

    def __test_request_post(self):
        """metodo interno para validar a requesição"""
        a = requests.post(self.url)
        return a.text

    def __test_request_get(self):
        """metodo interno para validar a requesição"""
        a = requests.get(self.url)
        return a.text

    def __find_link(self):
        """
        :param url:str
        :return: list of links
        """
        list_links = []
        soup = BeautifulSoup(self.url, "html.parser")
        for link in soup.findAll('a'):
            links = link.get('href')
            print(links)
            list_links.append(links)

    def __check(self):
        if self.__is_website_online():
            self.__is_page_available()
        else:
            return 'site down'


    def fetch_get(self):
        """
        metodo post para requisição
        """
        if not self.__check():
            return 'stop request site is donw'
        if len(self.headers) == 0:
            self.headers = {'User-Agent': useragentrandom()}
            print(self.headers)
        # by default timeout is 5 minutes, changed to 12 minutes for suip module
        # results are well worth the wait
        try:
            if self.proxy:
                try:
                    with Session() as session:
                        # either like this

                        session.proxies = {'https': f'https://{next(proxyrandom())}'}
                            # or like this
                        rquest = session.get(self.url)
                        return rquest.text if self.json is False else session.json()
                except Exception:
                    with Session() as session:
                        # either like this

                        session.proxies = {'https': f'https://{next(proxyrandom())}'}
                        # or like this
                        rquest = session.get(self.url)
                        return rquest.text if self.json is False else session.json()

            else:
                with Session() as session:
                    rquest = session.get(self.url)
                    return rquest.text if self.json is False else session.json()
        except Exception as e:
            print(f'An exception has occurred: {e}')
            return ''

    def fetch_post(self):
        """
        metodo post para requisição
        """
        if len(self.headers) == 0:
            self.headers = {'User-Agent': useragentrandom()}
            print(self.headers)
        # by default timeout is 5 minutes, changed to 12 minutes for suip module
        # results are well worth the wait
        try:
            if self.proxy:
                try:
                    with Session() as session:
                    # either like this

                        session.proxies = {'https': f'https://{next(proxyrandom())}'}
                            # or like this
                        rquest = session.get(self.url)
                        return rquest.text if self.json is False else session.json()
                except Exception:
                    with Session() as session:
                        # either like this

                        session.proxies = {'https': f'https://{next(proxyrandom())}'}
                        # or like this
                        rquest = session.get(self.url)
                        return rquest.text if self.json is False else session.json()

            else:
                with Session() as session:
                    rquest = session.get(self.url)
                    return rquest.text if self.json is False else session.json()
        except Exception as e:
            print(f'An exception has occurred: {e}')
            return ''

