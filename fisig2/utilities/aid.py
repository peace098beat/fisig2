#! coding:utf-8
"""
aid.py

NumPyから最高のパフォーマンスを得る方法
http://kaisk.hatenadiary.com/entry/2015/02/19/224531

Created by 0160929 on 2016/04/05 15:49
"""
__all__ = ["aid"]
def aid(x):
    # この関数は配列のメモリブロックアドレスを返します
    return x.__array_interface__['data'][0]