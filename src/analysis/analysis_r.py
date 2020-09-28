#! /bin/python
# -*- coding: UTF-8 -*-

import os
import csv

def read_to_map(file_path):
    gbm_data = dict()
    with open(file_path, 'r') as file:
        for line in file.readlines():
            arr = line.split(' ')
            key = arr[0].rstrip()
            value = arr[1].rstrip()
            gbm_data[key] = float(value)
    return gbm_data


def write_result(file_name, gbm_data):
    with open(file_name, 'w+') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in gbm_data.items():
            writer.writerow([key, value])


if __name__ == '__main__':
    # 定义文件相关路经
    gbm_file_list = ['GBM_vector.txt', 'GBM_betweenness.txt', 'GBM_closeness.txt', 'GBM_degree.txt']
    file_base_path = '/Users/jiaminsun/expsjm/single cell/GBM/GBM2'
    gbm_result_name = 'GBM_final_result.csv'
    # 所有的gbm数据
    gbm_data_list = []
    for file_path in gbm_file_list:
        gbm_data_list.append(read_to_map(os.path.join(file_base_path, file_path)))

    gbm_final_data = dict()
    # 开始处理gbm数据
    for key, value in gbm_data_list[0].items():
        total_value = value * 0.25
        for index in range(1, len(gbm_file_list)):
            total_value += (gbm_data_list[index][key] * 0.25)
        gbm_final_data[key] = total_value
    write_result(os.path.join(file_base_path, gbm_result_name), gbm_final_data)
