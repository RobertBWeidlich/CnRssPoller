#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# file:    cn_hp_thr.py 
# author:  rbw
# date:    110419.2020
# purpose: poll a single HTTP site - designed to run in a single
#          Python thread
# dependencies:
#          cn_xml_doc (make sure something like this is defined:
#
#       "export PYTHONPATH=~/Desktop/Projects2010/cn_xml_doc/py:$PYTHONPATH"
########################################################################
import sys, os
import urllib, time, re, anydbm
import threading
import random
from cn_rss_doc import CnRssDocument

class CnHpThr(threading.Thread):  # subclass of threading.Thread

  def __init__(self, id_arg, url_arg, \
               out_filename_raw_arg, out_filename_proc_arg, \
               p_file_arg, logmutex_arg):
    self.id = id_arg
    self.url = url_arg
    self.out_filename_raw = out_filename_raw_arg
    self.out_filename_proc = out_filename_proc_arg
    self.p_file = p_file_arg
    self.logmutex = logmutex_arg
    threading.Thread.__init__(self)

  def run(self):
    self.logmutex.acquire()
    #print ' >>%s starting' % self.id
    print ' >> starting %s' % self.id
    self.logmutex.release()

    #
    # 1. poll site
    #
    if False:
      print '777'
      print 'self.url:              %s' % self.url
      print 'self.out_filename_raw: %s' % self.out_filename_raw
      print '777'
    urllib.urlretrieve(self.url, self.out_filename_raw)

    #
    # 2. notify RSS post-processing utility via Unix pipe
    #
    # [commented out 110127.1153 - Unix pipes seem to be erratic...
    self.logmutex.acquire()
    try:
      self.p_file.write('%s\n' % self.out_filename_raw)
      self.p_file.flush()
    except:
      print("#WARNING: write to pipe failed")
    self.logmutex.release()

    #
    # 6. Write log info
    #
    self.logmutex.acquire()
    #print ' <<%s ending' % self.id
    print ' << ending %s' % self.id
    self.logmutex.release()

    #
    # as of 100127.2045, delete all of the following - post-processing
    # RSS data in a separate process...
    #
    return

    #
    # 2. parse discrete items (or entries, in the case of Atom)
    #    using CnRssDocument
    #
    gxp = CnRssDocument(self.out_filename_raw, False)

    #
    # extract site name from raw file name in the form
    #
    # 'cn_rss_raw-bbs.reddit.new-20110124.0013.13.xml'
    #
    fn_patt_str  = '.*cn_rss_raw-(.*)-(\d{8}\.\d{4}\.\d{2})\.xml$'
    fn_patt_obj = re.compile(fn_patt_str)
    fn_match_obj = fn_patt_obj.match(self.out_filename_raw)
    if fn_match_obj == None:
      # todo: flag as error
      return 
    src = fn_match_obj.group(1)
    tstamp = fn_match_obj.group(2)
    print('src:    %s' % src)
    print('tstamp: %s' % tstamp)

    items = gxp.getItems()
    self.logmutex.acquire()
    print('###')
    #print('gxp:')
    #print(gxp)
    print('self.out_filename_raw: %s' % self.out_filename_raw)
    for item in items:
      #
      # guid is unique ID for this item, but not all implementation define
      # it, so look for alternatives
      #
      guid = item['guid']
      if (len(guid) < 1):
        guid = item['title']
      if (len(guid) < 1):
        guid = item['description']
      #print('  item.guid: >>>%s<<<' % guid)
      if (len(guid) < 1):
        # todo: generate error message
        continue

      #
      # 3. dedup each item using anydbm
      #
      #self.isUniqueGuid(guid, src, tstamp)

    print('###')
    self.logmutex.release()

    #
    # 4. Clean text
    #

    #
    # 5. Write unique items, along with clean text, to file
    #

