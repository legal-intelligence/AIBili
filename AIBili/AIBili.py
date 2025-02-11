import os
import re
import time
import json
import random
from lxml import etree
from utils import *
from handle import *
import urllib
from typing import Union


def search(keyword, **kwargs):
    keyword_quo = urllib.parse.quote(keyword)
    order = kwargs.get('order', 'fans')
    followers = kwargs.get('followers', 0)
    count = int(kwargs.get('count', 12))
    page = int(kwargs.get('page', 1))
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
    for i in range(2, page + 1):
        time.sleep(random.uniform(0.1, 0.5))
        params['page'] = i
        response = SpiderRetry().request(url, headers=assemble_headers().get_headers(), params=params)
        tree = etree.HTML(response.text)
        mids_info.extend(tree.xpath('//div[@class="b-user-info-card flex_start"]'))
    count_already = 0
    while count_already < count:
        if count_already == len(mids_info):
            break
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
        count_already += 1
    return json_list


def up_download(mid: Union[str, list], **kwargs):
    mid = mid
    if isinstance(mid, str):
        mid = [mid]
    bv_info_json = {}
    for mid_ in mid:
        if kwargs.get("headers", None) is not None:
            headers = kwargs['headers']
        else:
            headers = assemble_headers().get_headers()
        headers['referer'] = f'https://space.bilibili.com/{mid_}/video'
        url = f'https://api.bilibili.com/x/space/wbi/arc/search'
        if kwargs.get('url_eg'):
            params_origin = urllib.parse.urlparse(kwargs.get('url_eg')).query.split('&')
            params = {}
            for param in params_origin:
                params[param.split('=')[0]] = param.split('=')[1]
        else:
            params = {
                "mid": mid_,
            }
        query = urllib.parse.urlencode(params)
        response = SpiderRetry().request(f'{url}?{query}', headers=headers, params=params,
                                         cookies=kwargs.get('cookies'))
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
        bv_info_json[mid_] = bv_info_list
    return bv_info_json


def audio_download(bv_ids: Union[str, list], **kwargs):
    bv_ids = bv_ids
    if isinstance(bv_ids, str):
        bv_ids = [bv_ids]
    audio_list = []
    for bv_id in bv_ids:
        url = f'https://www.bilibili.com/video/{bv_id}'
        response = requests.get(url, headers=assemble_headers().get_headers())
        html_data = response.text
        title = re.findall('<h1 data-title="(.*?)" title=', html_data)[0]
        initial_state = json.loads(re.findall('<script>window.__playinfo__=(.*?)</script>', html_data)[0])
        audio_url = initial_state['data']['dash']['audio'][0]['baseUrl']
        audio_content = requests.get(url=audio_url, headers=assemble_headers().get_headers()).content
        audio_info_json = {
            'title': title,
            'audio': audio_content
        }
        audio_list.append(audio_info_json)
    return audio_list


class UPSearch:
    def __init__(self, key_word, **kwargs):
        self.key_word = key_word
        self.order = kwargs.get('order', 'fans')
        self.followers = kwargs.get('followers', 0)
        self.count = int(kwargs.get('count', 12))
        self.page = int(kwargs.get('page', 1))
        self.intermediate = kwargs.get('intermediate', True)
        self.struct = kwargs.get('struct', True)
        self.data_dir = kwargs.get('data_dir')
        self.download_dir = kwargs.get('download_dir')
        self.cookies = kwargs.get('cookies', None)
        self.headers = kwargs.get('headers', None)
        self.url_eg = kwargs.get('url_eg', None)

    def search(self):
        up_info_list = search(self.key_word, order=self.order, followers=self.followers, page=self.page,
                              count=self.count)
        bv_info_list = up_download([x['mid'] for x in up_info_list], headers=self.headers, cookies=self.cookies,
                                   url_eg=self.url_eg)
        if self.intermediate:
            data_dir = File().validate_datapath(self.data_dir)
            with open(os.path.join(data_dir, 'up_info.json'), 'w') as f:
                f.write(json.dumps(up_info_list))
            save_bv_info(bv_info_list, self.struct, data_dir)
        save_audio(bv_info_list, self.struct, self.download_dir)
        return f"success"


class UPDownloader:
    def __init__(self, mid: Union[str, list], **kwargs):
        self.mid = mid
        if isinstance(mid, str):
            self.mid = [mid]
        self.struct = kwargs.get('struct', True)
        self.data_dir = kwargs.get('data_dir')
        self.download_dir = kwargs.get('download_dir')
        self.intermediate = kwargs.get('intermediate', True)
        self.struct = kwargs.get('struct', True)
        self.cookies = kwargs.get('cookies', None)
        self.headers = kwargs.get('headers', None)
        self.url_eg = kwargs.get('url_eg', None)

    def download(self):
        bv_info_list = up_download([x for x in self.mid], headers=self.headers, cookies=self.cookies,
                                   url_eg=self.url_eg)
        if self.intermediate:
            data_dir = File().validate_datapath(self.data_dir)
            save_bv_info(bv_info_list, self.struct, data_dir)
        save_audio(bv_info_list, self.struct, self.download_dir)


def save_bv_info(bv_info_list, struct, data_dir):
    if not struct:
        with open(os.path.join(data_dir, 'bv_info.json'), 'w') as f:
            f.write(json.dumps(bv_info_list))
    else:
        for up_info in bv_info_list.keys():
            up_path = File().validate_datapath(os.path.join(data_dir, up_info))
            with open(os.path.join(up_path, 'up_info.json'), 'w') as f:
                f.write(json.dumps(bv_info_list[up_info]))


def save_audio(bv_info_list, struct, download_dir):
    download_dir = File().validate_datapath(download_dir)
    for mid_bv in bv_info_list.keys():
        if struct:
            download_dir = validate_dir(os.path.join(download_dir, mid_bv))
        for bvid in bv_info_list.get(mid_bv):
            audio_info = audio_download(bvid)
            with open(os.path.join(download_dir, f'{audio_info[0]["title"]}.wav', 'wb')) as f:
                f.write(audio_info[0]['audio'])
