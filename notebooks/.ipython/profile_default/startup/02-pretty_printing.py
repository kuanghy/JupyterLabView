#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) Huoty, All rights reserved
# Author: Huoty <sudohuoty@gmail.com>
# CreateTime: 2018-11-24 14:50:36

from pprint import pprint


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
