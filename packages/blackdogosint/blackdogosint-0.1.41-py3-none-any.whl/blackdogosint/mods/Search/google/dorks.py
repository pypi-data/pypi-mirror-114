# -*- coding: utf-8 -*-
import json
import time

from googlesearch import search


class Dorks:
    def __init__(self, dork, tld, lang, num, start, stop, pause):
        """
        :param dork:
        :param tld:
        :param lang:
        :param num:
        :param start:
        :param stop:
        :param pause:
        """
        self.dork = dork
        self.tld = tld
        self.lang = lang
        self.num = num
        self.start = start
        self.stop = stop
        self.pause = pause

    def search_list(self):
        counter = 0
        requ = 0
        retorno = []
        for results in search(self.dork, self.tld, self.lang, self.num, self.start, self.stop, self.pause):
            counter += 1
            time.sleep(0.1)
            requ += 1
            if requ >= int(self.num):
                break

            data = (counter, results)
            retorno.append(results)
        return retorno

    def search_json(self):
        return [{'url': i} for i in self.search_list()]

    def search(self):
        counter = 0
        requ = 0
        for results in search(self.dork, self.tld, self.lang, self.num, self.start, self.stop, self.pause):
            counter += 1
            time.sleep(0.1)
            requ += 1
            if requ >= int(self.num):
                break

            data = (counter, results)
        return results


#a = Dorks(dork='site:elera.com +filetype:pdf', tld='com', lang='en', num=30, start=0, stop=2, pause=2).search()
# print(a)
