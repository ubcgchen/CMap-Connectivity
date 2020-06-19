import json
import requests
import config
import Tools


def get_signature_data():
    link = "https://api.clue.io/api/"
    key = "&user_key=" + config.api_key
    pert_data = process_cell_pert_data()
    all_requests = build_requests(link, pert_data, key)

    cmap_data = handle_requests(all_requests)

    Tools.write_file(cmap_data, '../data/cmap_sig_data.json')
    # write_file(cmap_data)


def process_cell_pert_data():
    path_pert = '../data/cmap_immunosuppressive_data.json'
    path_cell = '../data/cmap_immune_cell_data.json'
    file_pert = open(path_pert)
    file_cell = open(path_cell)
    cell_data = set(json.load(file_cell)["immune_cell_inames"])

    pert_json_data = json.load(file_pert)
    pert_data = json_to_list(pert_json_data)
    pert_data = filter_by_assayed_cells(cell_data, pert_data)

    return pert_data


def filter_by_assayed_cells(cell_data, pert_data):
    for pert in pert_data:
        x = 0
        while x < len(pert["cell_id"]):
            if pert["cell_id"][x] not in cell_data:
                pert["cell_id"].remove(pert["cell_id"][x])
                x -= 1
            x += 1
    pert_data = [data for data in pert_data if data["cell_id"] != []]
    return pert_data


def json_to_list(pert_json_data):
    pert_data = []
    for pert in pert_json_data:
        pert_data.append({"pert_iname": pert[0]["pert_iname"], "cell_id": pert[0]["cell_id"]})
    return pert_data


def build_requests(link, pert_data, key):
    all_requests = []
    for pert in pert_data:
        for cell in pert["cell_id"]:
            all_requests.append(link + "sigs" + "?filter={\"where\":{\"pert_iname\":\"" + pert["pert_iname"] +
                                "\",\"cell_id\":\"" + cell + "\"}}" + key)
    return all_requests


def handle_requests(all_requests):
    cmap_data = []
    for request in all_requests:
        request_result = requests.get(request)
        request_result = request_result.json()
        if request_result:
            cmap_data.append(request_result)
    return cmap_data


# def write_file(cmap_data):
#     file_path = '../data/cmap_sig_data.json'
#     with open(file_path, 'w') as outfile:
#         outfile.write(json.dumps(cmap_data, indent=4, sort_keys=True))


get_signature_data()
