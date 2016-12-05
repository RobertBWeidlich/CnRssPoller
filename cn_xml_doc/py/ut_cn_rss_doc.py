#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# file:    ut_cn_xml_doc.py
# author:  rbw
# date:    101219.2100
# purpose: Unit test for cn_xml_doc.py
########################################################################
import sys
from cn_rss_doc import CnRssDocument

def main():
  ## PSHB data

  ## RSS data
  path_101216_01_rss = \
      '/data2/cn/rss_raw/2010/12/17/01/' + \
      'cn_rss_raw-blog.andrewsullivan-20101217.0106.13.xml'
  path_101218_01_rss = \
      '/data2/cn/rss_raw/2010/12/18/23/' + \
      'cn_rss_raw-blog.andrewsullivan-20101218.2306.13.xml'
  path_101230_01_rss = \
      '/data2/cn/rss_raw/2010/12/30/01/' + \
      'cn_rss_raw-blog.andrewsullivan-20101230.0151.13.xml'
  path_20130310 = \
      '/data1/cn/rss_raw/2013/03/10/00/' + \
      'cn_rss_raw-news.washpost-20130310.0004.04.xml'

  ## Atom data
  path_101218_01_atom = \
      '/data2/cn/rss_raw/2010/12/18/23/' + \
      'cn_rss_raw-aggr.huffpost-20101218.2321.13.xml'

  ##path = path_101218_01_atom
  #path = path_101230_01_rss
  path = path_20130310

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

