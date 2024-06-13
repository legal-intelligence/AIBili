import os
import re
import time
import json
import csv
import random
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
    def __init__(self):
        pass
    @staticmethod
    def search(keyword, **kwargs):
        keyword_quo = urllib.parse.quote(keyword)
        order = kwargs.get('order', 'fans')
        followers = kwargs.get('followers', 0)
        count = int(kwargs.get('count', 12))
        page = int(kwargs.get('page', 1))
        intermediate = kwargs.get('intermediate', False)
        struct = kwargs.get('struct', True)
        data_dir = kwargs.get('data_dir')
        download_dir = kwargs.get('download_dir')
        File_op = File(data_dir, download_dir)
        json_list = []
        url = f'https://search.bilibili.com/upuser'
        params = {
            'keyword': keyword_quo,
            'from_source': 'webtop_search',
            'order': order,
            'spm_id_from': ''
        }
        response = SpiderRetry().request(url, headers=assemble_headers().get_headers(), params=params)
        tree = etree.HTML(response.text)
        mids_info = tree.xpath('//div[@class="b-user-info-card flex_start"]')
        for i in range(2, page+1):
            time.sleep(random.uniform(0.1, 0.5))
            params['page'] = i
            response = SpiderRetry().request(url, headers=assemble_headers().get_headers(), params=params)
            tree = etree.HTML(response.text)
            mids_info.extends(tree.xpath('//div[@class="b-user-info-card flex_start"]'))
        count_already = 0
        while count_already < count:
            mid_info = mids_info[count_already]
            mid = mid_info.xpath('./a[@class="mr_md"]/@href')[0].rsplit('/')[-1]
            description = mid_info.xpath('.//p/@title')[0]
            name = mid_info.xpath('.//h2/a/@title')[0]
            fans_num = Tools.transfer(description.split(" · ")[0])
            if fans_num <= followers:
                break
            mid_json = {
                'mid': mid,
                'name': name,
                'description': description,
            }
            json_list.append(mid_json)

        if not struct:
            File_op.save_json('mid.json', json_list)
            return f"已获取全部{count_already}位up主信息，信息下载至{File_op.validate_dataPath('')}"
        return json_list


class UPDownloader:
    def __init__(self):
        pass
    @staticmethod
    def download(mid: Union[str, list], **kwargs):
        self.struct = self.config.get('struct', True)
        mid = self.mid
        if isinstance(mid, str):
            mid = [mid]
        for mid_ in mid:
            url = f'https://search.bilibili.com/upuser?mid={mid_}'
            response = SpiderRetry().request(url, headers=assemble_headers().get_headers())
            json_data = json.loads(response.text)
            if 'code' in json_data:
                if json_data['code'] == -403:
                    return
            bv_info_list = []
            v_list = json_data['data']['list']['vlist']
            for v in v_list:
                bv_json = {
                    'title': v['title'],
                    'length': v['length'],
                    'bvid': v['bvid'],
                }
                bv_info_list.append(bv_json)
            # if not self.config.get("struct"):


class BVDownloader:
    def __init__(self, bv_id: Union[str, list], **kwargs):
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


if __name__ == '__main__':
    # upsearch = UPSearch()
    # upsearch.search('法律')
    up = UPDownloader
