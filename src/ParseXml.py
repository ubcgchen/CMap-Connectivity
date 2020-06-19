from lxml import etree

DRUG_BANK_PATH = "../files/full database.xml"
SAVE_PATH = "../data/immunosuppressives.json"
PREFIX = "{http://www.drugbank.ca}"
text_immunosuppressive = "Immunosuppressive Agents"
text_pubchem = "PubChem Compound"


def parse_xml():
    context = etree.iterparse(DRUG_BANK_PATH, tag=PREFIX + "drug")
    immunosuppressives = []

    # Iterate through every drug in the context
    for event, drug in context:
        if is_immunosuppressive(drug):
            cid = get_pubchem_id(drug)
            name = get_name(drug)
            json_text = {"name": name, "cid": cid}
            immunosuppressives.append(json_text)
        # Clear memory for the drug
        drug.clear()
        while drug.getprevious() is not None:
            del drug.getparent()[0]

    del context
    Tools.write_file(immunosuppressives, SAVE_PATH)
#     write_file(immunosuppressives)


# def write_file(immunosuppressives):
#     with open(SAVE_PATH, 'w') as outfile:
#         outfile.write(json.dumps(immunosuppressives, indent=4, sort_keys=True))


def get_name(drug):
    return drug.find(PREFIX + 'name').text


def is_immunosuppressive(drug):
    categories = drug.findall('*/' + PREFIX + 'category')

    # Check if the drug is an immunosuppressant
    for category in categories:
        if category[0].text == text_immunosuppressive:
            return True
    return False


def get_pubchem_id(drug):
    external_identifiers = drug.findall('*/' + PREFIX + 'external-identifier')

    # Check if the drug has a pubchem compound id (cid)
    for identifier in external_identifiers:
        if identifier[0].text == text_pubchem:
            return identifier[1].text
    return None


parse_xml()
