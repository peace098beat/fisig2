#! coding:utf-8
"""
__init__.py


(2016/03/22) ver0.0 たたき台を作成

Created by fifi  (2016/03/22 20:07)
"""
# __version__ = '0.0'
# print("> Load fisig2")

# __all__ =['SignalData','SpectrumData','SpectrogramData', 'timewatch']

# from . import signaldata
# from signaldata import SignalData
import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
print(sys.path)

from signaldata import SignalData
from spectrum import SpectrumData
from spectrogram import SpectrogramData
# from utilities import timewatch

if __name__ == '__main__':
	s = SignalData()
	print(s)