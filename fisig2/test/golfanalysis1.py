#! coding:utf-8
"""
golfanalysis1.py

Created by 0160929 on 2016/03/23 9:49
"""

import numpy as np

from fisig2.signal import SignalData

__version__ = '0.0'

wavfilepaht = "./audio.wav"

if __name__ == '__main__':
    # オーディオロード
    sig = SignalData().load_wav(wavfilepaht, 'M')
    # スペクトログラム
    spgram = sig.slice_time_ms(80, 120).gwt()
    # スペクトル(インパクト音)
    spec_impact = spgram.slice_time_ms(20, 25).time_average()  # .plot().show()

    # ガワ感
    g = spec_impact.liftering(lifter=5, mode="low").slice_freq_hz(1000, 4500).info().get_data()
    gawa = np.var(g)
    print gawa
    # 硬さ
    katasa = spec_impact.liftering(lifter=15, mode="low").slice_freq_khz(1, 4.5).cof()  # .plot().show()
    print katasa

    # gdata1 = spec_impact.get_logpow()
    # gdata2 = spec_impact.liftering(lifter=13, mode="high").get_logpow()

    # from matplotlib import pyplot as plt
    # plt.plot(gdata1)
    # plt.plot(gdata2)
    # plt.show()
