import attributes


class Clustering:
    # Represents a clustering algorithm

    def __init__(self, clustering_data, attribute_set, label):
        self.clustering_data = clustering_data
        self.attribute_set = attribute_set
        # self.attribute_set = attributes.Attributes(False, sorted(attribute_set, key = lambda attribute: attribute.name))
        self.label = label

        self.do_clustering()
        return

    def do_clustering(self):
        return

    def test(self, label):
        return 0.0

    def dump(self):
        return ""
