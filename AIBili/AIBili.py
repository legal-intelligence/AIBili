import os
import re
import time
import json
import csv
import random
import requests
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from utils import *
from handle import *
import urllib
from typing import Union


class UPSearch:
    def __init__(self, keyword, **kwargs):
        self.keyword = keyword
        self.config = kwargs
        # 验证参数是否提供地址，如果提供地址地址是否合法

    def search(self):
        keyword_quo = urllib.parse.puote(self.keyword)
        order = self.config.get('order', 'fans')
        followers_ = self.config.get('followers', 10)
        url = f'https://search.bilibili.com/upuser?keyword={keyword_quo}&from_source=webtop_search&spm_id_from&order={order}'
        response = SpiderRetry().request(url, headers=assemble_headers().get_headers())
        html = response.content.decode('utf-8')
        content = etree.HTML(html)
        contents = content.xpath('//*[@id="i_cecream"]/div/div[2]/div[2]/div/div/div[2]/div[1]/div/div/div/p/@title')
        mid = content.xpath('//*[@id="i_cecream"]/div/div[2]/div[2]/div/div/div[2]/div[1]/div/div/div/h2/a/@href')
        followers_dict = {}
        for i in range(len(contents)):
            match = re.search(r'(\d+\.\d+|\d+)万粉丝', contents[i])
            if match:
                followers = float(match.group(1))
                uid = mid[i].split("/")[-1]
                followers_dict[uid] = followers
        followers_gt_10_uid = [uid for uid, followers in followers_dict.items() if followers > followers_]
        data_folder = File().validate_dataPath(config.get('data_path', ''))
        file_path = os.path.join(data_folder, 'uids.txt')
        with open(file_path, 'w', encoding='utf-8') as f:
            for uid in uids:
                f.write(uid + '\n')
        if self.config.get("struct"):
            UPDownloader(followers_gt_10_uid)
        return followers_gt_10_uid


class UPDownloader:
    def __init__(self, mid: Union[str, list], **kwargs):
        self.mid = mid
        self.config = kwargs

    def download(self):
        mid = self.mid
        if isinstance(mid, str):
            mid = [mid]


class BVDownloader:
    def __init__(self, bv_id: Union[str,list], **kwargs):
        self.bv_id = bv_id
        self.config = kwargs

    def audioDownload(self):
        bv_ids = self.bv_id
        if isinstance(bv_ids, str):
            bv_ids = [bv_ids]
        for bv_id in bv_ids:
            url = f'https://www.bilibili.com/video/{bvid}'
            response = requests.get(url, headers=assemble_headers().get_headers())
            html_data = response.text
            title = re.findall('<h1 data-title="(.*?)" title=', html_data)[0]
            INITIAL_STATE = re.findall('<script>window.__playinfo__=(.*?)</script>', html_data)[0]
            initial_state = json.loads(INITIAL_STATE)
            audio_url = initial_state['data']['dash']['audio'][0]['baseUrl']
            audio_content = requests.get(url=audio_url, headers=header).content
