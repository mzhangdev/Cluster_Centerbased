'''
    This k-means++ algorithm refers to David Arthur and Sergei Vassilvitskii's paper:
    http://ilpubs.stanford.edu:8090/778/1/2006-13.pdf
'''

import clustering
import numpy
import random
from util import normalize


class ClusteringImp(clustering.Clustering):
    #  k-means++ algorithm implementation

    def __init__(self, clustering_data, attribute_set, label, k, to_normalize):
        super(ClusteringImp, self).__init__(clustering_data, attribute_set, label, k)
        if to_normalize:
            normalize(clustering_data, attribute_set)
        self.init_centers()
        self.do_clustering()
        return

    def init_centers(self):
        n = len(self.clustering_data)
        # Take one center c1, chosen uniformly at random from dataSet
        if self.k > 0 and self.clustering_data:
            self.clusters[0].center = self.clustering_data[random.randint(0, n - 1)].get_all_values()

        # Take c2 .. ck, from dataSet with probability
        for i in range(1, self.k):
            # min_dists is the distance^2 of each example (or record) to the nearest taken center
            min_dists = [0] * n
            for j, example in enumerate(self.clustering_data):
                min_dist = min([numpy.linalg.norm(self.clusters[l].center - example.get_all_values()) for l in range(i)])
                min_dists[j] = min_dist ** 2
            # gen a random number: rand_num, then select a new center with probability
            rand_num = random.random()
            sum_dists = sum(min_dists)
            accum_pro = 0
            for j in range(n):
                pro = min_dists[j] / sum_dists
                if accum_pro <= rand_num and accum_pro + pro > rand_num:
                    self.clusters[i].center = self.clustering_data[j].get_all_values()
                    break
                else:
                    accum_pro += pro

    def do_clustering(self):
        while True:
            # iterate through all the example (or record) in the dataset and append the example index to the nearest cluster
            for i, example in enumerate(self.clustering_data):
                cand_ind, cand_dist = 0, numpy.linalg.norm(self.clusters[0].center - example.get_all_values())
                for j, cluster in enumerate(self.clusters[1:], 1):
                    cur_dist = numpy.linalg.norm(cluster.center - example.get_all_values())
                    if cur_dist < cand_dist:
                        cand_ind, cand_dist = j, cur_dist
                self.clusters[cand_ind].append(i)
            # cal the new center for each cluster
            tmp_clusters = [clustering.Cluster(self.clustering_data) for _ in range(self.k)]
            for i, cluster in enumerate(self.clusters):
                tmp_clusters[i].center = numpy.mean([self.clustering_data[e].get_all_values() for e in cluster.get_examples_index()], axis=0)
            # loop until no longer changes
            if all([(a.center == b.center).all() for a, b in zip(self.clusters, tmp_clusters)]):
                break
            else:
                self.clusters = tmp_clusters
                self.iterations += 1

        return self.clusters
