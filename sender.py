import redis
import os
import requests
import elogger
import time
import urllib
import json_parser

def send_files_to_server(filepath: str, *args):
    local_redis = redis.Redis()

    conf_dict = json_parser.parse_json_to_var("/home/tzur/client/config.json")
    url_path = conf_dict["HAProxys_url"]

    try:
        get_val = local_redis.get(f"{os.path.splitext(filepath)[0][:-2]}")
    except Exception:
        os.remove(filepath)
        pass
    
    arr = [("files", open(get_val, "rb")), ("files", open(filepath, "rb"))]
    resp = requests.post(url=url_path, files=arr)
    if resp.status_code == 200:
        elogger.write_logs_to_elastic("sent")
    else:
        elogger.write_logs_to_elastic("didntsent")
        try:
            os.remove(get_val)
            os.remove(filepath)
        except Exception:
            pass
