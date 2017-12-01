import copy
import queue
import attributes


def hamming_distance(clustering_data, clusters, label, k):
    n = len(clustering_data)
    # edge matrix: 1 - in-cluster edge, 0 - between-cluster edge, only use the upper triangle
    edge_matrix_self = [[0] * n for i in range(n)]
    edge_matrix_ref = [[0] * n for i in range(n)]
    # get the edge matrix of the clustering generated
    for i in range(k):
        all_examples_inds = clusters[i].get_examples_index()
        for j, ind_a in enumerate(all_examples_inds):
            for ind_b in all_examples_inds[j + 1:]:
                edge_matrix_self[ind_a][ind_b] = 1
    # get the edge matrix of the clustering of classified label
    table = {}
    for i, example in enumerate(clustering_data):
        cluster_id = example.get_value(label)
        if cluster_id in table:
            table[cluster_id] += [i]
        else:
            table[cluster_id] = [i]
    for key in table:
        all_examples_inds = table[key]
        for j, ind_a in enumerate(all_examples_inds):
            for ind_b in all_examples_inds[j + 1:]:
                edge_matrix_ref[ind_a][ind_b] = 1

    return sum([edge_matrix_self[i][j] != edge_matrix_ref[i][j] for i in range(n) for j in range(i + 1, n)]) / float(
        n * (n - 1) / 2)


def classification_error_distance(clusters_stat, label, total=None):
    if isinstance(label, attributes.Attribute):
        label = label.values

    if total is None:
        total = 0
        for stat in clusters_stat:
            for name in label:
                total = total + stat[name]

    best_match = 0

    # BFS version
    class Node:
        def __init__(self, _clusters_stat, _label, match):
            self.clusters_stat = _clusters_stat
            self.label = _label
            self.match = match

    q = queue.Queue()
    q.put(Node(clusters_stat, label, 0))

    while not q.empty():
        node = q.get()
        c_stat = node.clusters_stat[0]
        if len(node.label) == 1:
            value = node.label[0]
            best_match = max(best_match, node.match + c_stat[value])
        else:
            for l_idx, value in enumerate(node.label):
                next_clusters_stat = copy.copy(node.clusters_stat)
                next_clusters_stat.pop(0)
                next_label_stat = copy.copy(node.label)
                next_label_stat.pop(l_idx)
                q.put(Node(next_clusters_stat, next_label_stat, node.match + c_stat[value]))

    d_ce = (total - best_match) / total
    return d_ce
