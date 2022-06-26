import pytest
import files_handler
import redis
import os


class TestFilesHandler():

    def test_save_to_redis(self):
        # watchdog client should run at the background
        with open("/home/tzur/all-the-photos/abc.txt", "w+") as file:
            name = file.name

        r = redis.Redis()
        content = r.get(os.path.splitext(name)[0][:-2]).decode()
        assert content == "/home/tzur/all-the-photos/abc.txt"

#    def test_with_blank_index_name(self):
 #       with pytest.raises(elogger.BlankIndexException):
  #          elogger.write_logs_to_elastic("")


