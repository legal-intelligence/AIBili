import json
import os


class File:
    def __init__(self):
        self.data_file = '../data'
        self.download_dir = '../download'

    def validate_datapath(self, file_name):
        """
        :param file_name:data保存的文件名
        :return:新建好的文件目录
        检验是否提供数据保存路径
        未提供则使用默认
        提供则先判断是否存在
        不存在则新建
        """
        if not file_name:
            if not os.path.exists(self.data_file):
                # 不存在则新建
                os.makedirs(self.data_file)
            return self.data_file
        try:
            if not os.path.exists(file_name):
                # 不存在则新建
                os.makedirs(file_name)
                return file_name
        except Exception as e:
            return f"创建路径'P{file_name}'失败：{str(e)}"

    def validate_download_path(self, file_name):
        """
        :param file_name:download保存的文件目录名
        :return:建好的文件目录
        检验是否提供下载路径
        未提供则使用默认
        提供则先判断是否存在
        不存在则新建
        """
        if not file_name:
            if not os.path.exists(self.download_dir):
                os.makedirs(self.download_dir)
            return self.download_dir
        try:
            if not os.path.exists(file_name):
                # 不存在则新建
                os.makedirs(file_name)
                return file_name
        except Exception as e:
            return f"创建路径'P{file_name}'失败：{str(e)}"


def save_json(file_name, data):
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(json.dumps(data, indent=4, ensure_ascii=False))


def validate_dir(folder_path):
    try:
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
    except Exception as e:
        return f"新建 '{folder_path}'目录出现问题"
    return folder_path
