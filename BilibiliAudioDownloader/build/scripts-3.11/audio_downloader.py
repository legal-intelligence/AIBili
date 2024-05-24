import requests
import re
import os
import time
import random
import json
import csv
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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


keyword = input("请输入关键词：")
uids = get_uids_with_keyword(keyword)
data_folder = './data'
if not os.path.exists(data_folder):
    os.makedirs(data_folder)

file_path = os.path.join(data_folder, 'uids.txt')
with open(file_path, 'w', encoding='utf-8') as f:
    for uid in uids:
        f.write(uid + '\n')

print(uids)


#第2


new_uid = input("请输入新的uid: ")

base_url = 'https://space.bilibili.com/{}/video?tid=0&pn={{}}&keyword=&order=pubdate'.format(new_uid)

# 初始化 Chrome WebDriver
driver = webdriver.Chrome()

# 发送请求
driver.get(base_url.format(1))

# 使用显式等待等待页面加载完成
wait = WebDriverWait(driver, 10)
wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="submit-video-list"]/ul[2]/li[1]/a')))

# 获取页面内容
html_content1 = driver.page_source

driver.quit()
# 解析页面内容
content1 = etree.HTML(html_content1)
# 获取总页数
total_pages_text = content1.xpath('//*[@id="submit-video-list"]/ul[3]/span[1]/text()')[0]
total_pages = int(re.search(r'\d+', total_pages_text).group())

# 初始化 Chrome WebDriver
driver = webdriver.Chrome()

# 存储所有内容
all_contents = []

# 循环遍历每一页
for page in range(1, total_pages + 1):
    # 构造当前页的URL
    url = base_url.format(page)
    driver.get(url)

    wait = WebDriverWait(driver, 20)
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="submit-video-list"]/ul[2]/li/a[1]')))

    # 获取页面内容
    html_content = driver.page_source

    # 解析页面内容
    content = etree.HTML(html_content)
    contents = content.xpath('//*[@id="submit-video-list"]/ul[2]/li/@data-aid')
    all_contents.extend(contents)

    wait_time = random.randint(3, 5)
    time.sleep(wait_time)

driver.quit()

file_path = os.path.join(data_folder, 'all_contents.csv')
with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    for content in all_contents:
        writer.writerow([content])

print("bvid 已保存到:", file_path)

#第3
def download_audio(bvid):
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0'
    }

    url = f'https://www.bilibili.com/video/{bvid}'
    response = requests.get(url, headers=header)
    html_data = response.text

    title = re.findall('<h1 data-title="(.*?)" title=',html_data)[0]

    INITIAL_STATE = re.findall('<script>window.__playinfo__=(.*?)</script>', html_data)[0]
    initial_state = json.loads(INITIAL_STATE)
    audio_url = initial_state['data']['dash']['audio'][0]['baseUrl']

    audio_content = requests.get(url=audio_url, headers=header).content
    audio_folder = './audio_download'
    if not os.path.exists(audio_folder):
        os.makedirs(audio_folder)

    with open(os.path.join(audio_folder, title + '.wav'), mode='wb') as audio:
        audio.write(audio_content)

def main():
    for index in all_contents:
        try:
            download_audio(index)
            print(f"Successfully downloaded audio for video with BVid: {index}")
        except Exception as e:
            print(f"Failed to download audio for video with BVid: {index}. Error: {e}")

        time.sleep(random.uniform(1, 3))

if __name__ == "__main__":
    main()
