import os
import unittest
from logic import UserList
class TestData(unittest.TestCase):
    """test_data [test classs for testing the data]
    """
    def test_write_file(self):
        """test_write_file [testing whether the write file is workin or not]
        """
        path = UserList(os.getcwd(), os.getcwd(), 'pranav', '580')
        inputvalues = [['testfile.txt', 'hello world'], ['testfile.txt', 'second statement']]
        returnvalues = ['file edited', 'file edited']
        result = []
        for i in inputvalues:
            result.append(path.write_file(i[0], i[1]))
        self.assertListEqual(result, returnvalues)
    def testing_create_folder(self):
        """testing_create_folder [testing whether the folder is created or not]
        """
        path = UserList(os.getcwd(), os.getcwd(), 'pranav', '580')
        inputvalues = ['sai1', 'sai1']
        returnvalues = ['folder created', 'failed to create folder']
        result = []
        for i in inputvalues:
            result.append(path.create_folder(i))
        self.assertListEqual(result, returnvalues)
if __name__ == "__main__":
    unittest.main()