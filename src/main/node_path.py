import networkx as nx


class NodePath:
    # path length
    length = 0
    # dvalue of path
    dvalue = 0.0
    # number of nodes exists in the result network
    num_of_res_net = 0
    # sum of edge weight
    edge_weight = 0.0
    # path
    path = []
    # result network
    result_net = None
    # 原始网络的边权重
    edge_weight_map = None
    # node_value
    node_value = None

    def __init__(self, path, result_net, edge_weight_map, node_dvalue):
        self.path = path
        self.result_net = result_net
        self.edge_weight_map = edge_weight_map
        self.node_value = node_dvalue

        self.length = len(path)
        self.calculate_dvalue()
        self.calculate_num_of_res_net()
        self.calculate_edge_weight()

    # calculate dvalue of current path
    def calculate_dvalue(self):
        sum_weight = 0.0
        # 查找DValue
        for node_in_path in self.path:
            if str(node_in_path) in self.node_value:
                sum_weight += float(self.node_value[str(node_in_path)])
        self.dvalue = sum_weight

    # calculate number of nodes exists in the result network
    def calculate_num_of_res_net(self):
        for node in nx.nodes(self.result_net):
            for tempNode in self.path:
                if node == tempNode:
                    self.num_of_res_net = self.num_of_res_net + 1

    def calculate_edge_weight(self):
        if len(self.path) <= 2:
            smaller_node = min(int(self.path[0]), int(self.path[1]))
            bigger_node = max(int(self.path[0]), int(self.path[1]))
            map_key = str(smaller_node) + '#' + str(bigger_node)
            weight_of_edge = self.edge_weight_map[map_key]
            self.edge_weight += weight_of_edge
        else:
            for index in range(len(self.path) - 1):
                smaller_node = min(int(self.path[index]), int(self.path[index + 1]))
                bigger_node = max(int(self.path[index]), int(self.path[index + 1]))
                map_key = str(smaller_node) + '#' + str(bigger_node)
                weight_of_edge = self.edge_weight_map[map_key]
                self.edge_weight += weight_of_edge

    # weight for this path
    # return
    def weight(self):
        # TODO
        return self.dvalue - 10000 * self.num_of_res_net

    def __str__(self):
        return "[Node Path]: path-> {0},dvalue->{1},edge_weight->{2}".format(self.path,self.dvalue,self.edge_weight)