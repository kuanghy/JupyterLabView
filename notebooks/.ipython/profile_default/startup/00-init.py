# Copyright (c) Huoty, All rights reserved
# Author: Huoty <sudohuoty@gmail.com>
# CreateTime: 2018-11-24 14:34:42

import os
import sys
import json
import contextlib
from pprint import pprint


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


@contextlib.contextmanager
def _ignore_exception():
    try:
        yield
    except Exception:
        pass


with _ignore_exception():
    np.set_printoptions(precision=6, edgeitems=4)

with _ignore_exception():
    pd.set_option('display.max_rows', 240)


if sys.platform == "darwin":
    from IPython.display import set_matplotlib_formats
    set_matplotlib_formats('retina')


def run_which_nodes(node="last_expr"):
    """Specifying which nodes should be run interactively

    displaying output from expressions

    ('all', 'last', 'last_expr' or 'none')
    """
    from IPython.core.interactiveshell import InteractiveShell
    InteractiveShell.ast_node_interactivity = node
