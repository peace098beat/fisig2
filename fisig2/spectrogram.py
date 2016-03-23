#! coding:utf-8
"""
    fisig.spectrogram.py
    ~~~~~~~~~~~~~~~~~

    スペクトログラムクラス. 信号データから時間-周波数解析されたスペクトログラムデータ.

    例えば.
        # >>> from fisig.signal import Signal
        # >>> spectrum = Signal().load_wav("./audio.wav", channel_no=(0,)).stft()
        # >>> spectrum.info()


"""

from core import BaseData
# from fisig import SpectrumData, SpectrogramData
from fisig2.spectrum import SpectrumData


class SpectrogramData(BaseData):
    """Spectrogramクラスは, 信号データを周波数分析した結果のクラスです.
    ここでSpectrogramとは時間-周波数軸上の2次元データとなります.
    主に信号データを解析した後に生成されるため, Spectrogramクラスを直接生成することはできません.

    :propaty data ndarray<time, frequency>:

    使い方
    ----

        from fisig.spectrum import Signal

        # >>> spcgram = Signal().load_wav("./audio.wav", (0)).stft()
        # >>> spcgram.info()
        spcgram.amp
        spcgram.pow
        spcgram.logamp
        spcgram.logpow
        spcgram.f_data
        spcgram.fk_data
        spcgram.t_data
        spcgram.tms_data

    """

    def __init__(self, data, xdata, ydata):
        super(SpectrogramData, self).__init__()
        self._set_data(data)
        self._set_xdata(xdata)
        self._set_ydata(ydata)
        self.slc()

    def info(self):
        """スペクトルデータの詳細を表示します."""
        print("\n#: ------------------------------- :#")
        print("Spectrogram shape<%r,%r>" % (self.get_data().shape))
        print("times %.5f[ms]-%.5f[ms]" % (self.get_xdata()[0] * 1000, self.get_xdata()[-1] * 1000))
        print("freqs %r[Hz]-%r[Hz]" % (self.get_ydata()[0], self.get_ydata()[-1]))
        print("#: ------------------------------- :#\n")
        return self

    #: ----------------------------------------------------
    #: 補助
    #: ----------------------------------------------------
    def time_average(self):
        from numpy import mean

        data = mean(self.get_amp(), axis=0)
        freq = self.get_ydata()
        return SpectrumData(data=data, xdata=freq)

    def slice_time_ms(self, stms, endms):
        ss = self._ms2smp(stms)
        se = self._ms2smp(endms)
        self._slice_xdata(ss, se)
        return self


    def plot(self):
        import matplotlib.pyplot as plt

        # extent = self.get_xdata()[0], self.get_xdata()[-1], self.get_ydata()[0], self.get_ydata()[-1]
        extent = self.get_xdata()[0] * 1000, self.get_xdata()[-1] * 1000, self.get_ydata()[0] / 1000, self.get_ydata()[
            -1] / 1000

        plt.imshow(self.get_logpow().T, origin="lower", aspect="auto", cmap="jet", extent=extent)
        # plt.imshow(self.get_data(), origin = "lower", aspect = "auto", cmap = "hot", vmin = vmin, vmax = vmax)

        plt.xlabel('Time [ms]')
        plt.ylabel('Frequency [kHz]')

        plt.locator_params(nbins=5, axis='x', tight=True)
        plt.locator_params(nbins=15, axis='y', tight=True, fontsize=1)

        plt.grid()

        return self
