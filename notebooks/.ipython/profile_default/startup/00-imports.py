#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) Huoty, All rights reserved
# Author: Huoty <sudohuoty@gmail.com>
# CreateTime: 2018-11-24 14:34:42

import os
import sys
import json
import contextlib


@contextlib.contextmanager
def _ignore_import_error():
    try:
        yield
    except ImportError:
        pass


with _ignore_import_error():
    import numpy as np

with _ignore_import_error():
    import pandas as pd

with _ignore_import_error():
    import matplotlib as mpl

with _ignore_import_error():
    import matplotlib.pyplot as plt
