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

        self.do_clustering()
        return

    def do_clustering(self):
        return

    def test(self, label):
        return 0.0

    def dump(self):
        return ""
