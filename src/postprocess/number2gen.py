# -*- coding: utf-8 -*-
"""
Created on Tue May 29 13:55:56 2018
A
@author: 44751
"""
import os
import src.constants.constants as constants

gen_column=[]

# 读取所有的基因信息
with open(os.path.join(constants.base_path, constants.gen_name_ansc_file) , 'r') as gen_file:
    for col1 in gen_file.readlines():
        gen_column.append(col1)


# 开始翻译节点信息
node_gen_file = open(os.path.join(constants.base_path, constants.minus_net_node_gen_file),'w+')
with open(os.path.join(constants.base_path, constants.minus_net_node_file), 'r') as file:
    for i in file.readlines():
        node_gen_file.writelines(gen_column[int(i)])
node_gen_file.close()

# 开始翻译边信息
edge_gen_file = open(os.path.join(constants.base_path, constants.minus_net_edge_gen_file),'w+')
with open(os.path.join(constants.base_path, constants.minus_net_edge_file), 'r') as file:
    for line in file.readlines():
        arr = line.split('\t')
        edge_gen_file.writelines(gen_column[int(arr[0])].strip() + ' '+ gen_column[int(arr[1])])
edge_gen_file.close()
