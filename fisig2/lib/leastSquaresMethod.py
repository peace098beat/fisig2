#! coding:utf-8
"""
leastSquaresMethod

Created by 0160929 on 2016/04/06 15:55
"""


def leastSquaresMethod(x, y):
    """http://tokeigaku.blog.jp/python/numpy/%E6%9C%80%E5%B0%8F%E4%BA%8C%E4%B9%97%E6%B3%95"""
    import numpy as np

    x = np.array(x).flatten()
    y = np.array(y).flatten()

    try:
        A = np.array([x, np.ones(x.size)]).T
        a, b = np.linalg.lstsq(A, y)[0]
        return a, b
    except:
        # print("Err:leastSquaresMethod", x, y)
        return 0, 0
