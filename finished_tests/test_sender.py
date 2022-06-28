import redis
import os
import sender
import unittest


class TestSender(unittest.TestCase):
    # Missed comment for whole test and also for specific lines/decisions
    def setUp(self):
        
        # CR: Just open,close wil be enough
        with open("a", "w+") as file:
            pass
        with open("b", "w+") as file:
            pass
         # CR: file handler leak
         # variable names should be selfexplanatory
        self.local_arr = [("files", open("/home/tzur/client2/a", "rb")), ("files", open("/home/tzur/client2/b", "rb"))]

    def test_build_file_array_organized(self):
        arr = sender.build_file_array("/home/tzur/client2/a", "/home/tzur/client2/b")
        self.assertEqual((arr[0][1].name, arr[1][1].name), (self.local_arr[0][1].name, self.local_arr[1][1].name))

    def test_build_file_array_unorganized(self):
        arr = sender.build_file_array("/home/tzur/client2/b", "/home/tzur/client2/a")
        self.assertEqual((arr[0][1].name, arr[1][1].name), (self.local_arr[0][1].name, self.local_arr[1][1].name))
    
    def tearDown(self):
        os.remove("./a")
        os.remove("./b")

if __name__ == '__main__':
    unittest.main()
