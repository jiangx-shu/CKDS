#! /bin/python
# -*- coding: UTF-8 -*-
# pre process two networks
import os
import csv


def read_network(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file.readlines():
            arr = line.split(' ')
            edge = []
            edge.append(int(arr[0]) -1)
            edge.append(int(arr[1]) - 1)
            edge.append(float(arr[2]))
            data.append(edge)
    return data


def write_network(file_path, data):
    with open(file_path, 'w+') as file:
        for line_arr in data:
            string = '{col1} {col2}\n'.format(col1=line_arr[0], col2=line_arr[1])
            file.writelines(string)

def write_network_with_weight(file_path, data):
    with open(file_path, 'w+') as file:
        for line_arr in data:
            string = '{col1} {col2} {col3}\n'.format(col1=line_arr[0], col2=line_arr[1], col3 =line_arr[2])
            file.writelines(string)

if __name__  == '__main__':
    file_path_base = "/Users/mhzhang/PycharmProjects/bio/data/rho_0.1_"

    network1_file_name = 'edgelist_network1.txt'
    network2_file_name = 'edgelist_network2.txt'
#两个网络 数字类型
    net1_file_name = "network1.txt"
    net2_file_name = "network2.txt"
# 两个网络 数字类型 + 权重
    net1_with_weight_file_name = "weighted_network1.txt"
    net2_with_weight_file_name = "weighted_network2.txt"

    for index in range(1, 101):
        file_path = file_path_base + str(index)
        data1 = read_network(os.path.join(file_path,network1_file_name))
        data2 = read_network(os.path.join(file_path,network2_file_name))

        write_network(os.path.join(file_path, net1_file_name), data1)
        write_network(os.path.join(file_path, net2_file_name), data2)

        write_network_with_weight(os.path.join(file_path, net1_with_weight_file_name), data1)
        write_network_with_weight(os.path.join(file_path, net2_with_weight_file_name), data2)
