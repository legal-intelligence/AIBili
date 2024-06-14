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
                                         cookies=kwargs.get('cookies', None))
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
        INITIAL_STATE = re.findall('<script>window.__playinfo__=(.*?)</script>', html_data)[0]
        initial_state = json.loads(INITIAL_STATE)
        audio_url = initial_state['data']['dash']['audio'][0]['baseUrl']
        audio_content = requests.get(url=audio_url, headers=header).content
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
                f.write(json.dumps(bv_info_list['up_info']))


def save_audio(bv_info_list, struct, download_dir):
    for mid_bv in bv_info_list.keys():
        download_dir = File().validate_datapath(download_dir)
        if struct:
            download_dir = validate_dir(os.path.join(download_dir, mid_bv))
        for bvid in bv_info_list.get(mid_bv):
            audio_info = audio_download(bvid)
            with open(os.path.join(download_dir, f'{audio_info[0]["title"]}.wav', 'w')) as f:
                f.write(audio_info[0]['audio'])


if __name__ == "__main__":
    cookies = {
        'buvid3': 'E8945886-8543-6D8C-13CC-BC5CAEFBA36C76919infoc',
        'b_nut': '100',
        'b_lsid': 'A115101D1_190144DD532',
        'bsource': 'search_bing',
        '_uuid': 'B7108A235-ABD10-1079C-210710-463D52218103763576infoc',
        'buvid_fp': '0be35eaa7e5d935853c9d958bb3c9b75',
        'enable_web_push': 'DISABLE',
        'header_theme_version': 'CLOSE',
        'buvid4': 'B26FECD0-BCE9-4297-CB38-9EF9EEFE84F862144-024061401-V0f8ULqgILvaGuu4Vr4OGmcRy74IdTu4hoixo4%2Fa4rhtjJsxLAujrKWBywuKcqBE',
        'home_feed_column': '4',
        'browser_resolution': '1392-778',
        'CURRENT_FNVAL': '4048',
        'bili_ticket': 'eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTg1ODc4ODcsImlhdCI6MTcxODMyODYyNywicGx0IjotMX0.y-QnRuQdSDiv7aTFuHh7cmYqhSyCdULhwAj1EHzlBds',
        'bili_ticket_expires': '1718587827',
        'rpdid': '0zbfVHgTAI|AZCM55a0|4if|3w1ShVMQ',
        'bp_t_offset_336260687': '942705460146864178',
        'SESSDATA': '8c30e23b%2C1733883524%2Ca2011%2A62CjDV9pUAkOH30meq80Wj4ClLRNAXB9-f3eQFD26cDMwJ0_J2zLwY9lKvJnVgEPKFaoMSVnNwT2dKaEJsQWhpZ3plVTJlaVZZYnJZLUpDRDFrYnVWaXZBNktCU0dmSEk4QUlFY3RsQWN6bjZaci1zbnBUTkRLR05VZGFzSDZER05KeE9SY0NiQWlnIIEC',
        'bili_jct': 'b8f9c4967ef3d98e8b7cbcb2c1c8e78c',
        'DedeUserID': '3546702594181339',
        'DedeUserID__ckMd5': '38bbd1b234bbb4e7',
        'sid': '7plw0qrr',
    }

    headers = {
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        # 'cookie': 'buvid3=E8945886-8543-6D8C-13CC-BC5CAEFBA36C76919infoc; b_nut=100; b_lsid=A115101D1_190144DD532; bsource=search_bing; _uuid=B7108A235-ABD10-1079C-210710-463D52218103763576infoc; buvid_fp=0be35eaa7e5d935853c9d958bb3c9b75; enable_web_push=DISABLE; header_theme_version=CLOSE; buvid4=B26FECD0-BCE9-4297-CB38-9EF9EEFE84F862144-024061401-V0f8ULqgILvaGuu4Vr4OGmcRy74IdTu4hoixo4%2Fa4rhtjJsxLAujrKWBywuKcqBE; home_feed_column=4; browser_resolution=1392-778; CURRENT_FNVAL=4048; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTg1ODc4ODcsImlhdCI6MTcxODMyODYyNywicGx0IjotMX0.y-QnRuQdSDiv7aTFuHh7cmYqhSyCdULhwAj1EHzlBds; bili_ticket_expires=1718587827; rpdid=0zbfVHgTAI|AZCM55a0|4if|3w1ShVMQ; bp_t_offset_336260687=942705460146864178; SESSDATA=8c30e23b%2C1733883524%2Ca2011%2A62CjDV9pUAkOH30meq80Wj4ClLRNAXB9-f3eQFD26cDMwJ0_J2zLwY9lKvJnVgEPKFaoMSVnNwT2dKaEJsQWhpZ3plVTJlaVZZYnJZLUpDRDFrYnVWaXZBNktCU0dmSEk4QUlFY3RsQWN6bjZaci1zbnBUTkRLR05VZGFzSDZER05KeE9SY0NiQWlnIIEC; bili_jct=b8f9c4967ef3d98e8b7cbcb2c1c8e78c; DedeUserID=3546702594181339; DedeUserID__ckMd5=38bbd1b234bbb4e7; sid=7plw0qrr',
        'origin': 'https://space.bilibili.com',
        'priority': 'u=1, i',
        'referer': 'https://space.bilibili.com/97213827/video',
        'sec-ch-ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0',
    }
    url_eg = "'https://api.bilibili.com/x/space/wbi/arc/search?mid=97213827&ps=30&tid=0&pn=1&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&dm_img_list=[%7B%22x%22:770,%22y%22:559,%22z%22:0,%22timestamp%22:10766,%22k%22:123,%22type%22:0%7D,%7B%22x%22:844,%22y%22:605,%22z%22:66,%22timestamp%22:10867,%22k%22:73,%22type%22:0%7D,%7B%22x%22:872,%22y%22:584,%22z%22:80,%22timestamp%22:10975,%22k%22:109,%22type%22:0%7D,%7B%22x%22:1056,%22y%22:769,%22z%22:261,%22timestamp%22:11193,%22k%22:74,%22type%22:0%7D,%7B%22x%22:1086,%22y%22:941,%22z%22:256,%22timestamp%22:11295,%22k%22:63,%22type%22:0%7D,%7B%22x%22:886,%22y%22:833,%22z%22:56,%22timestamp%22:11396,%22k%22:85,%22type%22:0%7D,%7B%22x%22:1335,%22y%22:1190,%22z%22:528,%22timestamp%22:11496,%22k%22:110,%22type%22:0%7D,%7B%22x%22:1011,%22y%22:544,%22z%22:342,%22timestamp%22:11596,%22k%22:113,%22type%22:0%7D,%7B%22x%22:863,%22y%22:388,%22z%22:218,%22timestamp%22:11696,%22k%22:110,%22type%22:0%7D,%7B%22x%22:1102,%22y%22:629,%22z%22:451,%22timestamp%22:11796,%22k%22:94,%22type%22:0%7D,%7B%22x%22:809,%22y%22:336,%22z%22:135,%22timestamp%22:11896,%22k%22:86,%22type%22:0%7D,%7B%22x%22:954,%22y%22:487,%22z%22:262,%22timestamp%22:11996,%22k%22:112,%22type%22:0%7D,%7B%22x%22:818,%22y%22:351,%22z%22:126,%22timestamp%22:12116,%22k%22:66,%22type%22:1%7D,%7B%22x%22:1406,%22y%22:932,%22z%22:712,%22timestamp%22:12735,%22k%22:108,%22type%22:0%7D,%7B%22x%22:1717,%22y%22:1104,%22z%22:888,%22timestamp%22:12835,%22k%22:92,%22type%22:0%7D,%7B%22x%22:2606,%22y%22:2189,%22z%22:1327,%22timestamp%22:12935,%22k%22:92,%22type%22:0%7D,%7B%22x%22:1495,%22y%22:1217,%22z%22:29,%22timestamp%22:13035,%22k%22:85,%22type%22:0%7D,%7B%22x%22:2959,%22y%22:2683,%22z%22:1487,%22timestamp%22:13136,%22k%22:95,%22type%22:0%7D,%7B%22x%22:3238,%22y%22:2888,%22z%22:1758,%22timestamp%22:14558,%22k%22:97,%22type%22:0%7D,%7B%22x%22:1626,%22y%22:909,%22z%22:143,%22timestamp%22:14660,%22k%22:83,%22type%22:0%7D,%7B%22x%22:1582,%22y%22:694,%22z%22:405,%22timestamp%22:15328,%22k%22:89,%22type%22:0%7D,%7B%22x%22:1774,%22y%22:1125,%22z%22:547,%22timestamp%22:15430,%22k%22:60,%22type%22:0%7D,%7B%22x%22:2117,%22y%22:1536,%22z%22:801,%22timestamp%22:15530,%22k%22:86,%22type%22:0%7D,%7B%22x%22:3330,%22y%22:3155,%22z%22:1808,%22timestamp%22:15631,%22k%22:87,%22type%22:0%7D,%7B%22x%22:2444,%22y%22:2299,%22z%22:924,%22timestamp%22:15732,%22k%22:114,%22type%22:0%7D,%7B%22x%22:1994,%22y%22:1842,%22z%22:472,%22timestamp%22:15836,%22k%22:106,%22type%22:0%7D,%7B%22x%22:2877,%22y%22:2718,%22z%22:1353,%22timestamp%22:15937,%22k%22:69,%22type%22:0%7D,%7B%22x%22:3482,%22y%22:3285,%22z%22:1957,%22timestamp%22:16040,%22k%22:106,%22type%22:0%7D,%7B%22x%22:4557,%22y%22:4359,%22z%22:3035,%22timestamp%22:16143,%22k%22:63,%22type%22:0%7D,%7B%22x%22:4038,%22y%22:3832,%22z%22:2517,%22timestamp%22:17729,%22k%22:65,%22type%22:0%7D,%7B%22x%22:3926,%22y%22:3543,%22z%22:2499,%22timestamp%22:17830,%22k%22:117,%22type%22:0%7D,%7B%22x%22:4799,%22y%22:4343,%22z%22:3453,%22timestamp%22:17930,%22k%22:116,%22type%22:0%7D,%7B%22x%22:2840,%22y%22:2357,%22z%22:1644,%22timestamp%22:18030,%22k%22:84,%22type%22:0%7D,%7B%22x%22:4536,%22y%22:4046,%22z%22:3384,%22timestamp%22:18130,%22k%22:86,%22type%22:0%7D,%7B%22x%22:1529,%22y%22:1038,%22z%22:380,%22timestamp%22:18230,%22k%22:65,%22type%22:0%7D,%7B%22x%22:4856,%22y%22:4373,%22z%22:3706,%22timestamp%22:19838,%22k%22:110,%22type%22:0%7D,%7B%22x%22:2946,%22y%22:2531,%22z%22:1776,%22timestamp%22:19939,%22k%22:96,%22type%22:0%7D,%7B%22x%22:1738,%22y%22:1324,%22z%22:565,%22timestamp%22:20040,%22k%22:126,%22type%22:0%7D,%7B%22x%22:3713,%22y%22:3306,%22z%22:2542,%22timestamp%22:20149,%22k%22:121,%22type%22:0%7D,%7B%22x%22:4337,%22y%22:3923,%22z%22:3164,%22timestamp%22:20308,%22k%22:72,%22type%22:0%7D,%7B%22x%22:2482,%22y%22:2077,%22z%22:1305,%22timestamp%22:20408,%22k%22:82,%22type%22:0%7D,%7B%22x%22:3910,%22y%22:3396,%22z%22:2600,%22timestamp%22:20509,%22k%22:113,%22type%22:0%7D,%7B%22x%22:1920,%22y%22:1407,%22z%22:607,%22timestamp%22:20615,%22k%22:112,%22type%22:0%7D,%7B%22x%22:5386,%22y%22:4882,%22z%22:4069,%22timestamp%22:22726,%22k%22:92,%22type%22:0%7D,%7B%22x%22:5318,%22y%22:4862,%22z%22:3236,%22timestamp%22:22827,%22k%22:111,%22type%22:0%7D,%7B%22x%22:5845,%22y%22:5690,%22z%22:3251,%22timestamp%22:22927,%22k%22:101,%22type%22:0%7D,%7B%22x%22:2691,%22y%22:2575,%22z%22:72,%22timestamp%22:23028,%22k%22:98,%22type%22:0%7D,%7B%22x%22:7224,%22y%22:7100,%22z%22:4514,%22timestamp%22:23129,%22k%22:90,%22type%22:0%7D,%7B%22x%22:6497,%22y%22:6444,%22z%22:3735,%22timestamp%22:23229,%22k%22:68,%22type%22:0%7D,%7B%22x%22:6758,%22y%22:6706,%22z%22:3993,%22timestamp%22:23329,%22k%22:81,%22type%22:0%7D]&dm_img_str=V2ViR0wgMS4wIChPcGVuR0wgRVMgMi4wIENocm9taXVtKQ&dm_cover_img_str=QU5HTEUgKEFNRCwgQU1EIFJhZGVvbiA3ODBNIEdyYXBoaWNzICgweDAwMDAxNUJGKSBEaXJlY3QzRDExIHZzXzVfMCBwc181XzAsIEQzRDExKUdvb2dsZSBJbmMuIChBTU&dm_img_inter=%7B%22ds%22:[%7B%22t%22:4,%22c%22:%22bW9yZQ%22,%22p%22:[135,45,45],%22s%22:[26,26,52]%7D],%22wh%22:[3131,5402,3],%22of%22:[1917,2834,417]%7D&w_rid=958e86ef2da3b21204dd327c216186d9&wts=1718331552'"
    up = UPDownloader('11097284', cookies=cookies, headers=headers, url_eg=url_eg)
    up.download()
    # audio_download('BV1V7421d7Vj')
