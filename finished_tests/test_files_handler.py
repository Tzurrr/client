import files_handler
import redis
import os
from watchdog.events import FileClosedEvent
import files_handler
from queue import Queue
import elogger
import unittest


class TestFilesHandler(unittest.TestCase):
    def test_save_to_redis(self):
        with open("/home/tzur/all-the-photos/abc.txt", "w+") as file:
            name = file.name

        watchdog_queue = Queue()
        event = FileClosedEvent(name)
        watchdog_queue.put(event)
        files_handler.process_queue(watchdog_queue)

        r = redis.Redis()
        content = r.get(os.path.splitext(name)[0][:-2]).decode()
        self.assertEqual(content, "/home/tzur/all-the-photos/abc.txt")

