#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# file:    cn_dump_nyt.py
# date:    111127.2045
# purpose: Dump all New York Times data from CN RSS processed files
#          in a given directory.
########################################################################
#import os, sys, time, re, anydbm
import sys, os
import socket

DEF_DATA_DIR_FC13 =   '/data2/cn/rss_proc/2011'
DEF_DATA_DIR_PUPPIS = '/home/polyticker/data2/cn/rss_proc/2011'

def main(dir_arg):
  print '  %s' % dir_arg

  files = os.listdir(dir_arg)
  files.sort()

  for file in files:
    path = dir_arg + os.sep + file
    process_file(path)

def process_file(path_arg):
  print path_arg


if __name__ == '__main__':
  path = ''
  if len(sys.argv) < 2:
    path = DEF_DATA_DIR_FC13
    hostname = socket.gethostname()
    #print hostname
    if hostname == 'puppis':
      path = DEF_DATA_DIR_PUPPIS

  else:
    path = sys.argv[1]

  main(path)
    
  sys.exit(1)

