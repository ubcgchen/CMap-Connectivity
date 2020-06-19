import json
import itertools
import os

import Tools
from matplotlib import pyplot

from upsetplot import plot
import numpy as np
import pandas as pd


def traverse_delta_sigs():
    sig_directory = '../data/delta_signatures'
    data_directory = '../data/delta_data'
    Tools.clear_folder(data_directory)

    for filename in os.listdir(sig_directory):
        drug_data, drug_name = retrieve_file_data(filename, sig_directory)
        raw_data_storage_path = os.path.join(data_directory, drug_name, "raw_data")
        graph_storage_path = os.path.join(data_directory, drug_name, "plots")
        os.makedirs(raw_data_storage_path)
        os.makedirs(graph_storage_path)
        traverse_conditions(drug_data, raw_data_storage_path, graph_storage_path)


def retrieve_file_data(filename, sig_directory):
    drug_name = os.path.splitext(filename)[0]
    path = os.path.join(sig_directory, filename)
    file = open(path)
    drug_data = json.load(file)
    return drug_data, drug_name


def build_diagrams(consolidated_data, graph_storage_path, condition):
    dn_list, doses_list, up_list = unpack_consolidated_data(consolidated_data)
    index = build_graph_index(doses_list)
    data_lists = [dn_list, up_list]
    for pos in range(0, 2):
        ser = build_graph_data(data_lists[pos], index)
        plot(ser)
        if pos is 0:
            pyplot.savefig(os.path.join(graph_storage_path, condition + '_down_' + '.png'))
        else:
            pyplot.savefig(os.path.join(graph_storage_path, condition + '_up_' + '.png'))


def unpack_consolidated_data(consolidated_data):
    doses_list = []
    up_list = []
    dn_list = []
    for data in consolidated_data:
        doses_list.append(data['dose'])
        up_list.append(data['up'])
        dn_list.append(data['down'])
    return dn_list, doses_list, up_list


def build_graph_data(data_list, index):
    data = np.array([])
    for component in data_list:
        data = np.append(data, len(component))
    ser = pd.Series(data, index=index)
    return ser


def build_graph_index(doses_list):
    doses = doses_list[0]
    index_arrays = []
    for dose in doses:
        index_partial = []
        for doses_rest in doses_list:
            index_partial.append(dose in doses_rest)
        index_arrays.append(index_partial)
    tuples = list(zip(*index_arrays))
    index = pd.MultiIndex.from_tuples(tuples, names=doses)
    return index


def traverse_conditions(drug_data, raw_data_storage_path, graph_storage_path):
    for condition, dose_signatures in drug_data.items():
        dose = []
        dose_tuples = []
        up = []
        up_tuples = []
        dn = []
        dn_tuples = []
        parse_sig_data(dn, dose, dose_signatures, up)

        build_sig_subsets(dn, dn_tuples, dose, dose_tuples, up, up_tuples)
        dn_intersections = build_subset_intersections(dn_tuples)
        up_intersections = build_subset_intersections(up_tuples)
        consolidated_data = build_data(dn_intersections, dose_tuples, up_intersections)
        build_diagrams(consolidated_data, graph_storage_path, condition)
        Tools.write_file(consolidated_data, raw_data_storage_path + "/" + condition + ".json")


def build_data(dn_intersections, dose_tuples, up_intersections):
    consolidated_data = []
    concatenate_data(consolidated_data, dn_intersections, dose_tuples, up_intersections)
    remove_overlapping_data(consolidated_data, dose_tuples)
    return consolidated_data


def remove_overlapping_data(consolidated_data, dose_tuples):
    for index in range(len(dose_tuples) - 1, 0, -1):
        for L1 in range(index - 1, -1, -1):
            if set(consolidated_data[index]['dose']).issubset(set(consolidated_data[L1]['dose'])):
                consolidated_data[index]['up'] = list(
                    set(consolidated_data[index]['up']) - set(consolidated_data[L1]['up']))
                consolidated_data[index]['down'] = list(
                    set(consolidated_data[index]['down']) - set(consolidated_data[L1]['down']))


def concatenate_data(consolidated_data, dn_intersections, dose_tuples, up_intersections):
    for index in range(0, len(dose_tuples)):
        consolidated_data.append(
            {"dose": dose_tuples[index], "up": up_intersections[index], "down": dn_intersections[index]})


def build_subset_intersections(tuples):
    intersections = []
    for subset in tuples:
        temp_intersection = subset[0]
        for next_list in subset:
            temp_intersection = list(set(temp_intersection) & set(next_list))
        intersections.append(temp_intersection)
    return intersections


def build_sig_subsets(dn, dn_tuples, dose, dose_tuples, up, up_tuples):
    for index in range(len(up), 0, -1):
        get_subset(index, up, up_tuples)
        get_subset(index, dn, dn_tuples)
        for subset in itertools.combinations(dose, index):
            subset = list(subset)
            dose_tuples.append(subset)


def get_subset(index, data, tuples):
    for subset in itertools.combinations(data, index):
        tuples.append(subset)


def parse_sig_data(dn, dose, dose_signatures, up):
    for dose_signature in dose_signatures:
        if dose_signature["dose"] in dose:
            break
        dose.append(dose_signature["dose"])
        up.append(dose_signature["up"])
        dn.append(dose_signature["down"])


traverse_delta_sigs()
