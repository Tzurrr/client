import json

def parse_json_to_var(json_filename):
    try:
        with open(json_filename, "r") as log_file:
            log_json = json.load(log_file)
            return log_json            
    except Exception:
        pass

