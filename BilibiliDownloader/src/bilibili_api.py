# This module handles Bilibili API interactions.
import json
import time
import requests

session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'
})
proxies = {
    'http': 'http://127.0.0.1:33210',
    'https': 'https://127.0.0.1:33210'
}


def getCidAndTitle(bvid, p=1):
    url = 'https://api.bilibili.com/x/web-interface/view?bvid=' + bvid
    try:
        response = requests.get(url, proxies=proxies)
        response.raise_for_status()  # 检查请求是否成功
        data = response.json()['data']
        print(data)
        title = data['title']
        cid = data['pages'][p - 1]['cid']
        return str(cid), title
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
    except requests.exceptions.ConnectionError as e:
        print(f"Connection Error: {e}")
    except requests.exceptions.Timeout as e:
        print(f"Timeout Error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Request Exception: {e}")
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")

    # 简单的重试逻辑
    time.sleep(1)  # 稍微等待一秒
    return getCidAndTitle(bvid, p)  # 重新尝试


def getAudioUrl(bvid, cid):
    base_url = 'https://api.bilibili.com/x/player/playurl?fnval=16&'
    url = base_url + 'bvid=' + bvid + '&cid=' + cid
    audio_url = requests.get(url).json()['data']['dash']['audio'][0]['baseUrl']
    return audio_url
