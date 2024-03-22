import argparse
import re
from lxml import html
from BilibiliDownloader.src.proxy_pool import request_proxies
from urllib.parse import quote
import os
from file_operations import save_to_csv, get_yaml_content, get_project_directory


def parse_args():
    project_directory = get_project_directory()
    data = get_yaml_content()
    up_list_file = os.path.join(project_directory, data['up_list_file'])
    parser = argparse.ArgumentParser(description="UP info download")
    parser.add_argument("--keyword", default="律师", type=str, help="Choose keyword to search up")
    parser.add_argument("--order", default="fans", type=str, help="Choose how to order")
    parser.add_argument("--pages", default=1, type=int, help="Choose download the number of pages")
    parser.add_argument("--up_list_file", default=up_list_file, type=str, help="Path to UP list file")
    parser = parser.parse_args()
    return parser


class UPSearch(object):
    def __init__(self, keyword, order, pages, up_list):
        self.keyword = keyword
        self.order = order
        self.pages = pages
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

    def run(self):
        mid_list = {}
        for i in range(self.pages):
            info = self.get_user_space_hrefs(i + 1)
            mid_list.update(info)
        save_to_csv(mid_list, self.up_list)


if __name__ == "__main__":
    args = parse_args()
    downloader = UPSearch(args.keyword, args.order, args.pages, args.up_list_file)
    downloader.run()
