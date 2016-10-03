#! coding:utf-8
"""
ceps.py

Created by 0160929 on 2016/03/23 14:29
"""
__version__ = '0.0'

import numpy as np


def ceps_gwt(gwtdata, lifter=5,  mode=None):
    """
    GWTのデータ配列からケプストラムを算出
    dataは1次元配列のみ可能.
    ※ ケプストラムには周波数軸上での折り返し成分が必要.
    ※ GWTスペクトルには折り返し成分がないため、人為的に作成する。
    :param data: 振幅スペクトル 1D-ndarray
    :param lift: リフタリング次数
    :param lift2: リフタリング次数. type='band'のときのみ利用。
    :param mode: 'low', 'high', 'band'
    :return: lifterd_data
    """


    # 左側データ
    gwt_left = np.atleast_2d(gwtdata)
    # print gwt_left.shape

    # 右側データの生成：(人為的に折り返す)
    gwt_right = np.fliplr(gwt_left)
    # print gwt_right.shape

    # numpy.hstack() で列方向に結合
    gwt_data = np.hstack((gwt_left, gwt_right))
    # print gwt_data.shape

    del gwt_right
    del gwt_left
    del gwtdata

    # 周波数領域
    FFT_abs = np.abs(gwt_data)

    # ケプストラム
    ceps = np.real(np.fft.ifft(np.log(FFT_abs)))

    # リフタリング
    rown, cols = ceps.shape
    Ceps_low = ceps.copy()

    if mode == "low":
        #  "low [1, 1, 1...0.0.0.0...1, 1, 1]"
        w = np.hstack((np.ones((rown, lifter)), np.zeros((rown, cols - 2 * lifter)), np.ones((rown, lifter))))
    elif mode == "high":
        #:  "high [0, 0, 0...1.1.1.1...0, 0, 0]"
        w = np.hstack((np.zeros((rown, lifter)), np.ones((rown, cols - 2 * lifter)), np.zeros((rown, lifter))))

    Ceps_low = Ceps_low * w

    # 逆毛ぷす
    Ceps_sspec = np.abs(np.exp(np.fft.fft(Ceps_low)))

    # 反転成分除去(1次元データなので0インデックス)
    Cepsed = Ceps_sspec[0, :cols / 2].T
    return Cepsed
