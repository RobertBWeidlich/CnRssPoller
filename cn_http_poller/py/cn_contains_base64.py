#!/usr/bin/env python3
# -*- coding: utf-8 -*-
########################################################################
# file:    cn_contains_base64.py
# author:  rbw
# date:    Mon Feb 15 13:40:54 EST 2021
# purpose: detect a base64-encoded string in text
########################################################################
import os, sys

t = True
f = False
b64map = [f, f, f, f, f, f, f, f, f, f, f, f, f, f, f, f,  # 0x00 - 0x0f
          f, f, f, f, f, f, f, f, f, f, f, f, f, f, f, f,  # 0x10 - 0x1f
          f, f, f, f, f, f, f, f, f, f, f, t, f, f, f, t,  # 0x20 - 0x2f
          t, t, t, t, t, t, t, t, t, t, f, f, f, f, f, f,  # 0x30 - 0x3f
          f, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t,  # 0x40 - 0x4f
          t, t, t, t, t, t, t, t, t, t, t, f, f, f, f, f,  # 0x50 - 0x5f
          f, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t,  # 0x60 - 0x6f
          t, t, t, t, t, t, t, t, t, t, t, f, f, f, f, f]  # 0x70 - 0x7f
b64map_sz = len(b64map)


#
# return True if max or more contiguous base64 characters can be found in
# string s
#
def cn_contains_base64(s, max):
    bb = bytearray(s)
    bblen = len(bb)
    count = 0
    for i in range(bblen):
        if b64map[bb[i]] == True:
            count += 1
            if count >= max:
                return True
        else:
            count = 0

        print(str(bb[i]), " ", b64map[bb[i]], count)

    return False


if __name__ == '__main__':
    # note the new lines in this string don't count as base64
    s01 = \
        """wN4h05OQ4cVvDWGFTxC5oNo1inC915/d7nnUUtLnp1ZRqqo5y/X+HibuoN1Ww7o/D3uPywW2lp5B
        Blb+aIgDNPyKqEr3cxLsauHOXDyHDhOrkFtGHCppNoWhOFB3QGxvowRlDy9qjxD0HBpFoCxCxEXI
        A8pgJkdUagqk/n+bUurkXc5p6vdGaJuiNJOjg6vMgB0/VON4NKcE3ydujeMC3Bm0Q+o4vb/F4vv4
        HRgyxfHNYcLFzlufvHeA0e3iKhQwey5/LaQM6aCrJZHqfD0NgeZlNDJRBbnh0JXXoKMf+d93Itr2
        3+UQPZXNXf1PHQ8upAytsZkUFkLDP9iUFzWvLil49EbjZNzvnLcjhfdIfUGaj+NGXV9qcmyEbDop
        m/3rC8Wbu/qA0u7mwFnJxINndOhceuk5fbt2h5aQlg97KXPJPaKUTY2RIAoGm8tNSpGCZeH+422P
        p6d2sWttIb7/+DjHM5IbHOSdulj91iuMdaOrL4KLvL5bW8Nu5dOawHP8zCD19Xad0v5hMBr5llQc
        1ZN9dDfFBMpxWeEzvpDCBAw+YVMn8BxdpfdRZQqXf8DzcxHNlk3L1rvm2j6tvroE7QovpIcMcM/6
        8zYR2TPCa3DmRnEaUbLp27feWkoQoNrpDMWH55MUsctbqXXxNcZu8ANKipj10FyEdFXeJu2yVezL
        ZG7N21LFxrvqbvhxpTEjFVCmR5T5ZjB5z4Dm04TMTX1UjALNkxb3hvjyd0HCuY6xOkuengldIOeq
        T02s+ZgV/6vJXzuNW526gxs7h0W+e7B4Cnn535KqBppIBCiD141KR5dd27dJbODECF+bZuOHZ9iy
        ee+Aadh81d2Mp/sibkEktcfToUBKgsxyp81iqD+DI0qsmqS+WXNb19IRDsDNVYYW7dFlLLXzLZPC
        qika5LOw3WmAURBD4lDpEw+cgHuP+SECM5ITrPvqGz7Vfvj9BpwKpy8q3IfJNl4dS2sTA2F6BSML
        BZXum3+vfI2wl434QjASOzi"""
    is_base64 = cn_contains_base64(s01, 70)
    print("is_base64: ", is_base64)
