import requests
from lxml import html
import time
import random
from file_operations import file_exists, save_bv_list

data = []


def get_info():
    i = 0
    while (i <= 50):
        i += 1
        time.sleep(1)
        # 获取html页面
        if (i == 1):
            url = 'https://search.bilibili.com/upuser?keyword=%E5%BE%8B%E5%B8%88&from_source=webtop_search&spm_id_from=333.1007&search_source=5&order=fans'
        else:
            url = 'https://search.bilibili.com/upuser?keyword=%E5%BE%8B%E5%B8%88&from_source=webtop_search&spm_id_from=333.1007&search_source=5&order=fans&page=' + str(
                i)
        head = [
            "Mozilla/5.0 (Windows NT 6.0; rv:2.0) Gecko/20100101 Firefox/4.0 Opera 12.14",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0) Opera 12.14",
            "Opera/12.80 (Windows NT 5.1; U; en) Presto/2.10.289 Version/12.02",
            "Opera/9.80 (Windows NT 6.1; U; es-ES) Presto/2.9.181 Version/12.00",
            "Opera/9.80 (Windows NT 5.1; U; zh-sg) Presto/2.9.181 Version/12.00",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"
        ]
        headers = {
            'user-agent': random.choice(head),
            'Referer': 'https://www.bilibili.com/',
            'cookie': "_uuid=38505D66-5836-7006-B441-D8A7F44B081255211infoc; buvid3=2FA7C975-1F6B-47FC-961D-B998597045C953923infoc; sid=jtgdj478; LIVE_BUVID=AUTO5015857997467736; rpdid=|(~u|RmYY)J0J'ul)l~mm~R~; LIVE_PLAYER_TYPE=2; blackside_state=1; fingerprint=b7046ad02d6444e63a99648735729cdc; buvid_fp=2FA7C975-1F6B-47FC-961D-B998597045C953923infoc; buvid_fp_plain=2FA7C975-1F6B-47FC-961D-B998597045C953923infoc; DedeUserID=319136001; DedeUserID__ckMd5=c2fd54a2f5fbb92c; SESSDATA=edc55d5a%2C1629375534%2Caf07a*21; bili_jct=fcc932e20010531a42957e154977371f; CURRENT_FNVAL=80; bsource=search_google; finger=-166317360; arrange=list; PVID=1"
        }
        # 发送HTTP请求获取页面内容
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            # 使用lxml解析HTML内容
            tree = html.fromstring(response.content)
            # 使用XPath获取所有包含“bilibilispace”的href属性
            href_list = tree.xpath('//a[contains(@href, "space.bilibili.com")]/@href')
            save_href_list = []
            # 打印结果
            for href in href_list:
                save_href = href.split('/')[-1]
                save_href_list.append(save_href)
                print(href)
            if file_exists(r'../data/up_list.csv'):
                save_bv_list(r'./../data/up_list.csv', save_href_list)
        else:
            print(f"Failed to retrieve the webpage. Status code: {response.status_code}")


def main():
    get_info()


if __name__ == "__main__":
    # execute only if run as a script
    main()
