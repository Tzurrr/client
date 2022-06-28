import elogger
import requests
import json
import time
import unittest


class TestELogger(unittest.TestCase):
    
    def test_with_valid_index_name(self):
        # No specific hardcoded data in sources - use config file 
        count_request_url = "http://13.81.211.207:9200/a/_count"
        resp = requests.get(count_request_url)
        # check HTTP error code first
        count_of_documents = json.loads(resp.content.decode())["count"]

        a = elogger.write_logs_to_elastic("a")
        time.sleep(1)

        resp = requests.get(count_request_url)
        # decode utf8
        new_count_of_documents = json.loads(resp.content.decode())["count"]

        self.assertEqual((count_of_documents + 1), new_count_of_documents)

    def test_with_blank_index_name(self):
        self.assertRaises(Exception, elogger.write_logs_to_elastic, "")
        


if __name__ == '__main__':
    unittest.main()

