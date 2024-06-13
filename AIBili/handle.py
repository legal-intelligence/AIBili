import os


class File:
    def __init__(self):
        self.data_file = '../data'
        self.download_dir = '../download'
        self.up_list_file = '../data/up_list.txt'
        self.bv_list_file = '../data/bv_list.txt'

    def validate_dataPath(self, file_name):
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

    def validate_downloadPath(self, file_name):
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

    def delete_file(self, path):
        """
        :param path:要删除的数据信息的目录路径
        :return:成功消息或错误消息
        """
        if not path:
            path = self.data_file
        try:
            # 确认路径存在并且是一个目录
            if not os.path.exists(path) or not os.path.isdir(path):
                return f"删除路径 '{path}' 失败"

            # 遍历目录中的所有文件和子目录
            for root, dirs, files in os.walk(path, topdown=False):
                for file in files:
                    file_path = os.path.join(root, file)
                    os.remove(file_path)  # 删除文件
                for dir in dirs:
                    dir_path = os.path.join(root, dir)
                    shutil.rmtree(dir_path)  # 递归删除子目录

            return f"成功删除数据文件"

        except Exception as e:
            return f"删除路径 '{path}' 下的文件时发生错误: {str(e)}"

