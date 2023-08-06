# -*- coding:utf-8 -*-
from JupyterNotebookBase.utils.log_utils import get_logger

log = get_logger()


def post_save_hook(os_path, model, contents_manager):
    logger = contents_manager.log
    logger.info("os_path at %s" % os_path)
    logger.info("model at %s" % model)
