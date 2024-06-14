import random
import requests
from requests.exceptions import RequestException
import time


class SpiderRetry:
    def __init__(self):
        self.max_retries = 5
        self.sleep_time = 1

    def request(self, url: str, **kwargs):
        retries = 0
        sleep_time = kwargs.pop('sleep', self.sleep_time)
        max_retries = kwargs.pop('max_retries', self.sleep_time)
        while retries < max_retries:
            try:
                response = requests.get(url, **kwargs)
                response.raise_for_status()
                return response
            except RequestException as e:
                print(f"请求失败：{e}， 正在重试({retries + 1}/{max_retries})")
                retries += 1
                time.sleep(sleep_time)
            raise Exception(f"请求失败，已重试{max_retriess}次")


class assemble_headers:
    def __init__(self, **kwargs):
        self.random_headers = False
        self.Headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0',
            "Referer": "https://www.bilibili.com",
        }
        self.config = kwargs

    def get_headers(self):
        random_headers = self.config.pop('random_headers', self.random_headers)
        if not random_headers:
            return self.Headers
        head_user_agent = ['Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
                           'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 '
                           'Safari/537.36',
                           'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR '
                           '3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; rv:11.0) like Gecko)',
                           'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1',
                           'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3',
                           'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12',
                           'Opera/9.27 (Windows NT 5.2; U; zh-cn)',
                           'Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0',
                           'Opera/8.0 (Macintosh; PPC Mac OS X; U; en)',
                           'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.12) Gecko/20080219 '
                           'Firefox/2.0.0.12'
                           'Navigator/9.0.0.6',
                           'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0)',
                           'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)',
                           'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR '
                           '2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; '
                           '.NET4.0C;'
                           '.NET4.0E)',
                           'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) '
                           'Maxthon/4.0.6.2000'
                           'Chrome/26.0.1410.43 Safari/537.1 ',
                           'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR '
                           '2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; '
                           '.NET4.0C;'
                           '.NET4.0E; QQBrowser/7.3.9825.400)',
                           'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0 ',
                           'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) '
                           'Chrome/21.0.1180.92'
                           'Safari/537.1 LBBROWSER',
                           'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; BIDUBrowser 2.x)',
                           'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) '
                           'Chrome/20.0.1132.11 TaoBrowser/3.0 Safari/536.11']
        header = {
            'User-Agent': random.choice(random.choice(head_user_agent)),
            "Referer": "https://www.bilibili.com",
        }
        return header


class Tools:
    @staticmethod
    def transfer(string):
        return string.encode('utf-8')
