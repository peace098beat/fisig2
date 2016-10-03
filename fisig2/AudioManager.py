# -*- coding: utf-8 -*-
"""AudioManager.py
アプリケーションのオーディオ機能を管理するクラス。
再生・信号データ・Fsの管理。

Property:
    filename:   ファイル名
    filepath:   ファイルパス
    sampwidth:  ファイルサイズ[byte]
    channels:   チャンネル数(モノラル:1,ステレオ:2)
    fs:         サンプリングレート
    framsize:   オーディオフレーム数
    data:       (Numpy 1D Array)wavデータ配列

Method:
    play():     オーディオの再生
    set_wav():  wavファイルを設定
    getFs():    fsを取得
    getData():  オーディオデータを返却(max1で正規化)
    getTimes():  時間配列

Example:
    file_path_1 = './audio1.wav'
    am = AudioManager(file_path_1)
    am.play(volume=0.5, play_channel='mono')
    data = am.data(data_ch='R')


Reference:
    <wave: http://docs.python.jp/2/library/wave.html>

(2016/03/23) ver2.1 時間配列データの返却
(2016/03/03) ver2.0 返却データ部分を改良(bit数で正規化したデータのみを返却)
(2105/12/11) ver1.2 Channel選択機能追加
(2105/12/11) ver1.1 Volume設定機能追加
"""
__version__ = '2.0'

import os.path
import wave
import sndhdr
import warnings

import numpy as np
import pyaudio


