import clustering
import numpy
import random

from util import normalize


class ClusteringImp(clustering.Clustering):
    # k-medoids algorithm implementation

    def __init__(self, clustering_data, attribute_set, label, k, to_normalize):
        super().__init__(clustering_data, attribute_set, label, k)
        if to_normalize:
            normalize(self.clustering_data, self.attribute_set)
        self.dist_matrix = numpy.zeros(shape=(len(self.clustering_data), len(self.clustering_data)))
        self.dist_between_examples()

        self.do_clustering()
        return

    def dist_between_examples(self):
        for i in range(0, len(self.clustering_data)):
            for j in range(i + 1, len(self.clustering_data)):
                self.dist_matrix[i][j] = numpy.linalg.norm(self.clustering_data[i].get_all_values() -
                                                           self.clustering_data[j].get_all_values())
                self.dist_matrix[j][i] = self.dist_matrix[i][j]

    def init_centers(self):
        #for idx, cluster in enumerate(self.clusters):
            #cluster.center = int(len(self.clustering_data) / len(self.clusters) * (idx + 1) - 1)
        all_centers = {}
        random.seed()
        for cluster in self.clusters:
            while True:
                center = random.randint(0, len(self.clustering_data) - 1)
                if all_centers.get(center, True):
                    cluster.set_center(center)
                    all_centers[center] = False
                    break

    def group_by_centers(self):
        for idx in range(0, len(self.clustering_data)):
            min_dist = self.dist_matrix.max()
            group = None
            dist_array = self.dist_matrix[idx]
            for cluster in self.clusters:
                dist = dist_array[cluster.get_center()]
                if min_dist > dist:
                    min_dist = dist
                    group = cluster
            assert group is not None, "group cannot be None"
            group.append(idx)

    def distance_sum(self, cluster):
        cost = 0
        dist_array = self.dist_matrix[cluster.get_center()]
        for idx in cluster.get_examples_index():
            cost = cost + dist_array[idx]
        return cost

    def pick_new_center(self, cluster):
        center = cluster.get_center()
        dist_sum = self.distance_sum(cluster)
        for idx in cluster.get_examples_index():
            cluster.set_center(idx)
            new_dist_sum = self.distance_sum(cluster)
            if dist_sum > new_dist_sum:
                dist_sum = new_dist_sum
                center = idx
        return center

    def do_clustering(self, max_iter=150):
        self.init_centers()
        self.group_by_centers()
        all_centers = [cluster.get_center() for cluster in self.clusters]
        self.iterations = 0
        while True:
            for cluster in self.clusters:
                center = self.pick_new_center(cluster)
                cluster.clean_up()
                cluster.set_center(center)
            self.group_by_centers()
            new_all_centers = [cluster.get_center() for cluster in self.clusters]
            self.iterations = self.iterations + 1
            if (all_centers != new_all_centers) and (max_iter != self.iterations):
                all_centers = new_all_centers
            else:
                #print("k-medoids done in iter %d" % self.iterations)
                break
        return
