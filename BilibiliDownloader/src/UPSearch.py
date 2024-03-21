import argparse
import re
import csv
from lxml import html
from BilibiliDownloader.src.proxy_pool import request_proxies
from urllib.parse import quote
import yaml
import os


def parse_args():
    project_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open('../config.yaml') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    up_list_file = os.path.join(project_directory, data['Paths']['up_list_file'])
    parser = argparse.ArgumentParser(description="UP info download")
    parser.add_argument("--keyword", default="律师", type=str, help="Choose keyword to search up")
    parser.add_argument("--order", default="fans", type=str, help="Choose how to order")
    parser.add_argument("--pages", default=1, type=int, help="Choose download the number of pages")
    parser.add_argument("--structured", default=True, type=bool, help="Choose whether download structured")
    parser.add_argument("--up_list_file", default=up_list_file, type=str, help="Path to UP list file")
    parser = parser.parse_args()
    return parser


class UPSearch(object):
    def __init__(self, keyword, order, pages, structured, up_list):
        self.keyword = keyword
        self.order = order
        self.pages = pages
        self.structured = structured
        self.up_list = up_list

    def get_user_space_hrefs(self, page_num):
        encode_keyword = quote(self.keyword)
        if page_num == 1:
            url = (f'https://search.bilibili.com/upuser?keyword={encode_keyword}&from_source=webtop_search&spm_id_from'
                   f'=333.1007&search_source=5&order={self.order}')
        else:
            url = (f'https://search.bilibili.com/upuser?keyword={encode_keyword}&from_source=webtop_search&spm_id_from'
                   f'=333.1007&search_source=5&order={self.order}&page={str(page_num)}')
        opener = request_proxies()
        req_view = opener.open(url)
        page_view = req_view.read().decode('utf-8')
        tree = html.fromstring(page_view)
        a_tags = tree.xpath('//a[contains(@href, "space.bilibili.com")]')
        mid_list = {}
        repeat = ""
        for a_tag in a_tags:
            href = a_tag.xpath('@href')[0]
            match = re.search(r'\d+', href).group()
            if match == repeat:
                continue
            repeat = match
            title = a_tag.xpath('@title')[0]
            mid_info = {"mid": match, "name": title}
            mid_list[match] = mid_info
        return mid_list

    @staticmethod
    def save_to_csv(mid_list, filename):
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['mid', 'name']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for mid, info in mid_list.items():
                writer.writerow(info)

    def run(self):
        mid_list = {}
        for i in range(self.pages):
            info = self.get_user_space_hrefs(i + 1)
            mid_list.update(info)
        self.save_to_csv(mid_list, self.up_list)


if __name__ == "__main__":
    args = parse_args()
    downloader = UPSearch(args.keyword, args.order, args.pages, args.structured, args.up_list_file)
    downloader.run()
