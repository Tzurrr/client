import json_parser
import os
import pytest


class TestJsonParse():
    def test_invalid_file(self):
        with open("file.json", "w+") as file:
            name = file.name

        with pytest.raises(json_parser.CustomError):
            json_parser.parse_json_to_var(name)

    def test_valid_file(self):
        with open("file1.json", "w+") as file:
            file.write("{}")
            name = file.name

        assert type(json_parser.parse_json_to_var(name)) == dict


