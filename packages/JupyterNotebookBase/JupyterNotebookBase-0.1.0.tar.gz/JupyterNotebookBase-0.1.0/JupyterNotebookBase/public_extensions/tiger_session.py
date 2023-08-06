# -*- coding:utf-8 -*-
from notebook.services.sessions.sessionmanager import SessionManager
from tornado import gen
import copy
import os
import re
import json
import codecs


class HubSessionManager(SessionManager):
    def __init__(self, **kw):
        super(HubSessionManager, self).__init__(**kw)

    @gen.coroutine
    def start_kernel_for_session(self, session_id, path, name, type, kernel_name):
        env = copy.copy(os.environ)
        pattern = re.compile(r"notebook_(\d+).ipynb")
        m = pattern.match(name)
        if m is not None:
            node_id = m.group([0])
            os.system("osscmd -H xxx -i xxx -k xxx ")
            try:
                with open("/ossfs/.%s_param.conf" % node_id, "r", encoding="UTF-8") as f:
                    content = f.read()
                    params = json.loads(content)
            except Exception as e:
                params = dict()
        else:
            params = dict()
        lines = params
        kernel_path = self.contents_manager.get_kernel_path(path=path)
        kernel_id = yield gen.maybe_future(
            self.kernel_manager.start_kernel(path=kernel_path, kernel_name=kernel_name, env=env, inject_lines=lines)
        )
        raise gen.Return(kernel_id)


class HubSessionManagerV2(SessionManager):
    def __init__(self, **kw):
        super(HubSessionManagerV2, self).__init__(**kw)

    @gen.coroutine
    def start_kernel_for_session(self, session_id, path, name, type, kernel_name):
        env = copy.copy(os.environ)
        pattern = re.compile(r"notebook_(\d+).ipynb")
        m = pattern.match(name)
        params = {}
        if m is not None:
            node_id = m.group([0])
            param_file_path = "/ossfs/.%s_param.conf" % node_id
            if os.path.exists(param_file_path):
                with codecs.open(param_file_path, "r", encoding="UTF-8") as f:
                    content = f.read()
                params = json.loads(content)
        lines = ['name="zhangsan"']
        kernel_path = self.contents_manager.get_kernel_path(path=path)
        from notebook.utils import maybe_future

        kernel_id = yield maybe_future(
            self.kernel_manager.start_kernel(path=kernel_path, kernel_name=kernel_name, env=env, inject_lines=lines)
        )
        raise gen.Return(kernel_id)
