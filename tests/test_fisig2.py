#! coding:utf-8
"""
パッケージのテスト
"""
print(__file__)

import unittest

try:
	from fisig2 import *
	import_err = False
except ImportError:
	import_err = True

class TestFisig2(unittest.TestCase):

	def setUp(self):
		pass

	def test_import(self):
		self.assertFalse(import_err, ImportError())
		pass

if __name__ == '__main__':
	unittest.main()