import json
import requests
import config
import Tools


def get_immunosuppressive_data():
    immunosuppressive_path = 'immunosuppressives.json'
    file = open(immunosuppressive_path)
    data = json.load(file)

    api_link = "https://api.clue.io/api/"
    conditions = build_conditions(data)
    api_key = "&user_key=" + config.api_key
    all_requests = build_requests(api_link, conditions, api_key)

    cmap_immunosuppressive_data = []
    for request in all_requests:
        request_result = requests.get(request)
        request_result = request_result.json()
        # Ignore empty results
        if request_result:
            cmap_immunosuppressive_data.append(request_result)

    Tools.write_file(cmap_immunosuppressive_data, '../data/cmap_immunosuppressive_data.json')
    # write_file(cmap_immunosuppressive_data)


def build_conditions(data):
    conditions = []

    # Iterate through all immunosuppressants and build conditions
    for immunosuppressant in data:
        if immunosuppressant['cid'] is not None:
            body = build_body_cid(immunosuppressant['cid'])
        else:
            body = build_body_name(immunosuppressant['name'])
        endpoint = "perts"
        conditions.append(endpoint + "?filter={" + body + "}")
    return conditions


def build_body_name(name):
    where_body = "\"pert_iname\":\"" + name + "\""
    return "\"where\":{" + where_body + "}"


def build_body_cid(cid):
    where_body = "\"pubchem_cid\":\"" + cid + "\""
    return "\"where\":{" + where_body + "}"


def build_requests(link, conditions, key):
    all_requests = []
    for condition in conditions:
        all_requests.append(link + condition + key)
    return all_requests


# def write_file(cmap_immunosuppressive_data):
#     file_path = 'cmap_immunosuppressive_data.json'
#     with open(file_path, 'w') as outfile:
#         outfile.write(json.dumps(cmap_immunosuppressive_data, indent=4, sort_keys=True))


get_immunosuppressive_data()
