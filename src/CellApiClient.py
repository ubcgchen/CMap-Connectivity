import requests
import Tools
import config

API_key = config.api_key


def get_immune_cell_data():
    cell_lineage = "haematopoietic_and_lymphoid_tissue"
    cell_request_results = handle_request(cell_lineage)
    cell_names = parse_cell_names(cell_request_results)
    Tools.write_file(cell_names, '../data/cmap_immune_cell_data.json')


def handle_request(cell_lineage):
    request = "https://api.clue.io/api/cells?filter={%22fields%22:[%22cell_iname%22]," \
              "%22where%22:{%22cell_lineage%22:%22" + cell_lineage + "%22}}" \
              "&user_key=" + API_key
    cell_request_results = requests.get(request)
    cell_request_results = cell_request_results.json()
    return cell_request_results


def parse_cell_names(cell_request_results):
    cell_names = {'immune_cell_inames': []}
    for request_result in cell_request_results:
        cell_names['immune_cell_inames'].append(request_result['cell_iname'])
    return cell_names


get_immune_cell_data()
