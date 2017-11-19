import attributes


class Cluster:
    # Represents a cluster

    def __init__(self, clustering_data):
        self.clustering_data = clustering_data
        self.examples_index = []
        self.center = clustering_data[0]
        return

    def set_center(self, example):
        self.center = example

    def append(self, index):
        assert isinstance(index, int), "Not an index"
        self.examples_index.append(index)

    def get_examples_index(self):
        return self.examples_index

    def clean_up(self):
        self.examples_index = []
        self.center = None


class Clustering:
    # Represents a clustering algorithm

    def __init__(self, clustering_data, attribute_set, label, k):
        self.clustering_data = clustering_data
        self.attribute_set = attribute_set
        self.label = label
        self.k = k
        self.clusters = [clustering.Cluster(clustering_data)] * k

        self.do_clustering()
        return

    def do_clustering(self):
        return

    def test(self, label):
        return 0.0

    def get_hamming_distance(self):
        n = len(self.clustering_data)
        # edge matrix: 1 - in-cluster edge, 0 - between-cluster edge, only use the upper triangle
        edge_matrix_self = [[0] * n for i in range(n)]
        edge_matrix_ref = [[0] * n for i in range(n)]
        # get the edge matrix of the clustering generated
        for i in range(self.k):
            all_examples_inds = self.clusters[i].get_examples_index()
            for j, ind_a in enumerate(all_examples_inds):
                for ind_b in all_examples_inds[j + 1:]:
                    edge_matrix_self[ind_a][ind_b] = 1
        # get the edge matrix of the clustering of classified label
        table = {}
        for i in range(n):
            if self.label[i] in table:
                table[self.label[i]] += [i]
            else:
                table[self.label[i]] = [i]
        for key in table:
            all_examples_inds = table[key]
            for j, ind_a in enumerate(all_examples_inds):
                for ind_b in all_examples_inds[j + 1:]:
                    edge_matrix_ref[ind_a][ind_b] = 1

        return sum([edge_matrix_self[i][j] != edge_matrix_ref[i][j] for i in range(n) for j in range(n)]) / float(n * (n - 1) / 2)

    def dump(self):
        return ""
