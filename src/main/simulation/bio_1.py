import os
from collections import OrderedDict
from src.main.node_path import NodePath
import networkx as nx
import src.util.bio_util as util
import src.main.simulation.minus_kds as kds
import src.util.logger as logger

process_logger = logger.logger('PROCESS')
result_logger = logger.logger('RESULT')


# 入口函数，调用该函数进行计算。
def start_calculate(origin_network_path, dvalue_path, subgraph_network_path, subgraph_node_path, common_top_nodes,
                    dvalue_weight, edge_weight):
    # 生成边权重的map
    edge_weight_dict = {}

    # 读取origin network的边权重
    with open(origin_network_path, 'r') as file:
        for line in file:
            arr = line.split(' ')
            smaller_node = min(int(arr[0]), int(arr[1]))
            bigger_node = max(int(arr[0]), int(arr[1]))
            dict_key = str(smaller_node) + '#' + str(bigger_node)
            edge_weight_dict[dict_key] = float(arr[2])
    process_logger.debug('[Edge Weight Dict]:%s', edge_weight_dict)

    # 开始生成图
    cancer_net = nx.Graph()
    with open(origin_network_path, 'r') as cancer:
        for line in cancer:
            line = line.strip('\n').split(' ')
            cancer_net.add_edge(line[0], line[1])

    # 读取dvalue
    node_dvalue_dict = {}
    with open(dvalue_path, 'r') as dvalue:
        for node in dvalue:
            node = node.strip('\n').split('\t')
            if len(node) == 2:
                node_dvalue_dict[str(int(node[0]))] = node[1]
    process_logger.debug('[Node DValue Dict]:%s', node_dvalue_dict)

    # key nodeId value DValue
    top_dvalue_list = OrderedDict()
    for node_key in common_top_nodes:
        top_dvalue_list[node_key] = node_dvalue_dict[node_key]
    top_dvalue_list = sorted(top_dvalue_list.items(), key=lambda top_node_dict: top_node_dict[1], reverse=True)
    process_logger.debug('[Top Node DValue List]:%s', top_dvalue_list)

    # 创建子图网络
    subgraph_net = nx.Graph()
    # 初始化准备工作，把top_node_dict第一个最大的点加入到cancer_result_network
    subgraph_net.add_node(top_dvalue_list[0][0])
    process_logger.debug('[Add Node]:%s', top_dvalue_list[0][0])
    del top_dvalue_list[0]

    # 从最大的点开始查找
    for (top_node, dvalue_of_node) in top_dvalue_list:
        # 如果这个节点本来就在子网里面，那么直接跳过，进入下一个点。
        if top_node in nx.nodes(subgraph_net):
            continue

        process_logger.debug('----------[Select Node]: Top Node->%2s , DValue Of Node -> %s----------', top_node, dvalue_of_node)
        process_logger.debug('----------[Current Result Network Start]---------]')
        for path in nx.edges(subgraph_net):
            process_logger.debug('%s', path)
        process_logger.debug('----------[Current Result Network End]---------]')
        # 标志是否找到了直接连通的点
        founded = False
        for result_node in list(nx.nodes(subgraph_net)):
            # 在原来网络中查找node_key和result_node_key是否连通
            if util.is_direct_nodes(cancer_net, result_node, top_node):

                process_logger.debug('[Found Direct Node]: result_node -> %s , top_node -> %s is direct link!'
                              ,result_node, top_node)
                # 直接连通，那么就直接放在新的网络里面。并加入边
                subgraph_net.add_node(top_node)
                process_logger.debug('[Add Node]: %2s', top_node)

                subgraph_net.add_edge(top_node, result_node)
                process_logger.debug('[Add Edge]: %2s <---> %2s', top_node, result_node)
                founded = True
                break
        process_logger.debug('[Founded]: %s', founded)
        # 如果没有直接连通，那么找两个点之间的最短距离
        if not founded:
            process_logger.debug('[Start Find All Simple Path]...')
            # 对所有路经，calculate weight
            all_paths = []
            for target_length in range(2, len(cancer_net) + 1):
                process_logger.debug('[Try Simple Path]: Length -> %2d', target_length)
                # 对每一个点找到所有的路径，测试每一条路径的权重
                for result_node in list(nx.nodes(subgraph_net)):
                    process_logger.debug('[Try Node Of SubGraph Network]: node-> %2s', result_node)
                    paths = nx.all_simple_paths(cancer_net, top_node, result_node, target_length)
                    count = 0
                    for path in paths:
                        node_path = NodePath(path, subgraph_net, edge_weight_dict, node_dvalue_dict)
                        all_paths.append(node_path)
                        count= count + 1
                    process_logger.debug('[Find Path]: Number Of Founded Path -> %2d', count)

                if len(all_paths) == 0:
                    process_logger.debug('[Try Simple Path Length Bigger...]')
                    continue
                else:
                    process_logger.debug('[Path Founded! Skip Found Another Paths!]')
                    break

            # 把找到的路经加入result_network
            process_logger.debug('[Try Select Best Path]...')
            max_path = util.calculate_best_path(all_paths, dvalue_weight, edge_weight)
            process_logger.debug('[Best Path]:%s', max_path)
            #   1.先把点加入到result_network
            # print('add path to result network,path[' + str(max_path) + ']')
            for node in max_path:
                already_added = False
                # 判断是否已经添加过了
                for node_in_network in nx.nodes(subgraph_net):
                    if node == node_in_network:
                        process_logger.debug('[Skip Add Node]: Node -> %s already in result net', node)
                        already_added = True
                if not already_added:
                    process_logger.debug('[Add Node]: node -> %s', node)
                    subgraph_net.add_node(node)
            # 2.然后加边
            for i in range(len(max_path)):
                if i < len(max_path) - 1:
                    subgraph_net.add_edge(max_path[i], max_path[i + 1])
                    process_logger.debug('[Add Edge]: edge %s -> %s', max_path[i], max_path[i + 1])
    process_logger.info('[Calculation Done]...')
    with open(subgraph_network_path, 'w') as network, open(subgraph_node_path, 'w') as nodes:
        for edge in nx.edges(subgraph_net):
            network.write(edge[0] + '\t' + edge[1] + '\n')
        for node in nx.nodes(subgraph_net):
            nodes.write(node + '\n')
    process_logger.info('[Result Network]: size->%s', len(subgraph_net))



