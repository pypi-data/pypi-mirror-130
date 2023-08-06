# -*- coding:utf-8 -*-
import os


def get_file_list_by_sort(dir_path):
    if not os.path.isdir(dir_path):
        return

    file_list = os.listdir(dir_path)
    file_list = list(filter(lambda file: os.path.isfile(os.path.join(dir_path, file)), file_list))
    return sorted(file_list, key=lambda file: os.path.getmtime(os.path.join(dir_path, file)))
