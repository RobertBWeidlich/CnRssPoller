#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# file:    cn_dump_dbm.py
# author:  rbw
# date:    110216.1920
# purpose: Dump dbm file
########################################################################
import os, sys, time, re, anydbm

def main(dbm_file):
  #print('  %s' % dbm_file)
  db = anydbm.open(dbm_file, 'r')
  keys = db.keys();
  for key in keys:
    #print(key)
    #print('%s = %s' % (key, db[key]))
    print('%-16s %s' % (db[key], key))

if __name__ == '__main__':
  if len(sys.argv) < 2:
    sys.stderr.write("usage: %s <dbm-file>\n" % sys.argv[0])
    sys.exit(1)

  #cfg_file = sys.argv[1]
  #main(cfg_file)

  main(sys.argv[1])


