#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) Huoty, All rights reserved
# Author: Huoty <sudohuoty@gmail.com>
# CreateTime: 2018-11-15 22:56:23

import os
import sys
import json
import socket
import subprocess
import webview
import jupyterlab


class ViewApp(object):

    def __init__(self):
        self.cwd = os.path.abspath(os.path.dirname(__file__))
        self.lab_cwd = os.path.join(self.cwd, "notebooks")
        self.lab_proc = None
        self.lab_version = jupyterlab.__version__

        os.chdir(self.cwd)

        try:
            with open("config.json") as fp:
                self.config = json.load(fp)
        except IOError:
            self.config = {}

        self.lab_python_path = self.config.get("pythonPath", sys.executable)
        self.lab_port = self.config.get("labPort", "12580")
        self.lab_log_path = self.config.get("labPath", "lab.log")
        self.notebook_config_path = self.config.get(
            "notebookConfigPath",
            ".jupyter_notebook_config.py"
        )

        self.lab_url = "http://localhost:{}".format(self.lab_port)

    def launch_jupyterlab(self):
        args = [self.lab_python_path, "-m", "jupyterlab",
                "--port", self.lab_port,
                "--config", self.notebook_config_path]
        env = os.environ.copy()
        env["HOME"] = self.lab_cwd
        stdout = open(self.lab_log_path, 'ab')
        proc = subprocess.Popen(
            args,
            cwd=self.lab_cwd,
            env=env,
            shell=False,
            stdout=stdout,
            stderr=subprocess.STDOUT
        )
        stdout.close()
        self.lab_proc = proc
        return proc

    def check_lab_server(self):
        sock = socket.socket()
        try:
            sock.connect(("localhost", self.lab_port))
            return True
        except socket.eror:
            return False

    def run(self):
        self.launch_jupyterlab()
        webview.create_window("JupyterLab", "loading.html")
        return self.lab_proc.terminate()


if __name__ == "__main__":
    app = ViewApp()
    sys.exit(app.run())
