from theHarvester.lib.core import *
from theHarvester.parsers import myparser


class SearchBaidu:

    def __init__(self, word, limit):
        self.word = word
        self.total_results = ""
        self.server = 'www.baidu.com'
        self.hostname = 'www.baidu.com'
        self.limit = limit
        self.proxy = False

    async def do_search(self):
        headers = {
            'Host': self.hostname,
            'User-agent': Core.get_user_agent()
        }
        base_url = f'https://{self.server}/s?wd=%40{self.word}&pnxx&oq={self.word}'
        urls = [base_url.replace("xx", str(num)) for num in range(0, self.limit, 10) if num <= self.limit]
        responses = await AsyncFetcher.fetch_all(urls, headers=headers, proxy=self.proxy)
        for response in responses:
            self.total_results += response

    async def process(self, proxy=False):
        self.proxy = proxy
        await self.do_search()

    async def get_emails(self):
        rawres = myparser.Parser(self.total_results, self.word)
        return await rawres.emails()

    async def get_hostnames(self):
        rawres = myparser.Parser(self.total_results, self.word)
        return await rawres.hostnames()


#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Charles on 2018/10/10
# Function:

import sys
import requests
from bs4 import BeautifulSoup


ABSTRACT_MAX_LENGTH = 300    # abstract max length

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'
    ' Ubuntu Chromium/49.0.2623.108 Chrome/49.0.2623.108 Safari/537.36',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; pt-BR) AppleWebKit/533.3 '
    '(KHTML, like Gecko)  QtWeb Internet Browser/3.7 http://www.QtWeb.net',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/41.0.2228.0 Safari/537.36',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.2 (KHTML, '
    'like Gecko) ChromePlus/4.0.222.3 Chrome/4.0.222.3 Safari/532.2',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.4pre) '
    'Gecko/20070404 K-Ninja/2.1.3',
    'Mozilla/5.0 (Future Star Technologies Corp.; Star-Blade OS; x86_64; U; '
    'en-US) iNet Browser 4.7',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.13) '
    'Gecko/20080414 Firefox/2.0.0.13 Pogo/2.0.0.13.6866'
]

# 请求头信息
HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    "Referer": "https://www.baidu.com/",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9"
}

baidu_host_url = "https://www.baidu.com"
baidu_search_url = "https://www.baidu.com/s?ie=utf-8&tn=baidu&wd="

session = requests.Session()
session.headers = HEADERS


def search(keyword, num_results=10, debug=0):
    """
    通过关键字进行搜索
    :param keyword: 关键字
    :param num_results： 指定返回的结果个数
    :return: 结果列表
    """
    if not keyword:
        return None

    list_result = []
    page = 1

    # 起始搜索的url
    next_url = baidu_search_url + keyword

    # 循环遍历每一页的搜索结果，并返回下一页的url
    while len(list_result) < num_results:
        data, next_url = parse_html(next_url, rank_start=len(list_result))
        if data:
            list_result += data
            if debug:
                print("---searching[{}], finish parsing page {}, results number={}: ".format(keyword, page, len(data)))
                for d in data:
                    print(str(d))

        if not next_url:
            if debug:
                print(u"already search the last page。")
            break
        page += 1

    if debug:
        print("\n---search [{}] finished. total results number={}！".format(keyword, len(list_result)))
    return list_result[: num_results] if len(list_result) > num_results else list_result


def parse_html(url, rank_start=0, debug=0):    # sourcery no-metrics
    """
    解析处理结果
    :param url: 需要抓取的 url
    :return:  结果列表，下一页的url
    """
    try:
        res = session.get(url=url)
        res.encoding = "utf-8"
        root = BeautifulSoup(res.text, "lxml")

        list_data = []
        div_contents = root.find("div", id="content_left")
        for div in div_contents.contents:
            if type(div) != type(div_contents):
                continue

            class_list = div.get("class", [])
            if not class_list:
                continue

            if "c-container" not in class_list:
                continue

            title = ''
            url = ''
            abstract = ''
            try:
                # 遍历所有找到的结果，取得标题和概要内容（50字以内）
                if "xpath-log" in class_list:
                    if div.h3:
                        title = div.h3.text.strip()
                        url = div.h3.a['href'].strip()
                    else:
                        title = div.text.strip().split("\n", 1)[0]
                        if div.a:
                            url = div.a['href'].strip()

                    if div.find("div", class_="c-abstract"):
                        abstract = div.find("div", class_="c-abstract").text.strip()
                    elif div.div:
                        abstract = div.div.text.strip()
                    else:
                        abstract = div.text.strip().split("\n", 1)[1].strip()
                elif "result-op" in class_list:
                    if div.h3:
                        title = div.h3.text.strip()
                        url = div.h3.a['href'].strip()
                    else:
                        title = div.text.strip().split("\n", 1)[0]
                        url = div.a['href'].strip()
                    if div.find("div", class_="c-abstract"):
                        abstract = div.find("div", class_="c-abstract").text.strip()
                    elif div.div:
                        abstract = div.div.text.strip()
                    else:
                        # abstract = div.text.strip()
                        abstract = div.text.strip().split("\n", 1)[1].strip()
                elif (
                    div.get("tpl", "") != "se_com_default"
                    and div.get("tpl", "") == "se_st_com_abstract"
                    and len(div.contents) >= 1
                ):
                    title = div.h3.text.strip()
                    if div.find("div", class_="c-abstract"):
                        abstract = div.find("div", class_="c-abstract").text.strip()
                    elif div.div:
                        abstract = div.div.text.strip()
                    else:
                        abstract = div.text.strip()
                elif (
                    div.get("tpl", "") == "se_com_default"
                    or div.get("tpl", "") != "se_st_com_abstract"
                    or len(div.contents) >= 1
                ) and (
                    div.get("tpl", "") == "se_com_default"
                    or div.get("tpl", "") == "se_st_com_abstract"
                    or len(div.contents) >= 2
                ):
                    title = div.h3.text.strip() if div.h3 else div.contents[0].text.strip()
                    url = div.h3.a['href'].strip()
                    # abstract = div.contents[-1].text
                    if div.find("div", class_="c-abstract"):
                        abstract = div.find("div", class_="c-abstract").text.strip()
                    elif div.div:
                        abstract = div.div.text.strip()
                    else:
                        abstract = div.text.strip()
            except Exception as e:
                if debug:
                    print("catch exception duration parsing page html, e={}".format(e))
                continue

            if ABSTRACT_MAX_LENGTH and len(abstract) > ABSTRACT_MAX_LENGTH:
                abstract = abstract[:ABSTRACT_MAX_LENGTH]

            rank_start+=1
            list_data.append({"title": title, "abstract": abstract, "url": url, "rank": rank_start})


        next_btn = root.find_all("a", class_="n")

        if len(next_btn) <= 0 or u"上一页" in next_btn[-1].text:
            return list_data, None

        next_url = baidu_host_url + next_btn[-1]["href"]
        return list_data, next_url
    except Exception as e:
        if debug:
            print(u"catch exception duration parsing page html, e：{}".format(e))
        return None, None


