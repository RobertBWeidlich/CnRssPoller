#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################
# file:    cn_analyze_proc_file.py
# author:  rbw
# date:    Sat Mar  9 21:22:03 EST 2013
# purpose: analyze data in CN RSS processed files
################################################################
import os, sys
from cn_hp_utils import parse_proc_items

def cn_analyze_proc_file(proc_file_arg):
  proc_file = proc_file_arg
  items = parse_proc_items(proc_file)
  #print type(items)
  #print len(items)
  count_by_src = {}

  print '##'
  print '## 1. RSS sources:'
  print '##'
  for item in items:
    #print item
    print item['tstamp'], item['src']
    src = item['src']
    if count_by_src.has_key(src):
      count_by_src[src] += 1
    else:
      count_by_src[src] = 1
  print ''

  #print count_by_src
  #print ''
  keys = count_by_src.keys()
  ##print keys

  ##
  ## sort by keys (src name)
  ##
  print '##'
  print '## 2. sort by keys (name of src)'
  print '##'
  keys.sort()
  for key in keys:
    print "%s %d" % (key, count_by_src[key])
  print ''

  ##
  ## sort by values (src count)
  ##
  print '##'
  print '## 3. sort by values'
  print '##'

  for k in sorted(count_by_src, key=count_by_src.get, reverse=True):
    print "%s %d" % (k, count_by_src[k])
  print ''


if __name__ == '__main__':
  if len(sys.argv) < 2:
    sys.stderr.write("usage: %s <cn-rss-proc-file>\n" % sys.argv[0])
    sys.exit(1)

  proc_file = sys.argv[1]
  #main(proc_file)
  cn_analyze_proc_file(proc_file)

