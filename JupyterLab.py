#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) Huoty, All rights reserved
# Author: Huoty <sudohuoty@gmail.com>
# CreateTime: 2018-11-15 22:56:23

import os
import sys
import json
import socket
import logging
import threading
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

        self.setup_logging(reset=True)
        logging.info("hello world")
        self._log = logging.getLogger("JupyterLabView")

        try:
            with open("config.json") as fp:
                self.config = json.load(fp)
        except IOError:
            self.config = {}

        self.lab_python_path = self.config.get("pythonPath", sys.executable)
        self.lab_port = int(self.config.get("labPort", 12580))
        self.lab_log_path = self.config.get("labLogPath")
        self.notebook_config_path = self.config.get(
            "notebookConfigPath",
            ".jupyter_notebook_config.py"
        )

        self.lab_url = "http://localhost:{}".format(self.lab_port)

    def setup_logging(self, reset=False):
        logger = logging.getLogger()

        if len(logger.handlers) > 0 and not reset:
            logging.debug("logging has been set up")
            return

        logger.handlers = []
        logger.setLevel(logging.DEBUG)

        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(logging.DEBUG)
        stdout_handler.setFormatter(
            logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        )
        logger.addHandler(stdout_handler)

    def launch_jupyterlab(self):
        args = [self.lab_python_path, "-m", "jupyterlab",
                "--port", str(self.lab_port),
                "--config", self.notebook_config_path]
        env = os.environ.copy()
        env["HOME"] = self.lab_cwd
        stdout = None
        if self.lab_log_path:
            stdout = open(self.lab_log_path, 'ab')
        self._log.info("Launching jupyterlab service")
        proc = subprocess.Popen(
            args,
            cwd=self.lab_cwd,
            env=env,
            shell=False,
            stdout=stdout,
            stderr=subprocess.STDOUT
        )
        if stdout:
            stdout.close()
        self.lab_proc = proc
        return proc

    def close_jupyterlab(self):
        ret = 0
        while self.check_lab_server():
            self._log.info("Trying to close the jupyterlab service")
            ret = self.lab_proc.terminate()
        return ret

    def check_lab_server(self):
        sock = socket.socket()
        try:
            sock.connect(("localhost", self.lab_port))
            return True
        except socket.error:
            return False

    def get_accessible_lab_url(self, params):
        if self.check_lab_server():
            return self.lab_url

    def load_error_window(self, message=None):
        html = '<h1>{}</h1>'.format(message)
        th = threading.Thread(target=lambda: webview.load_html(html))
        th.start()
        webview.create_window('Error')

    def load_lab_window(self):
        self.launch_jupyterlab()
        webview.create_window("JupyterLab", "loading.html", js_api=self, debug=True)
        return self.close_jupyterlab()

    def run(self):
        if self.check_lab_server():
            self.load_error_window("JupyterLab service already exists")
            code = 1
        else:
            code = self.load_lab_window()
        self._log.info("Application exit")
        return code


if __name__ == "__main__":
    app = ViewApp()
    sys.exit(app.run())
