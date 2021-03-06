#! coding:utf-8
"""
core.py

Created by 0160929 on 2016/03/23 10:16
"""
from numpy import empty, abs, log10
from .AudioManager import AudioManager

__all__ =["_load_wav","BaseData"]

def _load_wav(filepath, data_ch):
    am = AudioManager(filepath)
    fs = am.getFs()
    times = am.getTimes()

    if am.is_wavdata_channels(ch=1):
        data = am.getData()
    elif am.is_wavdata_channels(ch=2):
        data = am.getData(data_ch)
    else:
        data = empty([])

    del am

    return data.copy(), fs, times


class BaseData(object):
    def __init__(self):
        self._source_path = None
        self._fs = None

        self._data = None
        self._xdata = None
        self._ydata = None

        self._x_ss = None
        self._x_es = None

        self._y_ss = None
        self._y_es = None

        self.fig = None

        pass

    def info(self):
        # print("\n#: ------------------------------- :#")
        # print("#: ------------------------------- :#\n")
        return self

    #: ----------------------------------------------------
    #: Slice
    #: ----------------------------------------------------
    def _slice_xdata(self, start, end):
        assert start < end, "start:%r, end:%r" % (start, end)
        self._x_ss = start
        self._x_es = end

    def _slice_ydata(self, start, end):
        assert start < end, "start:%r, end:%r" % (start, end)
        self._y_ss = start
        self._y_es = end

    def _slice_clear_x(self):
        self._x_ss = 0
        self._x_es = self._xdata.shape[0]

    def _slice_clear_y(self):
        self._y_ss = 0
        self._y_es = self._ydata.shape[0]

    def slc(self):
        if self._xdata is not None:
            self._slice_clear_x()
        if self._ydata is not None:
            self._slice_clear_y()
        return self

    def slice_time_smp(self, start, end):
        pass

    def slice_freq_smp(self, start, end):
        pass  # helper

    def slice_time_ms(self, start, end):
        pass

    def slice_freq_hz(self, start, end):
        pass

    def slice_freq_khz(self, start, end):
        pass

    #: ----------------------------------------------------
    #: 単位変換
    #: ----------------------------------------------------

    def _ms2smp(self, ms):
        return int(ms / 1000. * self._fs)

    def _smp2ms(self, smp):
        return float(smp) / float(self._fs) * 1000.

    #: ----------------------------------------------------
    #: 物理量
    #: ----------------------------------------------------
    def get_amp(self):
        # return abs(self.get_data())
        from numpy import clip

        amp = abs(self.get_data())
        # 最小値は20*log10(1e-8)=-160
        clip(amp, a_min=1e-8, a_max=1e32, out=amp)
        return amp

    def get_pow(self):
        return self.get_amp() ** 2

    def get_logamp(self):
        raise Warning("It is LogAmp 10log10(x) not LogPower 20log10(x)")
        return 10 * log10(self.get_amp())

    def get_logpow(self):
        return 20 * log10(self.get_amp())

    def get_pow_norm(self):
        return self.get_pow() / sum(self.get_pow()) * self.get_pow().flatten().size

    def get_logpow_norm(self):
        return 20 * log10(self.get_pow_norm())

    #: ----------------------------------------------------
    #: Getter
    #: ----------------------------------------------------
    def get_source_path(self):
        return self._source_path

    def get_fs(self):
        return self._fs

    def get_data(self):
        if self._data.ndim == 1:
            return self._data[self._x_ss:self._x_es].copy()
        elif self._data.ndim == 2:
            return self._data[self._x_ss:self._x_es, self._y_ss:self._y_es].copy()

    def get_xdata(self):
        return self._xdata[self._x_ss:self._x_es].copy()

    def get_xlogdata(self):
        return 10 * log10(self.get_xdata())

    def get_ydata(self):
        return self._ydata[self._y_ss: self._y_es].copy()

    #: ----------------------------------------------------
    #: Setter
    #: ----------------------------------------------------
    def set_fs(self, fs):
        self._fs = fs
        return self

    #: ----------------------------------------------------
    #: Private Setter
    #: ----------------------------------------------------
    def _set_data(self, data):
        self._data = data.copy()
        return self

    def _set_xdata(self, xdata):
        self._xdata = xdata.copy()
        return self

    def _set_ydata(self, ydata):
        self._ydata = ydata.copy()
        return self

    def _set_fs(self, fs):
        self._fs = fs
        return self

    #: ----------------------------------------------------
    #: Plot
    #: ----------------------------------------------------
    def plot(self):
        import matplotlib.pyplot as plt

        # self.fig = plt.figure()
        return self

    def show(self):
        import matplotlib.pyplot as plt

        plt.show()
        return self

    def close(self):
        if self.fig:
            self.fig.clf()
        return self

    def save(self):
        import matplotlib.pyplot as plt
        if isinstance(self.fig, plt.Figure):
            self.fig.savefig(self.name)
        else:
            raise IOError("savefig")

    def get_fig(self):
        return self.fig

    #: ----------------------------------------------------
    #: Analys
    #: ----------------------------------------------------
    def fft(self):
        pass

    def _gwt(self, *args, **kw):
        from .gwt import gwt

        """gwt analysis
            gwt(audio_data, Fs, a_N=512, f_min=0, f_max=None):
        """
        # print "_gwt", self.get_fs()
        return gwt(*args, **kw)

    def stft(self):
        pass
