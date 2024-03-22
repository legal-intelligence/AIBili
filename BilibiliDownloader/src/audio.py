import os
import time
import urllib
import urllib.request
from BilibiliDownloader.src.proxy_pool import request_proxies
from bilibili_api import getCidAndTitle, getAudioUrl
from file_operations import *
import argparse


def parse_args():
    project_directory = get_project_directory()
    data = get_yaml_content()
    bv_list_file = os.path.join(project_directory, data['bv_list_file'])
    parser = argparse.ArgumentParser(description='Audio Downloader Parameters')
    parser.add_argument('--bv_list_file', default='../data/bv_list.csv', type=str, help='Path to BV list file')
    parser.add_argument('--bv_info_file', default='../data/bv_info.json', type=str, help='Path to BV info file')
    parser.add_argument('--download_dir', default='../download', type=str, help='Path to download directory')
    parser.add_argument('--structured', default=True, type=bool, help='Choose whether download structured')
    parser = parser.parse_args()
    return parser


class AudioDownloader(object):
    def __init__(self, bv_list_file, bv_info_file, download_dir, structured):
        self.structured = structured
        self.bv_list_file = bv_list_file
        self.bv_info_file = bv_info_file
        self.download_dir = download_dir
        create_directory(self.download_dir)

    def get_information(self, bv_list):
        info_dict = load_information(self.bv_info_file)  # Load existing information
        for bvid in bv_list:
            if bvid not in info_dict:
                cid, title, mid = getCidAndTitle(bvid)
                info_dict[bvid] = {'bvid': bvid, 'cid': cid, 'title': title, 'mid': mid}
                time.sleep(1)
            # warning no more than 150 times a minute
        save_information(info_dict, self.bv_info_file)  # Save updated information
        return info_dict

    def get_audio(self, info_dict):
        for bvid, data in info_dict.items():
            title = data['title']
            cid = data['cid']
            file_name = os.path.join(self.download_dir, f"{title}.m4a")
            if not file_exists(file_name):
                audio_url = getAudioUrl(bvid, cid)
                time.sleep(0.5)
                self.download_audio(audio_url, file_name, bvid)

    def download_audio(self, audio_url, file_name, bvid):
        opener = request_proxies()
        opener.addheaders = [
            ('Accept-Encoding', 'gzip, deflate, br'),
            ('Range', 'bytes=0-'),
            ('Referer', 'https://api.bilibili.com/x/web-interface/view?bvid=' + bvid),  # referer is must
            ('Origin', 'https://www.bilibili.com'),
        ]
        print(f'Downloading audio: {file_name}')
        st = time.time()
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(url=audio_url, filename=file_name, reporthook=self.callback)
        ed = time.time()
        print('\r' + str(round(ed - st, 2)) + ' seconds download complete:', file_name)
        time.sleep(1)

    def run(self):
        bv_list = get_bv_list(self.bv_list_file)
        info_dict = self.get_information(bv_list)
        self.get_audio(info_dict)

    @staticmethod
    def callback(blocking, block_size, totalsize):
        percent = 100.0 * blocking * block_size / totalsize
        if percent > 100:
            percent = 100
        print("\r{:^.2f}%".format(percent), end="", flush=True)


if __name__ == '__main__':
    args = parse_args()
    print(args.__dict__)
    print('The downloader starts:')
    # Initialize the downloader
    downloader = AudioDownloader(args.bv_list_file, args.bv_info_file, args.download_dir, args.structured)
    # Start the download process
    downloader.run()
