#! coding:utf-8
"""
mk_newdir.py

Created by 0160929 on 2016/03/29 16:38
"""
import shutil

__version__ = '0.0'

import os
import sys

def mk_newdir(DIR):
    if os.path.exists(DIR):
        shutil.rmtree(DIR)
        os.mkdir(DIR)
    else:
        os.mkdir(DIR)


if __name__ == '__main__':
    main()
