# -*- coding:utf-8 -*-
from concurrent.futures import ThreadPoolExecutor

from tornado import gen
from jupyter_client.ioloop import IOLoopKernelManager


class HubKernelManager(IOLoopKernelManager):

    _parallels = 2

    @property
    def executor(self):
        cls = type(self)
        if not hasattr(cls, "_executor"):
            cls._executor = ThreadPoolExecutor(self._parallels)
        return cls._executor

    @gen.coroutine
    def start_kernel(self, **kw):
        lines = kw.pop("inject_lines", None)
        super(HubKernelManager, self).start_kernel(**kw)
        if lines:
            yield self.inject_lines(lines)
        self.loop.call_later(1, self._check_alive)
        return

    @gen.coroutine
    def inject_lines(self, lines, silent=True):
        def fun():
            client = None
            try:
                client = self.blocking_client()
                client.start_channels()
                client.wait_for_ready(30)
                for line in lines:
                    client.execute(line, silent=silent)
            finally:
                if client:
                    client.stop_channels()

        self._launch_args["inject_lines"] = lines
        yield self.executor.submit(fun)

    @gen.coroutine
    def _check_alive(self):
        if self.is_alive():
            self.loop.call_later(1, self._check_alive)


class HubKernelManagerV2(IOLoopKernelManager):
    @gen.coroutine
    def start_kernel(self, **kw):
        lines = kw.pop("inject_lines", None)
        super(HubKernelManagerV2, self).start_kernel(**kw)

        if lines:
            from notebook.utils import maybe_future

            yield maybe_future(self.inject_lines(lines))

    @gen.coroutine
    def inject_lines(self, lines, silent=True):
        client = None
        try:
            client = self.blocking_client()
            client.start_channels()
            client.wait_for_ready(30)
            for line in lines:
                client.execute(line, silent=silent)
        finally:
            if client:
                client.stop_channels()
