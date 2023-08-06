# -*- coding:utf-8 -*-
from notebook.base.handlers import IPythonHandler
from concurrent.futures import ThreadPoolExecutor
import json
from tornado import gen, concurrent

# from jupyter_client.asynchronous.client import AsyncKernelClient
from jupyter_client.blocking.client import BlockingKernelClient
from notebook.utils import url_path_join
from JupyterNotebookBase.utils import notebook_kernel_utils


class OperateNotebookHandler(IPythonHandler):

    executor = ThreadPoolExecutor(4)

    def get_request_param(self, key, require=True):
        if self.request.headers["Content-Type"] == "application/json":
            args = json.loads(self.request.body)
            val = args.get(key)
        else:
            val = self.get_argument(key)
        if require and val is None:
            raise Exception("missing required param %s" % key)

        return val

    def get(self):
        res = {"success": "true", "message": "notebook is running"}
        self.write(res)

    @gen.coroutine
    def post(self):
        res = {"success": "true"}
        try:
            method = self.get_request_param("method")
            if method == "updateAIStudioDataframe":
                res = yield self.update_aistudio_dataframe()
                res.update(res)
            else:
                raise Exception("no method match")
        except Exception as e:
            res["success"] = "false"
            res["errorMessage"] = "%s" % e
        self.write(res)

    @concurrent.run_on_executor
    def update_aistudio_dataframe(self):
        nb_file_name = self.get_request_param("fileName")
        kernel_id = notebook_kernel_utils.get_notebook_kernel_id(nb_file_name)
        print("kernel_id: %s" % kernel_id)
        node_id = self.get_request_param("nodeId")
        param_file = "/root/.%s_param.conf" % node_id
        try:
            with open(param_file, "r", encoding="UTF-8") as f:
                content = f.read()
            lines = content
        except Exception as e:
            lines = ["import time\nimport uuid\na = time.time()\nb = uuid.uuid4()"]
        print("inject line length %s" % len(lines))
        kc = BlockingKernelClient(connection_file="/Users/youxuehu/Library/Jupyter/runtime/kernel-%s.json" % kernel_id)
        kc.load_connection_file()
        status, outs = notebook_kernel_utils.run_code_with_kernel(kc, lines)
        return {"status": status, "outs": outs}


def load_jupyter_server_extension(nb_app):
    web_app = nb_app.web_app
    host_pattern = ".*$"
    route_pattern = url_path_join(web_app.settings["base_url"], "/operate")
    web_app.add_handlers(host_pattern, [(route_pattern, OperateNotebookHandler)])
