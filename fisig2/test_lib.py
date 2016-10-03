
#! coding:utf-8
"""
パッケージのテスト
"""
print(__file__)
import unittest

try:
	from lib.core import _load_wav, BaseData
	from lib.AudioManager import *
	from lib.blob4path import *
	import_err = False
except:
	import_err = True

class TestFisig2(unittest.TestCase):
	def test_signaldata_import(self):
		self.assertFalse(import_err, "from lib.core import * is Error")
		b = BaseData()
		self.assertIsInstance(b, BaseData)
		lw = _load_wav
		self.assertIsNotNone(lw)

if __name__ == '__main__':
	unittest.main()