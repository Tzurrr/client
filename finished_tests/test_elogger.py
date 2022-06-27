import elogger
import pytest
import requests
import json
import time


class TestELogger():
    def test_with_valid_index_name(self):
        resp = requests.get("http://13.81.211.207:9200/a/_count")
        count_of_documents = json.loads(resp.content.decode())["count"]

        a = elogger.write_logs_to_elastic("a")
        time.sleep(1)

        resp = requests.get("http://13.81.211.207:9200/a/_count")
        new_count_of_documents = json.loads(resp.content.decode())["count"]

        assert count_of_documents + 1 == new_count_of_documents

    def test_with_blank_index_name(self):
        with pytest.raises(elogger.BlankIndexException):
            elogger.write_logs_to_elastic("")


