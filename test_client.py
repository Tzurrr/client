import unittest
import watchdog_client
from unittest.mock import patch
import json
import os
import redis
import sender
import responses

class TestInotify(unittest.TestCase):
    def setUp(self):
        with open("/home/tzur/all-the-photos/file1_a.txt", "wb+") as file:
            file.write(b"a")
        with open("/home/tzur/all-the-photos/file1_b.txt", "wb+") as file:
            file.write(b"b")


    def test_coupling_logics(self):
        r = redis.Redis()
        r.set("/home/tzur/all-the-photos/file1", "/home/tzur/all-the-photos/file1_a.txt")
        arr = [("files", open("/home/tzur/all-the-photos/file1_a.txt", "rb")),
                ("files", open("/home/tzur/all-the-photos/file1_b.txt", "rb"))]

        resp = responses.post(
                "http://127.0.0.1:80/",
                body=arr)
        
        a = sender.send_files_to_server("/home/tzur/all-the-photos/file1_b.txt")

        print(a)
        self.assertEqual(a.status_code, resp.status)


if __name__ == '__main__':
    unittest.main()


