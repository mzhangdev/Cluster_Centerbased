'''
    This k-means++ algorithm refers to David Arthur and Sergei Vassilvitskii's paper:
    http://ilpubs.stanford.edu:8090/778/1/2006-13.pdf
'''

import clustering
import numpy
import random


class ClusteringImp(clustering.Clustering):
    #  k-means++ algorithm implementation

    def __init__(self, clustering_data, attribute_set, label, k):
        super().__init__(clustering_data, attribute_set, label, k)
        self.init_centers()
        self.n = len(self.clustering_data)
        self.iterations = 0
        return

    def init_centers(self, clusters, clustering_data):
        # Take one center c1, chosen uniformly at random from dataSet
        if self.k > 0 and self.clustering_data:
            self.clusters[0].center = self.clustering_data[random.randint(0, self.n - 1)].get_all_values()

        # Take c2 .. ck, from dataSet with probability
        for i in (1, self.k):
            # min_dists is the distance of each example (or record) to the nearest taken center
            min_dists = [0] * self.n
            for j, example in enumerate(self.clustering_data):
                min_dist = min([numpy.linalg.norm(self.clusters[j].center - example) for j in range(i)])
                min_dists[j] = min_dist
            # gen a random number: rand_num, then select a new center with probability
            rand_num = random.random()
            sum_dists = sum(min_dists)
            accum_pro = 0
            for j in range(self.n):
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
                cand_ind, cand_dist = 0, numpy.linalg.norm(self.clusters[0].center - example)
                for j, cluster in enumerate(self.clusters[1:], 1):
                    cur_dist = numpy.linalg.norm(cluster.center - example)
                    if cur_dist < cand_dist:
                        cand_ind, cand_dist = j, cur_dist
                self.clusters[cand_ind].append(i)
            # cal the new center for each cluster
            tmp_clusters = [clustering.Cluster(self.clustering_data)] * k
            for i, cluster in enumerate(tmp_clusters):
                tmp_cluster[i].center = np.mean([self.clustering_data[e].get_all_values() for e in cluster.get_examples_index()], axis=0)
            # loop until no longer changes
            if all([a.center == b.center for a, b in zip(self.clusters, tmp_clusters)]):
                break
            else:
                self.clusters = tmp_clusters
                self.iterations += 1

        return self.clusters
