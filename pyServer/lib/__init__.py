#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@Author  :  hao
@File    :  __init__.py.py
@Time    :  2020/7/16 下午3:23
'''
import random
import socket
import string
import struct
from urllib.parse import urlparse

import requests

ua = [
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.2 (KHTML, like Gecko) Chrome/4.0.223.3 Safari/532.2',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/4.0.201.1 Safari/532.0',
    'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/3.0.195.27 Safari/532.0',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/530.5 (KHTML, like Gecko) Chrome/2.0.173.1 Safari/530.5',
    'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/8.0.558.0 Safari/534.10',
    'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/540.0 (KHTML,like Gecko) Chrome/9.1.0.0 Safari/540.0',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/9.0.600.0 Safari/534.14',
    'Mozilla/5.0 (X11; U; Windows NT 6; en-US) AppleWebKit/534.12 (KHTML, like Gecko) Chrome/9.0.587.0 Safari/534.12',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.13 (KHTML, like Gecko) Chrome/9.0.597.0 Safari/534.13',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.11 Safari/534.16',
    'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20',
    'Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.792.0 Safari/535.1'
]


def get_headers():
    HEADERS = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'User-Agent': "",
        'Referer': "",
        'X-Forwarded-For': "",
        'X-Real-IP': "",
        'Connection': 'keep-alive',
    }
    referer = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(random.randint(5, 15))])
    referer = 'www.' + referer.lower() + '.com'
    ip = socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))
    HEADERS["User-Agent"] = random.choice(ua)
    HEADERS["Referer"] = referer
    HEADERS["X-Forwarded-For"] = HEADERS["X-Real-IP"] = ip
    return HEADERS


class PocBase:

    def __init__(self, ip, port=None):
        self.host = ip
        self.port = int(port)

    @property
    def url(self):
        return self.host if not self.port else self.analyse_http_https()

    def analyse_http_https(self):
        if self.port == 443:
            return f"https://{self.host}:{self.port}"
        url = f"http://{self.host}:{self.port}"
        try:
            r = requests.get(url, headers=get_headers(), allow_redirects=False, timeout=3)
            if r.headers.get("Location"):
                redirect = r.headers.get("Location")
                domain1 = urlparse(redirect).netloc
                domain2 = urlparse(url).netloc
                http1 = urlparse(redirect).scheme
                http2 = urlparse(url).scheme
                if domain2 in domain1 and http1 != http2:
                    url = str(url).replace(http2, http1).replace(domain2, domain1)

        except:
            url = f"https://{self.host}:{self.port}"

        return url


if __name__ == '__main__':
    aa = PocBase("192.168.101.100", 80)
    print(aa.url)
