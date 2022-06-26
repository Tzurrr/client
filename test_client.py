import unittest
import watchdog_client
from unittest.mock import patch
import json
import os
import redis
import sender


class TestInotify(unittest.TestCase):
    def setUp(self):
        with open("/home/tzur/all-the-photos/file1_a.txt", "wb+") as file:
            file.write(b"a")
        with open("/home/tzur/all-the-photos/file1_b.txt", "wb+") as file:
            file.write(b"b")


    def test_coupling_logics(self):
        r = redis.Redis()
        r.set("/home/tzur/all-the-photos/file1", "/home/tzur/all-the-photos/file1_a.txt")
        with patch('sender.requests.post') as mocked_get:
            arr = [("files", open("/home/tzur/all-the-photos/file1_a.txt", "rb")),
                    ("files", open("/home/tzur/all-the-photos/file1_b.txt", "rb"))]

            a = sender.send_files_to_server("/home/tzur/all-the-photos/file1_b.txt")

            mocked_get.assert_called_with(url="http://127.0.0.1:80/", files=arr)
        pass

#    def tearDown(self):
#        os.remove("file1_a.txt")
#        os.remove("file1_b.txt")


if __name__ == '__main__':
    unittest.main()


