import argparse
import os
import yaml
from lxml import html
import time
import json
from BilibiliDownloader.src.proxy_pool import request_proxies
from file_operations import *
from AudioDownloader import *


def parse_args():
    project_directory = get_project_directory()
    data = get_yaml_content()
    data_dir = os.path.join(project_directory, data['data_dir'])
    up_list_file = os.path.join(data_dir, data['up_list_file'])
    up_info_file = os.path.join(data_dir, data['up_info_file'])
    parser = argparse.ArgumentParser()
    parser.add_argument("--mid", type=int, default=0, help="Download specified uploader")
    parser.add_argument("--pages", type=int, default=1, help="Choose download the number of pages")
    parser.add_argument("--up_list_file", default=up_list_file, type=str, help="Path to UP list file")
    parser.add_argument("--up_info_file", default=up_info_file, type=str, help="Path to UP info file")
    parser.add_argument("--structured", default=True, type=bool, help="Choose whether download structured")
    parser = parser.parse_args()
    return parser


class UPDownloader:
    def __init__(self, mid, pages, up_list_file, up_info_file, structured):
        self.mid = mid
        self.pages = pages
        self.up_list_file = up_list_file
        self.up_info_file = up_info_file
        self.structured = structured

    @staticmethod
    def download_mid_bid(mid, page):
        bvid_list = []
        if page == 1:
            url = f'https://api.bilibili.com/x/space/arc/search?mid={str(mid)}&ps=30&tid=0&order=pubdate&jsonp=jsonp'
        else:
            url = f'https://api.bilibili.com/x/space/arc/search?mid={str(mid)}&ps=30&tid=0&order=pubdate&jsonp=jsonp&pn={str(page)}'
        time.sleep(1)
        opener = request_proxies()
        req_view = opener.open(url)
        page_view = req_view.read().decode('utf-8')
        dic_page = json.loads(page_view)
        video_list = dic_page['data']['list']['vlist']
        for i in video_list:
            bvid = i['bvid']
            bvid_list.append(bvid)
        return bvid_list

    def download_and_save_bvids(self, mid, page):
        bvid_list = self.download_mid_bid(mid, page)
        if self.structured:
            mid_folder = create_mid_folder(self.mid)
            bv_list_file = save_bv_list_(mid_folder, bvid_list)
            AudioDownloader(bv_list_file, "", "", 1)
        else:
            save_bv_list(r'../data/bv_list.csv', bvid_list)

    def download_and_save_all_bvids(self, mids):
        for mid in mids:
            for page in range(1, self.pages + 1):
                self.download_and_save_bvids(mid, page)
            print(f"完成{mid}的爬取")

    def run(self):
        if self.mid != 0:
            for page in range(1, self.pages + 1):
                self.download_and_save_bvids(self.mid, page)
            return f"完成{self.mid}的爬取"
        mids = get_mids_from_csv(self.up_list_file)
        self.download_and_save_all_bvids(mids)
        return "完成列表内所有up的爬取"


if __name__ == "__main__":
    args = parse_args()
    downloader = UPDownloader(args.mid, args.pages, args.up_list_file, args.up_info_file, args.structured)
    downloader.run()
