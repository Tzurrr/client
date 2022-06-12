import redis
import os
import requests
import elogger
import time
import urllib

def send(filepath: str, *args):
    local_redis = redis.Redis()

    try:
        get_val = local_redis.get(f"{os.path.splitext(filepath)[0][:-2]}")
    except Exception:
        os.remove(filepath)
        pass
    
    arr = [("files", open(get_val, "rb")), ("files", open(filepath, "rb"))]
    resp = requests.post(url="http://127.0.0.1:80/", files=arr)
    if str(resp.json) == "<bound method Response.json of <Response [200]>>":
        elogger.write_logs_to_elastic("sent")
        os.remove(get_val)
        os.remove(filepath)
        print(resp.json)
    else:
        elogger.write_logs_to_elastic("didntsent")
        os.remove(get_val)
        os.remove(filepath)
        print(resp.json)
