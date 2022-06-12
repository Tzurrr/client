import json
import logging
import ecs_logging
import requests
import uuid
import os
import file_to_var

def write_logs_to_elastic(event_string):
    logger = logging.getLogger("app")
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler('/home/tzur/final-client/elvis.json')
    handler.setFormatter(ecs_logging.StdlibFormatter())
    logger.addHandler(handler)
    json_UUID = uuid.uuid4()
    
    # TODO: add value check

    logger.info(event_string, extra={"http.request.method": "get", "UUID": json_UUID})
    log_file = file_to_var.json_to_var("/home/tzur/final-client/elvis.json")

    os.remove("/home/tzur/final-client/elvis.json")

    doc_UUID = uuid.uuid4()
    resp = requests.post(url=f"http://13.81.211.207:9200/{event_string}/_doc/{doc_UUID}", json=log_json,
                        headers={'Content-Type': 'application/json'})
#    print(resp.json())
