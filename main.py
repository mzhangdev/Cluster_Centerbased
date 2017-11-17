#!/usr/bin/python

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
                     args.classifier)
    sys.exit(1)
label = all_attributes[args.label]

# Import the clustering module
clustering_pkg = __import__(args.clustering_module)

# Clustering
clustering_data = dataset.DataSet(args.training_file, all_attributes)
effective_attrs = copy.copy(all_attributes)
effective_attrs.remove(label)
Clustering = clustering_pkg.Clustering(clustering_data, effective_attrs, label)
print Clustering.dump()

"""
if args.testing_file:
  testing_data = dataset.DataSet(args.testing_file, all_attributes)
  correct_results = dtree.test(classifier, testing_data)
  print("%d of %d (%.2f%%) of testing examples correctly identified" %
        (correct_results, len(testing_data),
         (float(correct_results) * 100.0)/ float(len(testing_data))))
"""
