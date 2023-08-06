# -*- coding:utf-8 -*-
from nbconvert.preprocessors.execute import ExecutePreprocessor

error_raise = False


class TigerPreprocessorV1(ExecutePreprocessor):
    def __init__(self, param_file_path, **kw):
        print("=====================tiger_preprocessor.py=========================")
        super(TigerPreprocessorV1, self).__init__(**kw)
        self.param_file_path = param_file_path

    def preprocess(self, nb, resources=None, km=None):
        print("param_file_path: %s" % self.param_file_path)
        print("================TigerPreprocessor=============preprocess============================================")
        return super(TigerPreprocessorV1, self).preprocess(nb, resources, km)

    def preprocess_cell(self, cell, resources, index):
        print("================TigerPreprocessor=============preprocess_cell=========================================")
        return super(TigerPreprocessorV1, self).preprocess_cell(cell, resources, index)
