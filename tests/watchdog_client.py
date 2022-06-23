import os
import sys
import time
import datetime
from watchdog.events import PatternMatchingEventHandler, FileSystemEventHandler
from watchdog.observers import Observer
from queue import Queue
import os
from watchdog.events import FileCreatedEvent, FileClosedEvent
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import as_completed
import json_parser
import files_handler

class FileWatchdog(FileSystemEventHandler):
    def __init__(self, queue):
        self.queue = queue

    def process(self, event):
        self.queue.put(event)

    def on_closed(self, event):
        self.process(event)

if __name__ == "__main__":
    watchdog_queue = Queue()
    conf = json_parser.parse_json_to_var("/home/tzur/client/config.json")
    dir_path = conf["photos_dir"]

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
            a = executor.submit(files_handler.process_queue(watchdog_queue), watchdog_queue)
            a.result()

    except KeyboardInterrupt:
        observer.stop()
        observer.join()

