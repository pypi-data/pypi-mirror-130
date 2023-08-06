# -*- coding:utf-8 -*-
from notebook.services.contents.largefilemanager import LargeFileManager


class TigerFileManager(LargeFileManager):

    def get(self, path, content=True, type=None, format=None):
        self.log.info("Welcome to TigerFileManager.get.")
        self.log.info("Welcome to TigerFileManager.get > path at %s" % path)
        self.log.info("Welcome to TigerFileManager.get > content at %s" % content)
        self.log.info("Welcome to TigerFileManager.get > type at %s" % type)
        self.log.info("Welcome to TigerFileManager.get > format at %s" % format)
        return super(TigerFileManager, self).get(path, content, type, format)

    def save(self, model, path=''):
        self.log.info("Welcome to TigerFileManager.save.")
        return super(TigerFileManager, self).save(model, path)
