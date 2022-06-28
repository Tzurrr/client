import redis
import json_parser
import elogger
import sender
import os
import datetime

def process_queue(watchdog_queue):
    conf = json_parser.parse_json_to_var("/home/tzur/client/config.json")
    dir_path = conf["photos_dir"]
    r = redis.Redis()

    while True:
        if not watchdog_queue.empty():
            event = watchdog_queue.get()
            elogger.write_logs_to_elastic("arrivedtoserver")
            if r.get(f"{os.path.splitext(event.src_path)[0][:-2]}") != None:
                sender.send_files_to_server(event.src_path)
            else:
                r.setex(f"{os.path.splitext(event.src_path)[0][:-2]}", datetime.timedelta(minutes=1), event.src_path)
        #else:
        #sleep(0)
