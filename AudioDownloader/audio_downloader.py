import requests
import re
import os
import time
import random
import json
import up_uid_search
import bvid_search

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
    for index in bvid_search.all_contents:
        try:
            download_audio(index)
            print(f"Successfully downloaded audio for video with BVid: {index}")
        except Exception as e:
            print(f"Failed to download audio for video with BVid: {index}. Error: {e}")
        # Random wait between 1 to 3 seconds
        time.sleep(random.uniform(1, 3))

if __name__ == "__main__":
    main()
