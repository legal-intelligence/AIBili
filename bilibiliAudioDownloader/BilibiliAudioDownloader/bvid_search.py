import time
import random
import re
import os
import csv
import up_uid_search
from lxml import etree
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 获取用户输入的新的uid
new_uid = input("请输入新的uid: ")

# 构造新的URL
base_url = 'https://space.bilibili.com/{}/video?tid=0&pn={{}}&keyword=&order=pubdate'.format(new_uid)

# 初始化 Chrome WebDriver
driver = webdriver.Chrome()

# 发送请求
driver.get(base_url.format(1))  # 发送请求获取第一页以获取总页数

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

    # 发送请求
    driver.get(url)

    # 使用显式等待等待页面加载完成
    wait = WebDriverWait(driver, 20)  # 增加等待时间为20秒
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="submit-video-list"]/ul[2]/li/a[1]')))

    # 获取页面内容
    html_content = driver.page_source

    # 解析页面内容
    content = etree.HTML(html_content)
    # 根据实际情况修改提取内容的 XPath
    contents = content.xpath('//*[@id="submit-video-list"]/ul[2]/li/@data-aid')

    # 将当前页的内容添加到所有内容列表中
    all_contents.extend(contents)

    # 随机等待一段时间，模拟用户操作间隔
    wait_time = random.randint(3, 5)  # 随机生成一个3到5秒的等待时间
    time.sleep(wait_time)

# 关闭 WebDriver
driver.quit()

# 写入all_contents到CSV文件中
file_path = os.path.join(up_uid_search.data_folder, 'all_contents.csv')
with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    for content in all_contents:
        writer.writerow([content])

print("bvid 已保存到:", file_path)