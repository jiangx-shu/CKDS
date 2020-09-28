from collections import OrderedDict
import networkx as nx
import src.util.logger as logger

process_logger = logger.logger('PROCESS')
# 判断是否直接连通
def is_direct_nodes(net, node1, node2):
    for node in net.neighbors(node1):
        if node == node2:
            return True
    return False

# find base path among allNodePath
def calculate_best_path(all_node_path, dvalue_weight, edge_weight):
    process_logger.debug('[Try To Find Best Path]')
    max_weight = 0.0
    best_path = []
    for node_path in all_node_path:
        process_logger.debug('[Candidate Path]: %s ', node_path)
        current = dvalue_weight * node_path.dvalue + edge_weight * node_path.edge_weight
        process_logger.debug('[Current Weight]:%s', current)
        if current > max_weight:
            best_path = node_path.path
            max_weight = current
        process_logger.debug('[Max Weight]:%s', max_weight)
    process_logger.debug('[Best Path]:%s', best_path)
    return best_path

def prepare_top_nodes(dvalue_path, min_dvalue, top_num_dvalue):
    common_top_nodes = []
    temp_dvalue = OrderedDict()
    sorted_dvalue = OrderedDict()
    with open(dvalue_path, 'r') as file:
        for line in file:
            arr = line.split('\t')
            temp_dvalue[arr[0]] = float(arr[1])
        sorted_dvalue = sorted(temp_dvalue.items(), key=lambda temp_dvalue: temp_dvalue[1], reverse=True)
        #按d-value的值选定数值排序
        # for key, value in sorted_dvalue:
        #     if value > min_dvalue:
        #         common_top_nodes.append(key)
        #         print('top node:' + str(value))
        #取前x个数据
        for i in range(0, top_num_dvalue):
            # common_top_nodes.append(sorted_dvalue[i][0])
            if sorted_dvalue[i][1]>min_dvalue:
                common_top_nodes.append(sorted_dvalue[i][0])
    return common_top_nodes


# 写入network的边信息
def write_network_edges(file_path, network):
    with open(file_path, 'w') as write_file:
        for edge in nx.edges(network):
            write_file.write(str(edge[0]) + '\t' + str(edge[1]) + '\n')

# 写入network的节点信息
def write_network_nodes(file_path, network):
    with open(file_path, 'w') as write_file:
        for node in nx.nodes(network):
            write_file.write(str(node) + '\n')