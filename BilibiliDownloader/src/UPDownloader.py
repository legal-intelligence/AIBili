import requests
from lxml import html
import time
import random
import json
from BilibiliDownloader.src.proxy_pool import request_proxies
from file_operations import file_exists, save_bv_list


class BilibiliCrawler:
    def __init__(self):
        self.head = [
            "Mozilla/5.0 (Windows NT 6.0; rv:2.0) Gecko/20100101 Firefox/4.0 Opera 12.14",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0) Opera 12.14",
            "Opera/12.80 (Windows NT 5.1; U; en) Presto/2.10.289 Version/12.02",
            "Opera/9.80 (Windows NT 6.1; U; es-ES) Presto/2.9.181 Version/12.00",
            "Opera/9.80 (Windows NT 5.1; U; zh-sg) Presto/2.9.181 Version/12.00",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"
        ]
        self.headers = {
            'user-agent': '',
            'Referer': 'https://www.bilibili.com/',
            'cookie': "_uuid=38505D66-5836-7006-B441-D8A7F44B081255211infoc; buvid3=2FA7C975-1F6B-47FC-961D-B998597045C953923infoc; sid=jtgdj478; LIVE_BUVID=AUTO5015857997467736; rpdid=|(~u|RmYY)J0J'ul)l~mm~R~; LIVE_PLAYER_TYPE=2; blackside_state=1; fingerprint=b7046ad02d6444e63a99648735729cdc; buvid_fp=2FA7C975-1F6B-47FC-961D-B998597045C953923infoc; buvid_fp_plain=2FA7C975-1F6B-47FC-961D-B998597045C953923infoc; DedeUserID=319136001; DedeUserID__ckMd5=c2fd54a2f5fbb92c; SESSDATA=edc55d5a%2C1629375534%2Caf07a*21; bili_jct=fcc932e20010531a42957e154977371f; CURRENT_FNVAL=80; bsource=search_google; finger=-166317360; arrange=list; PVID=1"
        }

    def set_user_agent(self):
        self.headers['user-agent'] = random.choice(self.head)

    def get_html_page(self, url):
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.content
        else:
            print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
            return None

    def get_user_space_hrefs(self, page_num):
        url = ('https://search.bilibili.com/upuser?keyword=%E5%BE%8B%E5%B8%88&from_source=webtop_search&spm_id_from'
               '=333.1007&search_source=5&order=fans&page=') + str(page_num)
        html_content = self.get_html_page(url)

        if html_content:
            tree = html.fromstring(html_content)
            href_list = tree.xpath('//a[contains(@href, "space.bilibili.com")]/@href')
            return href_list
        else:
            return []

    def crawl_user_info(self, max_pages=50):
        save_href_list = []

        for i in range(1, max_pages + 1):
            time.sleep(1)
            self.set_user_agent()
            href_list = self.get_user_space_hrefs(i)

            for href in href_list:
                save_href = href.split('/')[-1]
                save_href_list.append(save_href)
                print(href)
                self.download_mid_audio(save_href)

        if file_exists(r'../data/up_list.csv'):
            save_bv_list(r'./../data/up_list.csv', save_href_list)

    @staticmethod
    def download_mid_audio(mid):
        downloader = BidDownloader(mid)
        downloader.download_mid_audio()


class BidDownloader:
    def __init__(self, mid):
        self.mid = mid

    def download_mid_audio(self):
        bvid_list = []

        for i in range(1, 10):
            url = ('https://api.bilibili.com/x/space/arc/search?mid={}&ps=30&tid=0&pn={'
                   '}&keyword=&order=pubdate&jsonp=jsonp').format(str(self.mid), str(i))
            opener = request_proxies()
            req_view = opener.open(url)
            page_view = req_view.read().decode('utf-8')
            dic_page = json.loads(page_view)

            print(dic_page)
            video_list = dic_page['data']['list']['vlist']
            print(video_list)
            for i in video_list:
                bvid = i['bvid']
                bvid_list.append(bvid)

            save_bv_list(r'../data/bv_list.csv', bvid_list)
            time.sleep(1)
        return f"完成{self.mid}的爬取"


def main():
    crawler = BilibiliCrawler()
    crawler.crawl_user_info()


if __name__ == "__main__":
    # execute only if run as a script
    main()
