import json_parser
import os
import unittest


class TestJsonParse(unittest.TestCase):
    def test_invalid_file(self):
        with open("file.json", "w+") as file:
            name = file.name

        self.assertRaises(Exception, json_parser.parse_json_to_var, name)

    def test_valid_file(self):
        with open("file.json", "w+") as file:
            file.write("{}")
            name = file.name

        self.assertEqual(type(json_parser.parse_json_to_var(name)), dict)
    
    def tearDown(self):
        os.remove("file.json")


if __name__ == '__main__':
    unittest.main()

