# -*- coding: utf-8 -*-
# author  : Cane
# QQ      : 54462068

import os
import time
from shutil import rmtree


#  环境变量
def get_env(name, strs=''):
    info = strs.split(';') if strs else os.environ.get(name).split(';')
    res = info[0] if len(info) == 1 else info
    return res


#  文件列表
def get_file_list(dir_path, file_type=''):
    if dir_path == '' or os.path.exists(dir_path) is False:
        return []
    if file_type == '':
        file_list = [os.path.join(root, filespath)
                     for root, dirs, files in os.walk(dir_path)
                     for filespath in files
                     ]
    else:
        file_list = [os.path.join(root, filespath)
                     for root, dirs, files in os.walk(dir_path)
                     for filespath in files
                     if str(filespath)[-len(file_type):].lower() == file_type.lower()
                     ]
    return file_list if file_list else []


# 文件名
def get_file_name(file_path, have_file_type=True):
    file_name = os.path.basename(file_path)  # 获得地址的文件名
    if not have_file_type:
        file_name = '.'.join(file_name.split('.')[:-1])
    parent_path = os.path.dirname(file_path)  # 获得地址的父链接
    return parent_path, file_name


# 获取文件类型
def get_file_type(file_path):
    parent_path, file_name = get_file_name(file_path, have_file_type=True)
    if '.' not in file_name:
        return None
    return file_name.split('.')[-1]


# 清除指定文件夹中的指定类型的文件
def clean_dir(dir_path, clean_type='whole'):
    if os.path.exists(dir_path):
        if clean_type == 'whole':
            rmtree(dir_path)
            os.makedirs(dir_path)
        file_list = get_file_list(dir_path, clean_type)
        for file in file_list:
            os.remove(file)
    else:
        dir_list = dir_path.split(os.sep)
        for i in range(len(dir_list) - 1):
            folder_path = os.sep.join(dir_list[0: i+2])
            if not os.path.exists(folder_path):
                os.mkdir(folder_path)


# 删除文件
def remove_file(filepath):
    if os.path.exists(filepath):
        if os.path.isdir(filepath):
            rmtree(filepath)
        else:
            os.remove(filepath)


# 复制文件夹目录结构
def cp_dir_structure(source, target):
    for source_root, source_dir_list, source_file in os.walk(source):
        tmp_target = source_root.replace(source, target)
        for sour_dir in source_dir_list:
            target_dir = tmp_target + os.sep + sour_dir
            if not os.path.exists(target_dir):
                os.mkdir(target_dir)


# 新建全新文件夹
def make_new_dir(filepath):
    if os.path.exists(filepath):
        rmtree(filepath)
        time.sleep(0.1)
        os.makedirs(filepath)
    else:
        os.mkdir(filepath)


if __name__ == '__main__':
    pass
