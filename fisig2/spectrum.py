#! coding:utf-8
"""
    fisig.spectrum.py
    ~~~~~~~~~~~~~~~~~

    スペクトルクラス. 信号データから周波数解析されたスペクトルデータ.

    例えば.

        # >>> spectrum = SignalData().load_wav("./audio.wav", (0)).fft()
        # >>> spectrum.info()


"""

from core import BaseData
from fisig2.core.ceps import ceps_gwt


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

    def __init__(self, data, xdata):
        super(SpectrumData, self).__init__()
        self._set_data(data)
        self._set_xdata(xdata)
        self.slc()

    def info(self):
        """スペクトルデータの詳細を表示します."""
        print("\n#: ------------------------------- :#")
        print("source path:%r" % self._source_path)
        print("xdata %r-%r" % (self.get_xdata()[0], self.get_xdata()[-1]))
        print("data shape:%r" % self.get_data().shape)
        print("#: ------------------------------- :#\n")
        return self

    def slice_freq_hz(self, start, end):
        from numpy import argmin as npargmin

        f1smp = npargmin(self.get_xdata() <= start)
        f2smp = npargmin(self.get_xdata() <= end)
        self._slice_xdata(f1smp, f2smp)

        return self

    def slice_freq_khz(self, start, end):
        self.slice_freq_hz(start * 1000, end * 1000)
        return self

    def liftering(self, lifter, mode):
        gwtd = self.get_amp()
        data = ceps_gwt(gwtd, lifter, mode)
        xdata = self.get_xdata()

        return SpectrumData(data, xdata)

    def cof(self, mode="log"):
        from numpy import sum as npsum

        if mode == "log":
            data = self.get_logpow()
        elif mode == "linear":
            data = self.get_amp()

        freq = self.get_xdata()

        c = npsum(data * freq) / npsum(data)
        return c

    def plot(self):
        import matplotlib.pyplot as plt
        from numpy import max as npmax

        mode = "logpow"
        if mode == "logpow":
            gdata = self.get_logpow()
            plt.ylabel("power [db]")

        plt.plot(self.get_xdata() / 1000., gdata)

        ymax = int(npmax(gdata) / 10) * 10 + 10
        ymin = ymax - 80

        plt.ylim(ymin, ymax)

        plt.xlabel('Frequency [kHz]')
        plt.locator_params(nbins=25, axis='x', tight=True)
        # plt.locator_params(nbins=15, axis='y', tight=True, fontsize=1)
        plt.grid()

        return self
