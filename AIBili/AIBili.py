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
from utils import assemble_headers
from utils import SpiderRetry


class UPSearch:
    def __init__(self, keyword, **kwargs):
        self.random_headers = kwargs.pop('random_headers', False)
        self.headers = assemble_headers()
        self.keyword = keyword

    def search(self):
        url = f'https://search.bilibili.com/upuser?keyword={keyword}&from_source=webtop_search&spm_id_from&order=fans'
        retry = SpiderRetry(5, ).get()
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
        followers_gt_10_uid = [uid for uid, followers in followers_dict.items() if followers > 10]

        return followers_gt_10_uid


class UPDownloader:
    def __init__(self, data_folder, audio_folder, **kwargs):
        pass


class BVDownloader:
    def __init__(self, data_folder, audio_folder, **kwargs):
        pass

    def get_uids_with_keyword(self, keyword):
        header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0'
        }
        url = f'https://search.bilibili.com/upuser?keyword={keyword}&from_source=webtop_search&spm_id_from&order=fans'
        response = self.session.get(url, headers=header)
        html = response.content.decode('utf-8')
        content = etree.HTML(html)
        contents = content.xpath('//*[@id="i_cecream"]/div/div[2]/div[2]/div/div/div[2]/div[1]/div/div/div/p/@title')
        mid = content.xpath('//*[@id="i_cecream"]/div/div[2]/div[2]/div/div/div[2]/div[1]/div/div/div/h2/a/@href')
        followers_dict = {}
        for i in range(len(contents)):
            match = re.search(r'(\d+\.?\d*)万粉丝', contents[i])
            if match:
                followers = float(match.group(1))
                uid = mid[i].split("/")[-1]
                followers_dict[uid] = followers
        followers_gt_10_uid = [uid for uid, followers in followers_dict.items() if followers > 10]
        return followers_gt_10_uid

    def save_uids(self, uids):
        file_path = os.path.join(self.data_folder, 'uids.txt')
        with open(file_path, 'w', encoding='utf-8') as f:
            for uid in uids:
                f.write(uid + '\n')

    def get_bvids_for_uid(self, uid):
        base_url = f'https://space.bilibili.com/{uid}/video?tid=0&pn={{}}&keyword=&order=pubdate'
        driver = webdriver.Chrome()
        all_contents = []
        page_num = 1
        while True:
            url = base_url.format(page_num)
            driver.get(url)
            wait = WebDriverWait(driver, 10)
            try:
                wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="submit-video-list"]/ul[2]/li/a[1]')))
                html_content = driver.page_source
                content = etree.HTML(html_content)
                contents = content.xpath('//*[@id="submit-video-list"]/ul[2]/li/@data-aid')
                if not contents:
                    break
                all_contents.extend(contents)
                page_num += 1
                time.sleep(random.randint(3, 5))
            except Exception:
                break
        driver.quit()
        return all_contents

    def save_bvids(self, bvids):
        file_path = os.path.join(self.data_folder, 'all_contents.csv')
        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            for bvid in bvids:
                writer.writerow([bvid])

    def download_audio(self, bvid):
        header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0'
        }
        url = f'https://www.bilibili.com/video/{bvid}'
        response = self.session.get(url, headers=header)
        html_data = response.text
        title = re.findall('<h1 data-title="(.*?)" title=', html_data)[0]
        initial_state = json.loads(re.findall('<script>window.__playinfo__=(.*?)</script>', html_data)[0])
        audio_url = initial_state['data']['dash']['audio'][0]['baseUrl']
        audio_content = self.session.get(url=audio_url, headers=header).content
        audio_path = os.path.join(self.audio_folder, title + '.wav')
        with open(audio_path, mode='wb') as audio_file:
            audio_file.write(audio_content)

    def main(self, keyword, new_uid):
        uids = self.get_uids_with_keyword(keyword)
        self.save_uids(uids)
        print("UIDs:", uids)

        bvids = self.get_bvids_for_uid(new_uid)
        self.save_bvids(bvids)
        print("BVIDs 已保存到:", os.path.join(self.data_folder, 'all_contents.csv'))

        for bvid in bvids:
            try:
                self.download_audio(bvid)
                print(f"Successfully downloaded audio for video with BVid: {bvid}")
            except Exception as e:
                print(f"Failed to download audio for video with BVid: {bvid}. Error: {e}")
            time.sleep(random.uniform(1, 3))


def run_bilibili_downloader(keyword, new_uid, data_folder=None, audio_folder=None):
    config_path = 'config.json'
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as config_file:
            config = json.load(config_file)
    else:
        config = {}

    data_folder = data_folder or config.get('data_folder', './data')
    audio_folder = audio_folder or config.get('audio_folder', './audio_download')

    downloader = BilibiliDownloader(data_folder=data_folder, audio_folder=audio_folder)
    downloader.main(keyword, new_uid)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Bilibili Audio Downloader')
    parser.add_argument('keyword', type=str, help='关键词')
    parser.add_argument('new_uid', type=str, help='新的uid')
    parser.add_argument('--data_folder', type=str, default=None, help='数据文件夹路径')
    parser.add_argument('--audio_folder', type=str, default=None, help='音频文件夹路径')

    args = parser.parse_args()
    run_bilibili_downloader(args.keyword, args.new_uid, args.data_folder, args.audio_folder)
