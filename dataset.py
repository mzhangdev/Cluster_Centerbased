import re
import sys

import numpy


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
            if attr.values[0] == "unused":
                continue
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
