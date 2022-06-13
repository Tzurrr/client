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
from threading import Thread
import os
from watchdog.events import FileCreatedEvent, FileClosedEvent
import remove_older
import sender
import elogger
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import as_completed
import json_parser


conf = json_parser.parse_json_to_var("/home/tzur/client/config.json")
dir_path = conf["photos_dir"]

def process_queue(watchdog_queue):
    counter = 0
    first_half_arr = []
    second_half_arr = []
    while True:
        counter += 1
        first_half_arr = remove_older.remove(first_half_arr)
        second_half_arr = remove_older.remove(second_half_arr)
        if not watchdog_queue.empty():
            event = watchdog_queue.get()
            elogger.write_logs_to_elastic("arrivedtoserver")

            if os.path.splitext(event.src_path)[0][-1] != "a" and os.path.splitext(event.src_path)[0][-1] != "b":
                os.remove(event.src_path)

            elif os.path.splitext(event.src_path)[0][-1] == "a":
                r.set(f"{os.path.splitext(event.src_path)[0][:-2]}", event.src_path, ex=60)

            elif os.path.splitext(event.src_path)[0][-1] == "b":
                if len(first_half_arr) > 0:
                    sender.send_files_to_server(event.src_path)


class FileWatchdog(PatternMatchingEventHandler):
    def __init__(self, queue):
        PatternMatchingEventHandler.__init__(self, patterns=["*"], ignore_patterns=None, ignore_directories=False, case_sensitive=True)
        self.queue = queue

    def process(self, event):
        self.queue.put(event)

    def on_closed(self, event):
        self.process(event)

if __name__ == "__main__":
    r = redis.Redis('localhost', 6379, charset="utf-8")
    watchdog_queue = Queue()

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

