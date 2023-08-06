# -*- coding:utf-8 -*-
from nbconvert.preprocessors.execute import ExecutePreprocessor
from nbformat.v4.nbbase import new_code_cell

error_raise = False


class TigerPreprocessorV2(ExecutePreprocessor):
    def __init__(self, param_file_path, **kw):
        print("=====================tiger_preprocessor_v2.py=========================")
        super(TigerPreprocessorV2, self).__init__(**kw)
        self.param_file_path = param_file_path

    def preprocess(self, nb, resources=None, km=None):
        print("param_file_path: %s" % self.param_file_path)
        print("================TigerPreprocessorV2=============preprocess========================================")
        return super(TigerPreprocessorV2, self).preprocess(nb, resources, km)

    def preprocess_cell(self, cell, resources, index):
        print("================TigerPreprocessorV2=============preprocess_cell===================================")
        cell, resources = super(TigerPreprocessorV2, self).preprocess_cell(cell, resources, index)
        new_cell = self.execute_cell(cell=new_code_cell(source="%who"), cell_index=index, store_history=True)
        print()
        print(new_cell.outputs[0]["text"])
        print()
        if new_cell.outputs[0]["text"]:
            for v in new_cell.outputs[0]["text"].split("\t"):
                try:
                    msg = self.execute_cell(
                        cell=new_code_cell(source="%store {}".format(v.strip())), cell_index=index, store_history=True
                    ).outputs[0][
                        "text"
                    ]  # noqa
                    print(msg)
                except Exception:  # noqa
                    pass
        self.nb["cells"][index] = cell
        return cell, resources
