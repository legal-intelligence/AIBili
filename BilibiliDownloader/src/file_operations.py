# This module deals with file read/write operations.
import csv
import json
import os


def get_bv_list(csv_file_path):
    bv_list = []
    with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row and not row[0].startswith('#'):
                bv_list.append(row[0])
    return bv_list


def save_bv_list(csv_file_path, bv_list):
    if file_exists(csv_file_path):
        # 获取现有的 bv_list
        existing_bv_list = get_bv_list(csv_file_path)
        # 将新的 bv_list 添加到现有的 bv_list 中
        merged_bv_list = existing_bv_list + bv_list
    else:
        merged_bv_list = bv_list
    # 将后续获取的bv_list添加到csv文件中
    with open(csv_file_path, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for bv in merged_bv_list:
            writer.writerow([bv])


def save_information(info_dict, json_file_path):
    with open(json_file_path, 'w', encoding='utf-8') as jsonfile:
        json.dump(info_dict, jsonfile, ensure_ascii=False, indent=4)


def load_information(json_file_path):
    if not os.path.exists(json_file_path):
        return {}
    with open(json_file_path, 'r', encoding='utf-8') as jsonfile:
        info_dict = json.load(jsonfile)
    return info_dict


def file_exists(file_path):
    return os.path.isfile(file_path)


def create_directory(dir_path):
    os.makedirs(dir_path, exist_ok=True)
