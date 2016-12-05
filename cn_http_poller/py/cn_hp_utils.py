#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# file:    cn_hp_utils.py
# author:  rbw
# date:    20121001.2224
# purpose: common utilities for cn_http_poller
########################################################################
import os, sys, time
import re

#
# return current UTC time as a five member array of:
#
#   0. hour (int),
#   1. min (int),
#   2. sec (float), 
#   3. readable time string in the form
#        'Sat Sep 18 15:18:17 2010'
#   4. another readable time string in the form
#        '15:18:17.513188'
#
def get_current_utc_hms():
  dbg = False
  hmsa = []

  tnow = time.time()
  #anow = time.asctime(time.localtime(tnow))
  anow = time.asctime(time.gmtime(tnow))

  if dbg:
    print 'tnow: %f' % tnow
    print 'anow: %s' % anow

  s = tnow % 60.0
  si = int(s)

  m = (tnow / 60.0)%60.0
  mi = int(m)

  h = (tnow / (3600.0)) % 24.0
  h = (tnow / (3600.0)) % 24.0
  hi = int(h)

  aanow = ''
  if (s < 10.0):
    #print '%02d:%02d:0%06f' % (hi, mi, s)
    aanow = '%02d:%02d:0%06f' % (hi, mi, s)
  else:
    #print '%02d:%02d:%06f' % (hi, mi, s)
    aanow = '%02d:%02d:%06f' % (hi, mi, s)

  if dbg:
    print 'h:  %d' % hi
    print 'm:  %d' % mi
    print 's:  %f' % s

  hmsa.append(hi)
  hmsa.append(mi)
  hmsa.append(s)
  hmsa.append(anow)
  hmsa.append(aanow)

  return hmsa

#
# get the N most recent processed data file pathnames
#
#   base_dir: base data directory
#   n:        N (any positive integer)
#
# NOTE: this fails if there are no subdirectories in base_dir
#
def get_last_n_proc_data_files(base_dir, n=3):
  base_dir_slash = base_dir
  if (not base_dir_slash.endswith(os.path.sep)):
    base_dir_slash += os.path.sep
  data_dirs = []
  data_dirs_all = os.listdir(base_dir);

  #
  # make sure everything here is a directory and is in the form "2012"
  #
  data_dirs_all.sort()
  ps_expected_dir = "^\d{4}$"
  po_expected_dir = re.compile(ps_expected_dir)
  for dda in data_dirs_all:
    mo = po_expected_dir.match(dda)
    if (mo):
      fpath = base_dir_slash + dda
      if os.path.isdir(fpath):
        data_dirs.append(dda)

  print 'data_dirs: %s' % data_dirs
  if len(data_dirs) < 1:
    print 'WARNING: get_last_n_proc_data_files():'
    print '  dir \"%s\" has no data dirs...' % base_dir
    return([])
  last_2_data_dirs = data_dirs[-2:]

  data_dir_1 = ''
  data_dir_2 = ''
  data_dir_1_slash = ''
  data_dir_2_slash = ''

  data_dir_1 = base_dir_slash + last_2_data_dirs[0]
  if (len(last_2_data_dirs) > 1):
    data_dir_2 = base_dir_slash + last_2_data_dirs[1]

  data_dir_1_slash = data_dir_1 + os.path.sep
  if (len(last_2_data_dirs) > 1):
    data_dir_2_slash = data_dir_2 + os.path.sep
  #print 'data_dir_1_slash: %s\n' % data_dir_1_slash
  #print 'data_dir_2_slash: %s\n' % data_dir_2_slash

  data_pathnames = []
  #
  # get all pathnames in 1st and 2nd dirs
  #
  data_files_1 = os.listdir(data_dir_1);
  data_files_1.sort()
  for data_file in data_files_1:
    data_pathnames.append(data_dir_1_slash + data_file)
  if (len(last_2_data_dirs) > 1):
    data_files_2 = os.listdir(data_dir_2);
    data_files_2.sort()
    for data_file in data_files_2:
      data_pathnames.append(data_dir_2_slash + data_file)

  return data_pathnames[-n:]

#
# get the N most recent processed data items
#
#   base_dir: base data directory
#   n:        N (any positive integer)
#   since:    timestamp in the form "20120102.0501.23"
#
def get_last_n_proc_data_items(base_dir, n=20, since=''):
  data_files_l = get_last_n_proc_data_files(base_dir, 2)
  #print 'data_files_l:'
  p_cn_proc_items = [] # partial
  cn_proc_items = []   # all
  for data_file_l in data_files_l:
    p_cn_proc_items = parse_proc_items(data_file_l)
    cn_proc_items += p_cn_proc_items
    
  return cn_proc_items[-n:]


#
# parse processed data items
#
# return a list of dictionaries.  The keys of the dictionaries are:
#
#    path
#    src
#    tstamp
#    pubdate
#    author
#    guid
#    url
#    title
#    summary
#    text1
#
#
def parse_proc_items(pathname_arg):
  #print '  parse_proc_items(\"%s\")' % pathname_arg

  ##
  ## RE to match "tstamp:  20120924.0000.13"
  ##
  re_patt_str = "^(\w+\-?\w+):\s*(\S*.*)$"
  re_patt_obj = re.compile(re_patt_str)

  f = open(pathname_arg, 'r')
  item = {}
  item_list = []
  inside_item = False
  data_tag = ''
  data_txt = ''

  while True:
    line = f.readline()
    if len(line) < 1:
      break;
    line = line.rstrip()

    if line.startswith('start-item:'):
        item = {}
        tag = ''
        data = ''
        inside_item = True

    elif line.startswith('end-item:'):
      if (len(item) > 0):
        item_list.append(item)
        item = {}
        tag = ''
        data = ''
        inside_item = False
    elif inside_item:
      # check for new tag
      match_obj = re_patt_obj.match(line)
      if (match_obj):
        g1 = match_obj.group(1)
        g2 = match_obj.group(2)
        tag = g1
        data = ''
        if g2: 
          if (len(g2) > 0):
            data = g2
            item[tag] = data
          else:
            item[tag] = data
        else:
          item[tag] = data
          pass
      else:
        if item.has_key(tag):
          item[tag] += os.linesep
          item[tag] += line
        else:
          item[tag] = line

  f.close()
  return item_list

