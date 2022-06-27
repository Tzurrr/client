import pytest
import redis
import os
import sender


class TestSender():
    def test_build_file_array_organized(self):
        with open("a", "w+") as file:
            pass
        with open("b", "w+") as file:
            pass

        arr = sender.build_file_array("/home/tzur/client/tests/a", "/home/tzur/client/tests/b")
        local_arr = [("files", open("/home/tzur/client/tests/a", "rb")), ("files", open("/home/tzur/client/tests/b", "rb"))]
        assert (arr[0][1].name, arr[1][1].name) == (local_arr[0][1].name, local_arr[1][1].name)

    def test_build_file_array_unorganized(self):
        arr = sender.build_file_array("/home/tzur/client/tests/b", "/home/tzur/client/tests/a")
        local_arr = [("files", open("/home/tzur/client/tests/a", "rb")), ("files", open("/home/tzur/client/tests/b", "rb"))]
        assert (arr[0][1].name, arr[1][1].name) == (local_arr[0][1].name, local_arr[1][1].name)

