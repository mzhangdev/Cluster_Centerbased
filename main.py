import argparse
import copy
import sys

import attributes
import dataset

parser = argparse.ArgumentParser(
                    description='Clustering a dataset')
parser.add_argument('clustering_module',
                    metavar='clustering-module',
                    help='clustering module name')
parser.add_argument('number_of_target_clusters',
                    type=int,
                    help='Number of target clusters')
parser.add_argument('label',
                    help='Name of the attribute to use for verification')
parser.add_argument('--attributes',
                    type=argparse.FileType('r'),
                    help='Name of the attribute specification file',
                    dest='attributes_file',
                    required=True)
parser.add_argument('--train',
                    type=argparse.FileType('r'),
                    help='Name of the file to use for clustering',
                    dest='training_file',
                    required=True)

args = parser.parse_args()

# Read in a complete list of attributes.
# global all_attributes
all_attributes = attributes.Attributes(args.attributes_file)
if args.label not in all_attributes.all_names():
    sys.stderr.write("label '%s' not a recognized attribute name\n" %
                     args.label)
    sys.exit(1)
label = all_attributes[args.label]
k = args.number_of_target_clusters
if k == 0:
    k = len(label.values)

# Import the clustering module
clustering_pkg = __import__(args.clustering_module)

# Clustering
clustering_data = dataset.DataSet(args.training_file, all_attributes)
effective_attrs = copy.copy(all_attributes)
effective_attrs.remove(label)

clustering = clustering_pkg.Clustering_imp(clustering_data, effective_attrs, label, k)
print(clustering.dump())

classified_err = clustering.test(label)
print("Classification Error %f" % classified_err)
