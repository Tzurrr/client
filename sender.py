import redis
import os
import requests
import elogger
import time
import urllib
import json_parser

def send_files_to_server(filepath: str, *args):
    local_redis = redis.Redis()
    arr = []

    conf_dict = json_parser.parse_json_to_var("/home/tzur/client/config.json")
    url_path = conf_dict["HAProxys_url"]
    get_val = local_redis.get(f"{os.path.splitext(filepath)[0][:-2]}")
    if get_val == None:
        pass
    
    if os.path.splitext(get_val)[0][:-1] == "a":
        arr = [("files", open(get_val, "rb")), ("files", open(filepath, "rb"))]
    elif os.path.splitext(get_val)[0][:-1] == "b":
        arr = [("files", open(file_path, "rb")), ("files", open(get_val, "rb"))]

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
