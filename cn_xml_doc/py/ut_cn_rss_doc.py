#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# file:    ut_cn_xml_doc.py
# author:  rbw
# date:    101219.2100
# purpose: Unit test for cn_xml_doc.py
########################################################################
import os, sys
from cn_rss_doc import CnRssDocument

def main():
  cd = os.getcwd()
  print "current directory: " + cd

  data_dir = "../../resources/data/"
  path_01 = data_dir + "cn_rss_raw-news.latimes-20180113.2304.13.xml"
  path_02 = data_dir + "cn_rss_raw-news.sweden.thelocal-20180113.2304.13.xml"
  path_03 = data_dir + "cn_rss_raw-news.upi-20180113.2305.13.xml"
  path_04 = data_dir + "cn_rss_raw-news.washpost.world-20180113.2307.13.xml"

  path = path_04

  print 'testing on file \"%s\"' % path

  gxp = CnRssDocument(path, False)
  #gxp = CnRssDocument(path, True)

  print 'type: %s' % gxp.getRssOrAtom()

  print('###Items###')
  items = gxp.getItems()
  for item in items:
    #print('########')
    #print('item:')
    #print(item)
    #print('########')
    print('title:')
    print(' %s' % item['title'])
    print('text:')
    print(' %s' % item['text'])
    print('guid:')
    print(' %s' % item['guid'])
    print('pubdate:')
    print(' %s' % item['pubdate'])
    print('url:')
    print(' %s' % item['url'])
    print('author:')
    print(' %s' % item['author'])
    print('summary:')
    print(' %s' % item['summary'])

  sys.exit(0)

if __name__ == '__main__':

  main()

