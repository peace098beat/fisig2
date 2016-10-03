#! coding:utf-8
"""
    fisig.signal.py
    ~~~~~~~~~~~~~~~

    シグナルクラス. 信号データクラス. wavファイルやcsv等から読み込んだ1次元データ
    に対して, 信号処理を行うことができる.

"""
import os

from .core import *
from .spectrogram import SpectrogramData
from .spectrum import SpectrumData


class SignalData(BaseData):
    """Signalクラスは信号処理における最初の重要なクラスです.
    信号を.wavファイルやcsvファイルからロードすることから始まり,
    読み込んだ信号データに対し, 準備されている信号処理を行うことができます.

    使い方
    ----

        # # >>> from signal import Signal
        # >>> sig = Signal()
        # >>> sig.load_wav('./test/audio.wav', channel_no=0)
        # >>> print sig.fs
        # >>> print sig.data.shape
        # >>> print sig.get_times
        # >>> spectrum = sig.fft("hanning")
        # >>> spectrogram = sig.stft(256, "hanning", 125, 0.5)

    """

    def __init__(self):
        super(SignalData, self).__init__()
        self._source_path = None
        self.name = ""
        # SignalData固有プロパティ
        self._data_ch = None

    def info(self):
        print("\n#: ------------------------------- :#")
        print("source path:%r" % self._source_path)
        print("data shape:%r" % self.get_data().shape)
        print("start:%r[n] - end:%r[n]" % (self._x_ss, self._x_es))
        print("times %.5f[ms]-%.5f[ms]" % (self.get_xdata()[0] * 1000, self.get_xdata()[-1] * 1000))
        print("#: ------------------------------- :#\n")
        return self

    def load_wav(self, wavfilepath, ch="M"):
        """wavファイルからオーディオデータを読み込みます. Signalクラスに保持さるのは1チャンネル分のデータになります.
        もし, wavファイルに複数のチャンネルが含まれている場合は:param:ch <"R:0","L":1,"M">にて指定可能です.
        """
        # Coreモジュールで定義
        data, fs, times = _load_wav(wavfilepath, data_ch=ch)
        self._source_path = wavfilepath
        self._data_ch = ch
        self._data = data
        self._fs = fs
        self._xdata = times
        self.name = os.path.basename(wavfilepath)

        # リセット
        self.slc()

        return self

    #: ----------------------------------------------------
    #: Slice
    #: ----------------------------------------------------
    def slice_time_ms(self, stms, endms):
        ss = self._ms2smp(stms)
        se = self._ms2smp(endms)
        self._slice_xdata(ss, se)
        return self

    def slice_time_smp(self, ss, se):
        self._slice_xdata(ss, se)
        return self

    def plot(self):
        import matplotlib.pyplot as plt

        plt.plot(self.get_xdata(), self.get_data())
        plt.xlabel('Time [ms]')
        plt.title(self.name)
        plt.locator_params(nbins=5, axis='x', tight=True)
        plt.locator_params(nbins=15, axis='y', tight=True, fontsize=1)
        plt.grid()

        return self

    #: ----------------------------------------------------
    #: Analys
    #: ----------------------------------------------------
    def gwt(self, *args, **kw):
        """gwt(audio_data, Fs, a_N=512, f_min=0, f_max=None):"""
        data, times, freq = self._gwt(self.get_data(), self.get_fs(), *args, **kw)
        return SpectrogramData(data, times, freq)._set_fs(self.get_fs())

    def stft(self, nwin=256, step=128):
        """
        hammingwindowでstft
        x : 入力信号(モノラル)
        win : 窓関数
        step : シフト幅
        """
        x = self.get_data()
        from scipy import hamming

        win = hamming(nwin)

        from fisig2.core.stft import stft, frange

        # FFT結果
        # X<frame, freq>
        X = stft(x, win, step)
        X = X[:, :(nwin / 2)]
        # 周波数軸
        freq = frange(nwin, self.get_fs())
        freq = freq[:(nwin / 2)]

        # サイズ確認
        Nt, Nf = X.shape

        # 時間軸(適当)
        t0, t1 = self.get_xdata()[0], self.get_xdata()[-1]

        from numpy import linspace

        times = linspace(t0, t1, Nt)

        specgram = SpectrogramData(data=X, xdata=times, ydata=freq)
        specgram.set_fs(self.get_fs())

        return specgram

    def normalizeSpl(self, Pmax, P0=20e-6):
        sig = self.get_data()
        data = Pmax * sig / P0
        self._set_data(data)
        return self

    def Afilter(self):
        import scipy.signal

        a = [1.000000000, -4.417756060, 7.777187062, -6.882221690, 3.161704960, -0.696710943, 0.057796673]
        b = [0.169099309, -0.338198619, -0.169099309, 0.676397238, -0.169099309, -0.338198619, 0.169099309]

        sig = self.get_data()
        data = scipy.signal.lfilter(b, a, sig)
        self._set_data(data)

        return self

    def filter(self, c):
        """
        TODO: 時期バージョンから追加予定
        使い方：
            フィルタリング
            import numpy as np
            import scipy.signal
            fs = 44100
            fe1 = 1000. / (fs/2.0)
            ntap = 101#(奇数)
            c = scipy.signal.firwin(ntap, fe1, pass_zero=False) # High-pass
            signal.filter(c)

        :param c:
        :return:
        """
        from numpy import convolve

        data = convolve(self.get_data(), c, "same")
        self._set_data(data)
        return self

    def fft(self, window="hanning", nfft=None):
        from numpy.fft.fftpack import fft as npfft
        from numpy.fft import fftfreq as npfftfreq
        from scipy import hamming, hanning

        sig = self.get_data()
        n = sig.shape[0]

        if window == "hamming":
            win = hamming(n)
        elif window == "hanning":
            win = hanning(n)
        elif window == "square":
            win = 1
        else:
            raise StandardError("Windows is not %s" % (window,))

        #: FFT, 折り返しこみ
        if nfft is None:
            nfft = n

        spec = npfft(sig * win, n=nfft)

        #: Freq, 折り返しこみ
        freq = npfftfreq(nfft, d=1. / self.get_fs())

        # : 折り返しを削除して返却
        se = round(nfft / 2)
        spectrum = SpectrumData(data=spec[:se], xdata=freq[:se], name=self.name)
        spectrum.set_fs(self.get_fs())

        return spectrum


if __name__ == '__main__':
    # オーディオロード
    sig = SignalData().load_wav("./test/audio.wav", 'M')

    sig.fft().info().plot().show()

    # スペクトログラム
    spgram = sig.slice_time_ms(80, 120).info().gwt()

    # スペクトル(インパクト音)
    spec_impact = spgram.slice_time_ms(20, 25).time_average()  # .plot().show()

    #

    # ガワ感
    # g = spec_impact.liftering(lif1=5, mode="low").get_data()
    # from numpy import var as npvar
    #
    # gawa = npvar(g)
    # print gawa

    # 硬さ
    katasa = spec_impact.liftering(lifter=15, mode="low").info()  # .plot().show()

    gdata1 = spec_impact.get_logpow()
    gdata2 = spec_impact.liftering(lifter=13, mode="high").get_logpow()
