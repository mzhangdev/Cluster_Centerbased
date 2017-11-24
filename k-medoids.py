import clustering

from util import normalize


class ClusteringImp(clustering.Clustering):
    # k-medoids algorithm implementation

    def __init__(self, clustering_data, attribute_set, label, k):
        normalize(clustering_data, attribute_set)
        super().__init__(clustering_data, attribute_set, label, k)
        return

    def do_clustering(self):
        return