# 评价本次计算结果的好坏
def start_evaluate(important_node_path, subgraph_node_path):
    line10 = []
    im10 = []
    linenode = []
    result = 0
    with open(important_node_path, 'r') as f, open(subgraph_node_path, 'r') as node_result:
        im10 = list()
        imnode = list()
        for line10 in f.readlines():
            line10 = line10.strip('\n')
            im10.append(int(line10) - 1)
        for linenode in node_result.readlines():
            linenode = linenode.strip('\n')
            imnode.append(int(linenode))
            # print (set(im10).intersection(set(imnode)))
            # 输出匹配结果个数，最优结果为10
            # print (len(set(im10).intersection(set(imnode))))
            result = len(set(im10).intersection(set(imnode)))
    return result


if __name__ == '__main__':
    # 源数据路径前缀
    txt_path_base = '/Users/mhzhang/PycharmProjects/bio/data/rho_0.1_'
    for arg_dvalue in range(0, 101):
        dvalue_weight = round(arg_dvalue / 100, 2)
        edge_weight = round(1 - dvalue_weight, 2)
        print('[ARGS]: dvalue_weight->{0} edge_weight->{1}'.format(dvalue_weight, edge_weight))
        for index in range(1, 101):
            process_logger.info('[[[=================| %d |================]]]', index)

            # 拼接文件存储路径的前缀
            txt_path = txt_path_base + str(index)
            process_logger.info('[Read File Base Path]->%s', txt_path)
            # 需要读取的文件
            network1_path = os.path.join(txt_path, 'weighted_network1.txt')
            network2_path = os.path.join(txt_path, 'weighted_network2.txt')
            dvalue_path = os.path.join(txt_path, 'graphlet_dvalue.txt')
            important_node_path = os.path.join(txt_path, 'important.txt')

            # 需要输出的文件1
            subgraph_network_path = os.path.join(txt_path, 'subgraph_test1.txt')
            subgraph_node_path = os.path.join(txt_path, 'nodes_test1.txt')

            # 需要输出的文件2
            subgraph2_network_path = os.path.join(txt_path, 'subgraph_test2.txt')
            subgraph2_node_path = os.path.join(txt_path, 'nodes_test2.txt')

            # 读取重要的点
            common_top_nodes = util.prepare_top_nodes(dvalue_path, 0.30, 13)

            # 开始计算1
            start_calculate(network1_path, dvalue_path, subgraph_network_path, subgraph_node_path, common_top_nodes, dvalue_weight,
                            edge_weight)
            # 评估计算结果1
            current_score = start_evaluate(important_node_path, subgraph_node_path)
            # if current_score < 6:
            #     break
            process_logger.info('[network1 current_score:]' + str(current_score) + ',unit:' + str(index) + ',args:' + str(dvalue_weight) + ' ' + str(
                edge_weight))

            # 开始计算 network2
            start_calculate(network2_path, dvalue_path, subgraph2_network_path, subgraph2_node_path, common_top_nodes, dvalue_weight,
                            edge_weight)
            # 评估计算结果2
            current_score = start_evaluate(important_node_path, subgraph2_node_path)

            # if current_score < 6:
            #     break
            process_logger.info('[network2 current_score:]' + str(current_score) + ',unit:' + str(index) + ',args:' + str(dvalue_weight) + ' ' + str(
                edge_weight))
        # 评估本次结果
        count, sub_net_nodes = kds.cal_result()
        result_logger.info('%s %s %s %s', dvalue_weight, edge_weight, count,sub_net_nodes)