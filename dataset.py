import re
import sys
import numpy


def normalize(dataset, attributes):
    min_array = dataset[0].get_all_values()
    max_array = dataset[0].get_all_values()
    for example in dataset:
        min_array = numpy.minimum(min_array, example.get_all_values())
        max_array = numpy.maximum(max_array, example.get_all_values())

    dif_array = max_array - min_array
    for example in dataset:
        original_array = example.get_all_values()
        normalize_data = (original_array - min_array) / dif_array
        example.set_all_values(normalize_data, attributes)
    return


class Example:
    # An individual example with values for each attribute

    def __init__(self, values, attributes, filename, line_num):
        if len(values) != len(attributes):
            sys.stderr.write(
                "%s: %d: Incorrect number of attributes (saw %d, expected %d)\n" %
                (filename, line_num, len(values), len(attributes)))
            sys.exit(1)
        # Add values, Verifying that they are in the known domains for each attribute
        self.values = {}
        values_array = []
        for ndx in range(len(attributes)):
            attr = attributes.attributes[ndx]
            if attr.values[0] != "numeric":
                value = values[ndx]
                if value not in attr.values:
                    sys.stderr.write(
                        "%s: %d: Value %s not in known values %s for attribute %s\n" %
                        (filename, line_num, value, attr.values, attr.name))
                    sys.exit(1)
            else:
                value = float(values[ndx])
                values_array.append(value)
            self.values[attr.name] = value
        self.np_array = numpy.array(values_array)

    # Find a value for the specified attribute, which may be specified as
    # an Attribute instance, or an attribute name.
    def get_value(self, attr):
        if isinstance(attr, str):
            return self.values[attr]
        else:
            return self.values[attr.name]

    def get_all_values(self):
        return self.np_array

    def set_all_values(self, values, attributes):
        assert len(values) == len(attributes), "Arguments' length are not equal."
        assert isinstance(values, list) or isinstance(values, numpy.ndarray), "Invalid argument"
        if isinstance(values, list):
            values = numpy.array(values)
        for ndx in range(len(values)):
            attr = attributes.attributes[ndx]
            self.values[attr.name] = values[ndx]
        self.np_array = values


class DataSet:
    # A collection of instances, each representing data and values

    def __init__(self, data_file=False, attributes=False, all_examples=False):
        self.all_examples = []
        if data_file:
            line_num = 1
            num_attrs = len(attributes)
            for next_line in data_file:
                next_line = next_line.rstrip()
                next_line = re.sub(".*:(.*)$", "\\1", next_line)
                attr_values = next_line.split(',')
                new_example = Example(attr_values, attributes, data_file.name, line_num)
                self.all_examples.append(new_example)
                line_num += 1

        if all_examples:
            self.all_examples = all_examples

    def __len__(self):
        return len(self.all_examples)

    def __getitem__(self, key):
        return self.all_examples[key]

    def append(self, example):
        self.all_examples.append(example)



"""
  def majority(self, classifier, is_root=False):
    classifier_name = classifier.name
    classifier_value_set = sorted(classifier.values)

    if len(self.all_examples) == 0:
      return None

    subset_sizes = []
    for value in classifier_value_set:
      subset_sizes.append(len([example for example in self.all_examples if example.get_value(classifier_name) == value]))

    max_subset_size = max(subset_sizes)
    if is_root == False and len([subset_size for subset_size in subset_sizes if subset_size == max_subset_size]) > 1:
        return None

    majority_index = subset_sizes.index(max_subset_size)
    value = classifier_value_set[majority_index]

    return value
"""
