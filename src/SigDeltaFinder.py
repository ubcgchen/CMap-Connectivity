import json
import Tools


# Group raw signature data obtained from CMap by drug name
def group_raw_sig_data():
    sig_data = load_sig_data()
    grouped_signatures = {}
    for sig_group in sig_data:
        for sig in sig_group:
            key = sig["pert_iname"]
            sig_to_add = sig
            add_sig(grouped_signatures, key, sig_to_add)
    find_diff_doses(grouped_signatures)


# Load raw signature data
def load_sig_data():
    path_sig = '../data/cmap_sig_data.json'
    file_sig = open(path_sig)
    sig_data = json.load(file_sig)
    return sig_data


# Finds drugs evaluated at different doses for a given pert plate/incubation time/dose and writes them to files
def find_diff_doses(grouped_data):
    for drug_name, drug_sig_data in grouped_data.items():
        processed_data = {}
        for sig in drug_sig_data:
            key = sig["brew_prefix"][0]
            sig_to_add = {"dose": sig["pert_idose"], "down": sig["dn50_lm"], "up": sig["up50_lm"]}
            add_sig(processed_data, key, sig_to_add)
        remove_non_diff_doses(processed_data)
        if processed_data:
            path = '../data/delta_signatures/' + drug_name + '.json'
            Tools.write_file(processed_data, path)


def remove_non_diff_doses(processed_data):
    for condition, sig_data in list(processed_data.items()):
        if not exists_unique(sig_data):
            del processed_data[condition]


# Add a signature to the dictionary based on if the key is already in the dictionary
def add_sig(dictionary, key, sig_to_add):
    if key not in dictionary:
        dictionary[key] = [sig_to_add]
    else:
        dictionary[key] += [sig_to_add]


def exists_unique(sig_data):
    unique_doses = []
    for sig_1 in sig_data:
        if sig_1["dose"] not in unique_doses and len(unique_doses) == 0:
            unique_doses.append(sig_1["dose"])
        elif sig_1["dose"] not in unique_doses:
            return True
    return False


Tools.clear_folder('../data/delta_signatures/')
group_raw_sig_data()
