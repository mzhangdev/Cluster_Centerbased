# Cluster_Centerbased
Course Project - centerbased clustering, comparing K-meaning++ &amp; PAM 
https://docs.google.com/document/d/1BWXlfbSS0L61Ol_yEr6U4f2jf0Azgfum0JxHl840PVk/edit

###  Main code structure and functions:
- ./datasets/*: store the datasets those are to test. Each dataset should consist of the csv data file, and the attributes file, which is required by the code to process the data.

- attributes.py: Including “Attributes class” and “Attribute class”
“Attributes class” represents a set of attributes.
“Attribute class” represent an attribute.

- clustering.py: Including “Clustering class” and “Cluster class”
“Clustering class” is an interface for clustering algorithms.
“Cluster class” represents a cluster used by clustering algorithms.

- dataset.py: Including “Dataset class” and “Example class”
“Dataset class” represents a dataset with loading data from files function.
“Example class” represents an instance.

- evaluation.py: Containing “hamming_distance” and “classification_error_distance” functions for evaluating the correctness of clustering algorithms.

- util.py: Containing “normalize” function which is used by clustering algorithms.

- k-means++.py: Including the implementation of  k-means++ clustering algorithm.

- k-medois.py: Including the implementation of k-medoids clustering algorithm.

- main.py: A script for parsing arguments and coordinating all classes. 

- runner.py: A script for running experiments repeatedly, collecting and formatting outputs


### Environment requirements:
- Python 3.6.3
- Numpy 1.13.3


### Usage: 
In the terminal, enter the project folder, run

#### Do clustering of certain algorithm once:
take the wine dataset for example:
```
python3 ./main.py k-means++ 0 class --attributes datasets/wine-attributes.txt --train datasets/wine-data.csv --normalize n
```

#### Do the repeated experiments:
```
python3 ./runner.py
```
Then, enter the number of times you want to do the clustering.
