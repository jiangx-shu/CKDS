# -*- coding: utf-8 -*-

import os
import networkx as nx
import src.util.logger as logger

process_logger = logger.logger('KDS_MINUS')

# if len(sys.argv) < 1 :
#     print('参数错误，使用方法 python minus_graph.py $index')
#     exit(-1)
# 当前处理的目录索引
# index = int(sys.argv[1])


# 读取网络
def read_network(network, file_path):
    with open(file_path, 'r') as file:
        for line in file:
            arr = line.split('\t')
            network.add_edge(int(arr[0]), int(arr[1]))


# 移除两个网络的共同边
def minus_subgraph(network1, network2):
    common_edges = list(set(network1.edges) & set(network2.edges))

    full_network = nx.compose(network1, network2)
    for edge in common_edges:
        full_network.remove_edge(edge[0], edge[1])
    return full_network


def read_important(base_path, file_name):
    important_nodes = []
    with open(os.path.join(base_path, file_name), 'r') as file:
        for line in file:
            important_nodes.append(line.rstrip())
    return important_nodes



def main(base_path):
    # 文件名
    sub_graph1 = 'subgraph_test1.txt'
    sub_graph2 = 'subgraph_test2.txt'
    important_graph = 'important.txt'
    # 创建网络
    sub_graph1_network = nx.Graph()
    sub_graph2_network = nx.Graph()

    # 打开文件读取网络
    read_network(sub_graph1_network, os.path.join(base_path, sub_graph1))
    read_network(sub_graph2_network, os.path.join(base_path, sub_graph2))
    # nx.draw_networkx(sub_graph1_network)
    # plt.title('network1_origin')
    # plt.show()

    # nx.draw_networkx(sub_graph2_network)
    # plt.title('network2_origin')
    # plt.show()

    minus_network = minus_subgraph(sub_graph1_network, sub_graph2_network)

    # nx.draw_networkx(minus_network)
    # plt.title('network_minus')
    # plt.show()

    important_nodes = read_important(base_path, important_graph)
    process_logger.debug('minus_res_nodes:%s', nx.number_of_nodes(minus_network))
    process_logger.debug('total nodes:{total_nodes}'.format(total_nodes=important_nodes))

    #print('network nodes:{network_nodes}'.format(network_nodes=list(minus_network.nodes)))
    hit = 0
    for node in important_nodes:
        if (int(node) - 1) in list(minus_network.nodes):
            hit = hit + 1
    process_logger.debug('{hit}'.format(hit=hit))
    return hit, nx.number_of_nodes(minus_network)

def cal_result():
    base_path = '/Users/mhzhang/PycharmProjects/bio/data/rho_0.1_'
    count = 0
    count_network_nodes=0
    for index in range(1, 101):
        process_logger.debug('---[UNIT:{unit}]---'.format(unit=index))
        result_tuple = main(base_path + str(index))
        hit = result_tuple[0]
        count = count + hit

        network_nodes = result_tuple[1]
        count_network_nodes += network_nodes
    process_logger.debug('---[TOTAL:{total}]---'.format(total=count))
    process_logger.debug('---[TOTAL MINUS NETWORK :{total_network_nodes}]---'
          .format(total_network_nodes=count_network_nodes))
    return count,count_network_nodes
if __name__ == '__main__':
    base_path = '/Users/mhzhang/PycharmProjects/bio/data/rho_0.1_'
    count = 0
    count_network_nodes=0
    for index in range(1, 101):
        process_logger.debug('---[UNIT:{unit}]---'.format(unit=index))
        result_tuple = main(base_path + str(index))
        hit = result_tuple[0]
        count = count + hit

        network_nodes = result_tuple[1]
        count_network_nodes += network_nodes
    process_logger.debug('---[TOTAL:{total}]---'.format(total=count))
    process_logger.debug('---[TOTAL MINUS NETWORK :{total_network_nodes}]---'
          .format(total_network_nodes=count_network_nodes))





