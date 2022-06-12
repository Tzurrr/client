import json

def json_to_var(json_filename):
    log_file = open(json_filename, "r")
    log_json = json.load(log_file)
    log_file.close()
    return log_json
