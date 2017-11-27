import numpy


def normalize(dataset, attributes):
    min_values = dataset[0].get_all_values()
    max_values = dataset[0].get_all_values()
    for example in dataset:
        min_values = numpy.minimum(min_values, example.get_all_values())
        max_values = numpy.maximum(max_values, example.get_all_values())

    range_array = max_values - min_values
    for example in dataset:
        original_values = example.get_all_values()
        normalized_values = (original_values - min_values) / range_array
        example.set_all_values(normalized_values, attributes)

