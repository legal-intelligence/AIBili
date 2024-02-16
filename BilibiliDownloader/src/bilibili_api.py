# This module handles Bilibili API interactions.
import json
from BilibiliDownloader.src.proxy_pool import request_proxies


def getCidAndTitle(bvid, p=1):
    opener = request_proxies()
    url = 'https://api.bilibili.com/x/web-interface/view?bvid=' + bvid
    req_view = opener.open(url)
    page_view = req_view.read().decode('utf-8')
    dic_page = json.loads(page_view)
    data = dic_page['data']
    title = data['title']
    cid = data['pages'][p - 1]['cid']
    return str(cid) if cid else None, title


def getAudioUrl(bvid, cid):
    base_url = 'https://api.bilibili.com/x/player/playurl?fnval=16&'
    url = base_url + 'bvid=' + bvid + '&cid=' + cid
    opener = request_proxies()
    req_view = opener.open(url)
    page_view = req_view.read().decode('utf-8')
    dic_page = json.loads(page_view)
    audio_url = dic_page['data']['dash']['audio'][0]['baseUrl']
    return audio_url
