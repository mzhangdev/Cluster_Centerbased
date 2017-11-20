import attributes


class Cluster(object):
    # Represents a cluster

    def __init__(self, clustering_data):
        self.clustering_data = clustering_data
        self.examples_index = []
        self.center = clustering_data[0]
        return

    def set_center(self, center):
        self.center = center

    def get_center(self):
        return self.center

    def append(self, index):
        assert isinstance(index, int), "Not an index"
        self.examples_index.append(index)

    def get_examples_index(self):
        return self.examples_index

    def get_examples(self):
        examples = []
        for index in self.examples_index:
            examples.append(self.clustering_data[index])
        return examples

    def clean_up(self):
        self.examples_index = []
        self.center = None


class Clustering(object):
    # Represents a clustering algorithm

    def __init__(self, clustering_data, attribute_set, label, k):
        self.clustering_data = clustering_data
        self.attribute_set = attribute_set
        self.label = label
        self.k = k
        self.clusters = [Cluster(clustering_data) for _ in range(k)]

        #self.do_clustering()
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

        return sum([edge_matrix_self[i][j] != edge_matrix_ref[i][j] for i in range(n) for j in range(i + 1, n)]) / float(n * (n - 1) / 2)

    def dump(self):
        print("Clustering result: ")
        for i, cluster in enumerate(self.clusters):
            print(cluster.get_examples_index())
        print("Hamming distance to ref: ")
        print(self.get_hamming_distance())
        return ""
