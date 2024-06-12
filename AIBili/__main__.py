import argparse


def main():
    pass


def parse_args():
    parser = argparse.ArgumentParser(description="AIBili，", prog="AIBili")
    """
        B站对于访问api的IP的管控策略是：
        每十分钟检测一次，若被ban则一次半个小时
    """
    # 三个功能，分别是通过关键词获取up主、通过up主主页获取bv信息和通过bv号获取音频
    subparsers = parser.add_subparsers(dest="command")
    parser_upsearch = subparsers.add_parser("upsearch", help="Search Aim UP")
    # 搜索参数组
    # 排序顺序
    # 是否结构化
    # 文件夹地址
    # 页数
    # 下载数量
    # 关键词
    # 是否保存中间文件
