
#! coding:utf-8
"""
パッケージのテスト
"""
print(__file__)
import os
import unittest

try:
    from signaldata import SignalData
    import_err = False
except:
    import_err = True

class TestFisig2(unittest.TestCase):
    def test_signaldata_import(self):
        self.assertFalse(import_err, "from signaldata import SignalData is Error")

    def test_signaldata(self):
        rootpath = os.path.dirname(__file__)
        wav_file = os.path.normpath(os.path.join(rootpath, "tests/audio.wav"))
        self.assertTrue(os.path.exists(wav_file), wav_file)
        # オーディオロード
        sig = SignalData()
        sig.load_wav(wav_file, 'M')
        self.assertIsNotNone(sig.get_fs())
        self.assertIsNotNone(sig.get_xdata())
        self.assertIsNotNone(sig.get_data())
        self.assertTrue(sig.name, "audio.wav")


if __name__ == '__main__':
    unittest.main()