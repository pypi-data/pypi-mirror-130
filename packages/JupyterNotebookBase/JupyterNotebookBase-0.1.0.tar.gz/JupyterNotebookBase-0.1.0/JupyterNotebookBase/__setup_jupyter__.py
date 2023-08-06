# -*- coding:utf-8 -*-
from JupyterNotebookBase.jupyter_extensions import current_dir
import os
import shutil

jupyter_notebook_config = os.path.join(current_dir, "jupyter_notebook_config.py")
jupyter_nbconvert_config = os.path.join(current_dir, "jupyter_nbconvert_config.py")


def main():
    shutil.copy(jupyter_notebook_config, os.path.join(os.getenv("JUPYTER_CONFIG_HOME"), "jupyter_notebook_config.py"))
    shutil.copy(jupyter_nbconvert_config, os.path.join(os.getenv("JUPYTER_CONFIG_HOME"), "jupyter_nbconvert_config.py"))
