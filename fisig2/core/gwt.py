# -*- coding: utf-8 -*-
"""GaborWavelet.py
ガボール変換を使ったウェーブレット変換

Version:
    1.0


Reference:
    http://hp.vector.co.jp/authors/VA046927/gabor_wavelet/gabor_wavelet.html
    http://criticaldays2.blogspot.jp/2014/04/blog-post_23.html
    http://www.softist.com/programming/gabor-wavelet/gabor-wavelet.htm
"""
__version__ = '2.0'
import numpy as np


def gwt(audio_data, Fs, a_N=512, f_min=0, f_max=None):
    def psi(a, b, a_t, sigma):
        """ ガボール関数"""
        t = (a_t - b) / a
        g = 1. / (2 * np.sqrt(np.pi * sigma)) * np.exp(-1. * t ** 2 / (4. * sigma ** 2))
        e = np.exp(1j * 2. * np.pi * t)
        return g * e

    def utili_sample(a, sigma, Vc):

        samp = a * sigma * np.sqrt(-2. * np.log(Vc))
        return samp

    import time

    start = time.time()

    Fs = float(Fs)
    adata = audio_data
    N = len(adata)
    X = np.array(adata) * 1.

    # -------------------
    # ウェーブレット変換処理
    # -------------------
    """
        解析パラメータ
    """
    # 1. ガボールウェーブレットパラメータ
    sigma = 5
    # 2. 周波数分割数
    # a_N = 512 (ver2.0から引数で定義)
    # 解析周波数(最低周波数)
    f_min = 0
    # 解析周波数(最高周波数)
    if f_max == None:
        f_max = Fs / 2
    # 有効計算幅(小さいほど精度高い)
    Vc = 0.00001

    # ループ準備
    # ---------
    # 時間幅
    # t = np.arange(0, N) / float(Fs)
    t = np.linspace(0, N / Fs, N)
    # 解析周波数
    _fn = np.linspace(f_min, f_max, a_N + 1)
    fn = _fn[1:]
    # 解析結果格納バッファ
    Anadata = np.empty(shape=(N, a_N), dtype=complex)

    print "-----------------------------"
    print '== Gabor Wavelet Analysing =='
    print '== ...'
    print '== f_min=%r, f_max=%r, a_N=%r' % (f_min, f_max, a_N)
    print '== Vc=%r, Sigma=%r' % (Vc, sigma)
    print '== f[0]=%r, f[1]=%r, f[-1]=%r' % (fn[0], fn[1], fn[-1])
    print '== ...'

    # for a_n in range(0, a_N):
    #     "0.68s"
    #     a = 1. / fn[a_n]
    #     b = 1. * N / 2. / Fs
    #     Psi = psi(a, b, t, sigma)
    #
    #     # 実用領域のみ畳み込み
    #     us = np.floor(utili_sample(a, sigma, Vc) * Fs)
    #     if us < N:
    #         ss = np.floor(N / 2 - us / 2)
    #         se = np.floor(N / 2 + us / 2)
    #         Psi = Psi[ss:se]
    #
    #     # 畳み込み (convolve)
    #     Anadata[:, a_n] = (1. / np.sqrt(a)) * np.convolve(X, Psi, 'same')

    def _subfun(t, sigma, Vc, N, a_N):
        "0.65s"
        a = 1. / fn[a_n]
        b = 1. * N / 2. / Fs
        Psi = psi(a, b, t, sigma)

        # 実用領域のみ畳み込み
        us = np.floor(utili_sample(a, sigma, Vc) * Fs)
        if us < N:
            ss = np.floor(N / 2 - us / 2)
            se = np.floor(N / 2 + us / 2)
            Psi = Psi[ss:se]

        return (1. / np.sqrt(a)) * np.convolve(X, Psi, 'same')

    Anadata = [_subfun(t, sigma, Vc, N, a_N) for a_n in range(0, a_N)]
    Anadata = np.array(Anadata).T


    # 解析時間
    print '== return spectrum<%r : % r>, trange, frange' % Anadata.shape
    print("== Finish Analys :{0}".format(time.time() - start))
    print "-----------------------------"

    return Anadata, t, fn

# ******************************************
#
#  Demo
#
# ******************************************

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    import numpy as np

    filename = 'audio-golf1.wav'

    # オーディオのロード
    from scipy.io.wavfile import read

    fs, data = read(filename)
    data = data[0:fs / 4 - 1]

    # GWT解析
    gwt_data = gwt(data, Fs=fs)
    gdata, trange, frange = np.abs(gwt_data)
    gdata = 20 * np.log10(gdata)
    #
    # # STFTの表示
    # fig2 = plt.figure()
    # ax2 = fig2.gca()
    # plt.specgram(data, NFFT=512, noverlap=256, Fs=fs, cmap='jet', scale='dB', mode='magnitude', vmin=0, vmax=120)
    # plt.colorbar()
    # plt.title('specgram (STFT)')
    #
    # # Scarogramの表示
    # fig3 = plt.figure()
    # ax3 = fig3.add_subplot(111)
    # extent = 0, (fs / 2. - 1) / fs, 0, fs / 2
    # gdata = np.flipud(gdata.T)
    # img = plt.imshow(gdata, cmap='jet', extent=extent, vmin=0, vmax=120)
    # plt.colorbar()
    # ax3.set_title('scarogram (GWT)')
    # ax3.axis('auto')
    #
    # plt.show()

    import csv

    with open('log.csv', 'w') as f:
        writer = csv.writer(f, lineterminator='\n')
        # writer.writerows(self.A_Matrix.tolist())
        writer.writerows(self.phy)
        writer.writerows(self.elements)
