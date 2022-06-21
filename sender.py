import redis
import os
import requests
import elogger
import json_parser
import sys
import local_logger


def send_files_to_server(filepath: str):
    filename_from_redis = get_file_from_redis(filepath)
    if filename_from_redis is None or filepath is None or filename_from_redis == filepath:
        return

    arr = build_file_array(filename_from_redis, filepath)
    send_to_server(arr, filename_from_redis, filepath)


def get_file_from_redis(filepath):
    local_redis = redis.Redis()
    filename_clean = os.path.splitext(filepath)[0][:-2]
    filename_from_redis = local_redis.get(filename_clean).decode()
    return filename_from_redis


def send_to_server(arr, filename_from_redis, filepath):
    conf_dict = json_parser.parse_json_to_var("./config.json")
    url_path = conf_dict["HAProxys_url"]
    resp = requests.post(url=url_path, files=arr)
    if resp.status_code == 200:
        elogger.write_logs_to_elastic("sent")
    else:
        elogger.write_logs_to_elastic("didntsent")
    remove_file_safely(filename_from_redis)
    remove_file_safely(filepath)


def build_file_array(filename_from_redis, filepath):
    filepath_ending = os.path.splitext(filepath)[0][-1]
    if filepath_ending == "a":
        arr = [("files", open(filepath, "rb")), ("files", open(filename_from_redis, "rb"))]
    elif filepath_ending == "b":
        arr = [("files", open(filename_from_redis, "rb")), ("files", open(filepath, "rb"))]
    return arr

def remove_file_safely(filename):
    try:
        os.remove(filename)
    except:
        local_logger.log_to_local_file("no such file")
