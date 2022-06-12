import json
def parse():
    filename = "/home/tzur/client/config.json"
    conf_dict = json.load(open(filename, "r"))
    return conf_dict
