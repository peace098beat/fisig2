#! coding:utf-8
"""
    fisig.signal.py
    ~~~~~~~~~~~~~~~

    シグナルクラス. 信号データクラス. wavファイルやcsv等から読み込んだ1次元データ
    に対して, 信号処理を行うことができる.

"""

from core import _load_wav, BaseData, _gwt
from fisig.spectrogram import SpectrogramData


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

        # リセット
        self.slc()

        return self

    def slice_time_ms(self, stms, endms):
        ss = self._ms2smp(stms)
        se = self._ms2smp(endms)
        self._slice_xdata(ss, se)
        return self

    def gwt(self):
        data, times, freq = _gwt(self.get_data(), self.get_fs())
        return SpectrogramData(data, times, freq)._set_fs(self.get_fs())

    def plot(self):
        import matplotlib.pyplot as plt

        plt.plot(self.get_xdata(), self.get_data())
        plt.xlabel('Time [ms]')
        plt.locator_params(nbins=5, axis='x', tight=True)
        plt.locator_params(nbins=15, axis='y', tight=True, fontsize=1)
        plt.grid()

        return self


if __name__ == '__main__':
    # オーディオロード
    sig = SignalData().load_wav("./test/audio.wav", 'M')
    # スペクトログラム
    spgram = sig.slice_time_ms(80, 120).gwt()
    # スペクトル(インパクト音)
    spec_impact = spgram.slice_time_ms(20, 25).time_average()#   .plot().show()

    #

    # ガワ感
    # g = spec_impact.liftering(lif1=5, mode="low").get_data()
    # from numpy import var as npvar
    #
    # gawa = npvar(g)
    # print gawa

    # 硬さ
    katasa = spec_impact.liftering(lifter = 15, mode="low").info()#.plot().show()

    gdata1 = spec_impact.get_logpow()
    gdata2 = spec_impact.liftering(lifter=13, mode="high").get_logpow()

    from matplotlib import pyplot as plt
    plt.plot(gdata1)
    plt.plot(gdata2)
    plt.show()