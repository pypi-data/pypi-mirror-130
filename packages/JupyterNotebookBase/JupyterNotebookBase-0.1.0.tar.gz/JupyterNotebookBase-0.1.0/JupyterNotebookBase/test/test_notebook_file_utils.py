# -*- coding:utf-8 -*-
from JupyterNotebookBase.utils import notebook_file_utils
from JupyterNotebookBase.public_extensions import current_dir
import unittest


class TestNotebookFileUtils(unittest.TestCase):

    def test_get_file_list_by_sort(self):
        file_list = notebook_file_utils.get_file_list_by_sort(current_dir)
        for file in file_list:
            print(file)


if __name__ == '__main__':
    unittest.main()
