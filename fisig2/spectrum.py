#! coding:utf-8
"""
    fisig.spectrum.py
    ~~~~~~~~~~~~~~~~~

    スペクトルクラス. 信号データから周波数解析されたスペクトルデータ.

    例えば.

        # >>> spectrum = SignalData().load_wav("./audio.wav", (0)).fft()
        # >>> spectrum.info()


"""

# from core.core import 
# import lib.core as lc
#_load_wav = lc._load_wav
# BaseData = lc.BaseData

# from lib.ceps import ceps_gwt

from .core import *
from .ceps import *

class SpectrumData(BaseData):
    """Spectrumクラスは, 信号データを周波数分析した結果のクラスです.
    ここでSpectrumとは周波数軸上の1次元データとなります.
    主に信号データを解析した後に生成されるため, Spectrumクラスを直接生成することはできません.

    使い方
    ----

        from fisig.spectrum import Signal

        # >>> spec = SignalData().load_wav("./audio.wav", (0)).fft()
        # >>> spec.info()
        spec.amp
        spec.pow
        spec.logamp
        spec.logpow
        spec.fdata
        spec.fkdata

    """

    def __init__(self, data, xdata, name="none"):
        super(SpectrumData, self).__init__()
        self._set_data(data)
        self._set_xdata(xdata)
        self.slc()
        self.name = name

    def info(self):
        """スペクトルデータの詳細を表示します."""
        print("\n#: ------------------------------- :#")
        print("<Spectrum Info>")
        print("source path:%r" % self._source_path)
        print("data shape:%r" % self.get_data().shape)
        print("xdata(freq) %0.1f-%0.1f [Hz]" % (self.get_xdata()[0], self.get_xdata()[-1]))
        print("xdata(smp) %d-%d [n]" % (0, self.get_data().shape[0] - 1))
        print("#: ------------------------------- :#\n")
        return self

    #: ----------------------------------------------------
    #: Slice
    #: ----------------------------------------------------
    def slice_freq_hz(self, start, end):
        self.slc()
        assert start < end, "start:%r, end:%r" % (start, end)
        from numpy import argmin as npargmin

        f1smp = npargmin(self.get_xdata() <= start)
        f2smp = npargmin(self.get_xdata() <= end)
        assert f1smp < f2smp, "f1smp:%r, f2smp:%r, start:%r, end:%r" % (f1smp, f2smp, start, end)
        self._slice_xdata(f1smp, f2smp)

        return self

    def slice_freq_khz(self, start, end):
        self.slc()
        assert start < end, "start:%r, end:%r" % (start, end)
        self.slice_freq_hz(start * 1000, end * 1000)
        return self

    #: ----------------------------------------------------
    #: Getter
    #: ----------------------------------------------------
    def get_xdata_khz(self):
        return self.get_xdata() / 1000

    def get_xdata_hz(self):
        return self.get_xdata()

    #: ----------------------------------------------------
    #: Analys
    #: ----------------------------------------------------
    def liftering(self, lifter, mode):
        gwtd = self.get_amp()
        data = ceps_gwt(gwtd, lifter, mode)
        xdata = self.get_xdata()

        return SpectrumData(data, xdata)

    def lfiltering(self, b=None, a=None):
        from scipy.signal import lfilter

        x = self.get_amp()
        # alpha = 0.1
        # xx = lfilter([alpha],[1, 1-alpha], x)
        xx = lfilter(b, a, x)

        self._set_data(xx)

        return self

    def cof(self, mode="log"):
        from numpy import sum as npsum

        data = None
        if mode == "log":
            data = self.get_logpow()
        elif mode in ("linear", 'lin'):
            data = self.get_pow()

        freq = self.get_xdata()

        c = npsum(data * freq) / npsum(data)
        return c

    def ave_power(self, mode="lin"):
        """
        事前にスライスされた帯域のスペクトルパワーの平均を算出
        :param mode:
        :return: 平均パワー[db]
        """
        from numpy import mean as npmean
        from numpy import log10 as nplog10

        power = self.get_pow()

        if mode == "lin":
            average_power = npmean(power)
            return 10*nplog10(average_power)
        elif mode == "log":
            average_power = npmean(10 * nplog10(power))
            return average_power


    def ma(self, tap=3):

        data = self.get_amp()
        data[0] = 0

        from numpy import convolve
        from numpy import ones as npones
        # ma = [1. / tap] * tap
        m = npones(tap) / tap

        res = convolve(data, m, "same")

        Spec = SpectrumData(res, self.get_xdata())
        Spec._fs = self._fs

        return Spec

    def band_power(self, f1, f2):
        """
        :param f1: 100kHz
        :param f2: 200kHz
        """
        import numpy as np

        freq = self.get_xdata_hz()
        power = self.get_pow()
        Fp5 = np.argwhere((f1 < freq) * (freq < f2))
        P5 = np.mean(power[Fp5])  # f1Hz以上のパワー
        P5 = 10 * np.log10(P5)
        return P5

    #: ----------------------------------------------------
    #: Plot
    #: ----------------------------------------------------

    def plot(self, fig=None):
        import matplotlib.pyplot as plt
        if fig == None and not isinstance(self.fig, plt.Figure):
            self.fig = plt.figure()
        else:
            self.fig = fig
        # plt.gcf(self.fig)
        plt.figure(self.fig.number)
        plt.hold(True)

        from numpy import max as npmax

        mode = "logpow"
        if mode == "logpow":
            gdata = self.get_logpow()
            plt.ylabel("power [db]")

        plt.plot(self.get_xdata() / 1000., gdata)

        ymax = int(npmax(gdata[1:]) / 10.) * 10 + 10
        ymin = ymax - 80

        plt.ylim(ymin, ymax)

        plt.xlabel('Frequency [kHz]')
        plt.locator_params(nbins=20, axis='x', tight=True)
        # plt.locator_params(nbins=15, axis='y', tight=True, fontsize=1)
        plt.grid()
        plt.title(self.name)
        return self

        #: ----------------------------------------------------
        #: EOF
        #: ----------------------------------------------------
