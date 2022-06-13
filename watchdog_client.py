import os
import sys
import time
from threading import Thread
import time
import datetime
import redis
from watchdog.events import PatternMatchingEventHandler, FileSystemEventHandler
from watchdog.observers import Observer
from queue import Queue
import os
from watchdog.events import FileCreatedEvent, FileClosedEvent
import sender
import elogger
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import as_completed
import json_parser


conf = json_parser.parse_json_to_var("/home/tzur/client/config.json")
dir_path = conf["photos_dir"]
r = redis.Redis()

def process_queue(watchdog_queue):
    counter = 0
    while True:
        counter += 1
        if not watchdog_queue.empty():
            event = watchdog_queue.get()
            elogger.write_logs_to_elastic("arrivedtoserver")
            if r.get(f"{os.path.splitext(event.src_path)[0][:-2]}") != None:
                sender.send_files_to_server(event.src_path)
            else:
                r.setex(f"{os.path.splitext(event.src_path)[0][:-2]}", datetime.timedelta(minutes=1), event.src_path)


class FileWatchdog(FileSystemEventHandler):
    def __init__(self, queue):
        self.queue = queue

    def process(self, event):
        self.queue.put(event)

    def on_closed(self, event):
        self.process(event)

if __name__ == "__main__":
    watchdog_queue = Queue()
    local_conf = json_parser.parse_json_to_var("/home/tzur/client/config.json")
    local_conf = local_conf["redis_conf"]

    for file in os.listdir(dir_path):
        filename = os.path.join(dir_path, file)
        event = FileClosedEvent(filename)
        watchdog_queue.put(event)

    event_handler = FileWatchdog(watchdog_queue)
    observer = Observer()
    observer.schedule(event_handler, path=dir_path)
    observer.start()
    try:
        with ProcessPoolExecutor() as executor:
            a = executor.submit(process_queue(watchdog_queue), watchdog_queue)
            a.result()

    except KeyboardInterrupt:
        observer.stop()
        observer.join()