class AudioManager(object):
    def __init__(self, filepath=None):

        # プロパティ
        self.filepath = None
        self.filename = None
        self.data_raw = None
        self.data = None
        self.data_n = None
        self.wf = None

        if filepath is None:
            return

        # ファイルが存在しない場合は何もしない
        if os.path.exists(filepath):
            self.filepath = filepath
            self.filename = os.path.basename(self.filepath)
            self.set_wav(self.filepath)
        else:
            warnings.warn("file is not exists")

    def set_wav(self, filepath):
        """waveファイルの読み込み
        疑似ファイル(画像等)を.wavで読み込ますと、waveパッケージの方で
        エラーを出力してしまう。ファイル拡張子のエラーに対応している。
        """
        # ファイルが存在しない場合は返却
        if not os.path.exists(filepath):
            raise StandardError("File is not exist %s" % (filepath))
            return

        # ファイル名の取得
        filename = os.path.basename(filepath)

        # wavファイルかどうかを調べる(疑似ファイルならエラー)
        if sndhdr.what(filepath)[0] is not 'wav':
            return

        # オーディオファイルであれば
        try:
            # ファイルオープン
            wf_tmp = wave.open(filepath, 'rb')
        except IOError:
            raise StandardError("Cant file load %s" % (filename))
        else:
            # 正常時の処理
            self.wf = wf_tmp
            self.filename = filename
            self.filepath = filepath

            # サンプルサイズ[byte]
            self.sampwidth = self.wf.getsampwidth()
            # チャンネル数(モノラル:1,ステレオ:2)
            self.channels = self.wf.getnchannels()
            # サンプリングレート
            self.fs = self.wf.getframerate()
            # オーディオフレーム数
            self.framsize = self.wf.getnframes()
            # self.data_rawのセット
            self.__set_data()
            # wevファイル情報の表示
            self.__printWaveInfo()
        finally:
            pass

    def __set_data(self):
        """
        waveファイルをNumpy配列に変換し、
        dataプロパティに格納
        """
        # ファイルポインタをオーディオストリームの先頭に戻す
        self.wf.rewind()
        # バッファの格納(バイト文字列)
        wbuffer = self.wf.readframes(self.wf.getnframes())
        # ファイルポインタをオーディオストリームの先頭に戻す
        self.wf.rewind()

        # Numpy配列に変換
        # バイナリなので2バイトずつ整数(-32768-32767)にまとめる
        bit = self.sampwidth * 8
        if bit == 8:
            self.data_raw = np.frombuffer(wbuffer, dtype="int8")
        elif bit == 16:
            self.data_raw = np.frombuffer(wbuffer, dtype="int16")
        elif bit == 32:
            self.data_raw = np.frombuffer(wbuffer, dtype="int32")
        elif bit == 24:
            # 24bit データを読み込み、16bitに変換
            self.data_raw = np.frombuffer(wbuffer, 'b').reshape(-1, 3)[:, 1:].flatten().view('i2')
        else:
            print('Wargning!!!!!!! bit %d is none' % bit)

    def __printWaveInfo(self):
        """WAVEファイルの情報を表示"""
        # print ""
        # print "-------------------------"
        # print "ファイル名:", self.filename
        # print "チャンネル数:", self.wf.getnchannels()
        # print "サンプル[Byte]:", self.wf.getsampwidth()
        # print "サンプリング周波数:", self.wf.getframerate()
        # print "フレーム数:", self.wf.getnframes()
        # print "パラメータ:", self.wf.getparams()
        # print "長さ（秒）:", float(self.wf.getnframes()) / self.wf.getframerate()
        # print "振幅幅", (2 ** 8) ** self.sampwidth / 2 - 1
        # print "-------------------------"
        # print ""
        pass

    def play(self, play_channel, boost_db=0):
        """Play Audio by PyAudio
        :param: volume : 音量[0,1]
        :param: play_channel : 'left', 'right', 'mono', 'stereo'
        """
        if self.wf is None:
            raise StandardError("AuudioManager cant play. wave object is None")

        # print '\n== Audio:play run.. =='
        # print('>>Audio Channel :: %s' % play_channel)
        # print('>>Audio volume :: %s' % boost_db)

        p = pyaudio.PyAudio()

        def callback(in_data, frame_count, time_info, status):
            data = self.wf.readframes(frame_count)
            sig = pcmToFloat(byteToPCM(data, self.sampwidth))

            return (data, pyaudio.paContinue)

        def callback_vol_ctrl(in_data, frame_count, time_info, status):
            """
            ボリュームブースト機能の追加
            サンプル幅(bit数)に合っているか分からないで注意
            """
            # https://gist.github.com/peace098beat/e00e30e10cb6b8ff753c
            data = self.wf.readframes(frame_count)
            # バイナリデータからFloatへ変換
            sig = pcmToFloat(byteToPCM(data, self.sampwidth))

            # db分だけブースト
            db = boost_db
            sig = sig * (10. ** (db / 20.))
            # クリップしているかのチェック
            if sig.max() > 1:
                print('WARNING! : CLIP AUDIO:')

            # Channel選択
            if play_channel is 'L':
                sig[1::2] = sig[0::2]
            elif play_channel is 'R':
                sig[0::2] = sig[1::2]
            # モノラル化
            elif play_channel is 'M':
                sig[1::2] = (sig[0::2] + sig[1::2]) / 2
                sig[0::2] = (sig[0::2] + sig[1::2]) / 2
            elif play_channel is 'S':
                # 何もしなければオーディオのまま
                pass
            else:
                # 何もしなければオーディオのまま
                raise StandardError("Cant play_channel '%s' : => 'L','R','M','S'. " % (play_channel))

            # PCMからFloatへ変換
            sig_pcm = floatToPCM(sig)
            # PCMからバイナリへ変換
            playdata = (sig_pcm.tostring())

            return (playdata, pyaudio.paContinue)

        stream = p.open(
            format=p.get_format_from_width(self.sampwidth),
            channels=self.channels,
            rate=self.fs,
            output=True,
            stream_callback=callback_vol_ctrl)

        # 改善の余地あり main()の場合は、これじゃないと回らない
        if __name__ == '__main__':
            print('>>Audio Play :: __main__ Mode ')
            stream.start_stream()
            while stream.is_active():
                import time

                time.sleep(0.1)

            stream.stop_stream()
            stream.close()
            p.terminate()

        # print '== Audio:play ..end =='

        # ファイルポインタをオーディオストリームの先頭に戻す
        self.wf.rewind()

    def getFs(self):
        return self.fs

    def getData(self, data_ch=None):
        """
        オーディオデータの返却
        ver2.0からはチャンネルの選択が必須になる
        :param ch: L:left, R:right, M:mono
        :return: self.data <1D Array>
        """
        # 返却データの生成 ※ 強制的に1チャンネル分の1次元データとして返却
        self.data = np.array([])
        if self.channels == 1:
            # wavデータが1チャンネルの場合の処理
            # ロードしたデータをそのまま返却
            self.data = np.array(self.data_raw[:])

        if self.channels == 2:
            # wavデータが2チャンネルの場合の処理
            # 0:Left, 1:Right, 2:Moneとして1次元データを返却
            if data_ch == 'L':
                self.data = np.array(self.data_raw[::2])
            elif data_ch == 'R':
                self.data = np.array(self.data_raw[1::2])
            elif data_ch == 'M':
                right = np.array(self.data_raw[::2])
                left = np.array(self.data_raw[1::2])
                self.data = (right + left) / 2.
            else:
                raise StandardError("Cant data_ch '%s' : => 'L','R','M'  " % (data_ch))

        # 離散かされているので，[0,1]に正規化
        amp = (2. ** 8) ** self.sampwidth / 2 - 1
        if self.sampwidth * 8 == 24:
            # 24bitの場合の特別処理 ※24bitのオーディオデータは実装の都合上16bit化している.
            byte = 2.
            amp = (2. ** 8) ** byte / 2 - 1

        self.data = self.data / float(amp)
        # print type(self.data)

        return self.data

    def getTimes(self):
        return np.linspace(0, float(self.wf.getnframes()) / self.wf.getframerate(), self.wf.getnframes())

    def is_wavdata_channels(self, ch):
        return ch == self.channels


## UTILITY
def byteToPCM(data, sample_width):
    d_type = 'float'
    if sample_width == 2:
        d_type = 'short'
    return np.frombuffer(data, dtype=d_type)


def pcmToFloat(sig, type='float32'):
    sig = np.asarray(sig)
    if sig.dtype.kind != 'i':
        raise TypeError('signal must be integer')
    type = np.dtype(type)
    if type.kind != 'f':
        raise TypeError('type must be float')

    return sig.astype(type) / type.type(-np.iinfo(sig.dtype).min)


def floatToPCM(sig, dtype='int16'):
    return (sig * np.iinfo(dtype).max).astype(dtype)


# def byte24bitToPCM(data):
#     return np.frombuffer(data, 'b').reshape(-1, 3)[:, 1:].flatten().view('i2')
#     pass

def main():
    path = '../test/audio.wav'
    am = AudioManager(path)
    am.play(boost_db=5, play_channel='L')
    am.play(boost_db=5, play_channel='R')
    am.play(boost_db=5, play_channel='S')
    am.play(boost_db=5, play_channel='M')

    if am.is_wavdata_channels(ch=1):
        data = am.getData()
    elif am.is_wavdata_channels(ch=2):
        data = am.getData(data_ch='R')
        data = am.getData(data_ch='L')
        data = am.getData(data_ch='M')

    # print am.getTimes()
if __name__ == '__main__':
    main()
