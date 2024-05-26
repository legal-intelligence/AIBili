# This module deals with file read/write operations.
import csv
import json
import os
import yaml


def get_project_directory():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_yaml_content():
    project_directory = get_project_directory()
    config_file_path = os.path.join(project_directory, 'config.yaml')
    with open(config_file_path) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    return data.get('Paths', {})


def save_to_csv(mid_list, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['mid', 'name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for mid, info in mid_list.items():
            writer.writerow(info)


def get_mids_from_csv(filename):
    mids = []
    with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            mid = row['mid']
            mids.append(mid)
    return mids


def create_mid_folder(mid):
    project_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    mid_folder = os.path.join(project_directory, 'data', 'mid_' + str(mid))
    if not os.path.exists(mid_folder):
        os.makedirs(mid_folder)
    return mid_folder


def save_bv_list_(mid_folder, bvid_list):
    bv_list_file = os.path.join(mid_folder, 'bv_list.txt')
    with open(bv_list_file, 'a', encoding='utf-8') as f:
        for bvid in bvid_list:
            f.write(bvid + '\n')
    return bv_list_file


def get_bv_list(csv_file_path):
    bv_list = []
    with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row and not row[0].startswith('#'):
                bv_list.append(row[0])
    return bv_list


def save_bv_list(csv_file_path, bv_list):
    with open(csv_file_path, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for bv in bv_list:
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
