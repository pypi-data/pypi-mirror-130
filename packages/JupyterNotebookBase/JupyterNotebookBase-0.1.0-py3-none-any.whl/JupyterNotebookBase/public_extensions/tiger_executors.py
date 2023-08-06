# -*- coding:utf-8 -*-
import sys
from nbconvert import HTMLExporter
from nbconvert.postprocessors import PostProcessorBase
from JupyterNotebookBase.utils.common_utils import is_new_notebook
from nbconvert.preprocessors.execute import ExecutePreprocessor
from traitlets.traitlets import Any


class TigerPreprocessor(ExecutePreprocessor):

    param_file_path = Any(default_value="/ossfs/.param.conf", allow_none=True, help="param file").tag(config=True)

    def __init__(self, **kw):
        super(TigerPreprocessor, self).__init__(**kw)
        if is_new_notebook():
            from JupyterNotebookBase.public_extensions.tiger_preprocessor_v2 import TigerPreprocessorV2  # noqa

            self.preprocessor = TigerPreprocessorV2(param_file_path=self.param_file_path)
        else:
            from JupyterNotebookBase.public_extensions.tiger_preprocessor_v1 import TigerPreprocessorV1  # noqa

            self.preprocessor = TigerPreprocessorV1(param_file_path=self.param_file_path)

    def preprocess(self, nb, resources=None, km=None):
        return self.preprocessor.preprocess(nb, resources, km)

    def preprocess_cell(self, cell, resources, index):
        return self.preprocessor.preprocess_cell(cell, resources, index)


class TigerHTMLExporter(HTMLExporter):
    def __init__(self, config=None, **kw):
        super(TigerHTMLExporter, self).__init__(config, **kw)


class TigerPostprocessor(PostProcessorBase):
    def postprocess(self, input):
        if is_new_notebook():
            from JupyterNotebookBase.public_extensions.tiger_preprocessor_v2 import error_raise  # noqa
        else:
            from JupyterNotebookBase.public_extensions.tiger_preprocessor_v1 import error_raise  # noqa
        if error_raise:
            sys.exit(1)
