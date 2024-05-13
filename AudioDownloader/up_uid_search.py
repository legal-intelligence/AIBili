import os
import re
import requests
from lxml import etree


def get_uids_with_keyword(keyword):
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0'}
    url = f'https://search.bilibili.com/upuser?keyword={keyword}&from_source=webtop_search&spm_id_from&order=fans'
    response = requests.get(url, headers=header)

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


# 获取用户输入的关键词
keyword = input("请输入关键词：")
uids = get_uids_with_keyword(keyword)
# 创建文件夹
data_folder = './data'
if not os.path.exists(data_folder):
    os.makedirs(data_folder)

# 写入uids到文件中
file_path = os.path.join(data_folder, 'uids.txt')
with open(file_path, 'w', encoding='utf-8') as f:
    for uid in uids:
        f.write(uid + '\n')

print(uids)