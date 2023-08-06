from typing import Type
import ast
import requests
import json
from blackdogosint.utils.coreosint import ConvertAllTo
from blackdogosint.utils.coreosint import BlackDogRequest


class SearchAnubis():

    def __init__(self, word):
        self.word = word
        self.totalhosts = list
        self.proxy = False

    def do_search(self):
        url = f'https://jldc.me/anubis/subdomains/{self.word}'
        request = BlackDogRequest(url=url, headers='', data='', json=False, proxy=False, timeout=10).fetch_get()
        self.totalhosts = ast.literal_eval(request)
        return ConvertAllTo(self.totalhosts).list_to_dict()

    def get_total_hostnames(self) -> int:
        return len(self.totalhosts)


"""test = SearchAnubis(word='google.com')
print(test.do_search())"""
