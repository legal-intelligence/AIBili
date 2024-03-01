import json
import time
from BilibiliDownloader.src.proxy_pool import request_proxies
from file_operations import save_bv_list


class BidDownloader:
    def __init__(self, mid):
        self.mid = mid

    @staticmethod
    def download_mid_audio(mid):
        bvid_list = []  # 视频地址

        for i in range(1, 10):  # 前10页
            url = 'https://api.bilibili.com/x/space/arc/search?mid=527145352&ps=30&tid=0&pn={}&keyword=&order=pubdate&jsonp=jsonp'.format(
                str(i))
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
        return f"完成{mid}的爬取"


if __name__ == '__main__':
    print('The downloader starts:')
    # Initialize the downloader
    downloader = BidDownloader.download_mid_audio(527145352)
