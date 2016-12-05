#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# file:    cn_rss_proc_batch.py
# author:  rbw
# date:    110111.2155
# purpose: Process a batch of raw RSS or Atom documents:
#            - dedup
#            - clean text
#            - store a single RSS item (or Atom feed.entry) per output
#              file
# status:  Seems to successfully process 99.9% of items.  Fails on a
#          few Huffington Post items (search for "#FAIL" in text.
#          Solution: run encode() on all text items...
########################################################################
import os, sys, re
from cn_rss_doc import CnRssDocument

# DEBUG
#start_at_20110101 = True
start_at_20110101 = False
unique_strs = {}
pdf_count = 0

def main():
  base_raw_dir =  '/data2/cn/rss_raw'
  base_proc_dir = '/data2/cn/rss_proc'

  # file match regular expression
  file_match_str  = '.*cn_rss_raw-(.*)-(\d{8}\.\d{4}\.\d{2})\.xml$'
  file_pattobj = re.compile(file_match_str)

  # year
  yr_dir_list = os.listdir(base_raw_dir)
  yr_dir_list.sort()
  if start_at_20110101:
    yr_dir_list = ['2011']
  for yr_dir in yr_dir_list:
    yr_dir_path = base_raw_dir + os.sep + yr_dir
    mon_dir_list = os.listdir(yr_dir_path)
    mon_dir_list.sort()
    for mon_dir in mon_dir_list:
      mon_dir_path = yr_dir_path + os.sep + mon_dir
      day_dir_list = os.listdir(mon_dir_path)
      day_dir_list.sort()
      for day_dir in day_dir_list:
        day_dir_path = mon_dir_path + os.sep + day_dir
        hr_dir_list = os.listdir(day_dir_path)
        hr_dir_list.sort()
        for hr_dir in hr_dir_list:
          hr_dir_path = day_dir_path + os.sep + hr_dir
          data_file_list = os.listdir(hr_dir_path)
          data_file_list.sort()
          # todo: sort chronologically, not alphabetically
          data_file_list_cron_sort = sort_filenames_cron(data_file_list)
          tstamp_str = yr_dir + mon_dir + day_dir + hr_dir;
          tstamp_i = int(tstamp_str)
          #for data_file in data_file_list:
          for data_file in data_file_list_cron_sort:
            data_file_path =  hr_dir_path + os.sep + data_file
            if file_pattobj.match(data_file):
              process_data_file(data_file_path)
            else:
              print('#WARNING:  bad file name \'%s\'' % data_file_path)
 

def process_data_file(path_arg):
  global pdf_count
  """
  Process those RSS items that are unique.  Use the unique_strs dictionary
  to store the guids of those items that have been encountered before.
  """
  ##print('%s %s %s %s %s' % (yr_arg, mon_arg, day_arg, hr_arg, path_arg))
  #print('%s' % (path_arg))

  where = 0;
  pdf_count += 1
  try:
    try:
      cn_rss_doc = CnRssDocument(path_arg, False)
      type = ''
      try:
        type = cn_rss_doc.getRssOrAtom()
      except:
        # todo: handle exception...
        print('#FAIL - cn_rss_doc.getRssOrAtom()')
      print('#processing %s (%s)' % (path_arg, type))
    except:
      #print('#FAIL process_data() - 1: path_arg=\'%s\'' % path_arg)
      return
    try:
      items = cn_rss_doc.getItems()
    except:
      print('#FAIL process_data() - 2: cn_rss_doc.getItems() failed')
      return
    for item in items:
      try:
        #print('%d 114' % pdf_count)
        #print('processing \'%s\'' % path_arg)
        ## WTF?!? ## cn_rss_doc = CnRssDocument(path_arg, False)
        #print('%d 115' % pdf_count)
        title = item['title']
        guid = item['guid']
        guid_hash = hash(guid)
        #print('%d 116' % pdf_count)
      except:
        print('#FAIL-12')
      ##
      ## test if guid is unique
      ##
      try:
        #print('%d 117' % pdf_count)
        if unique_strs.has_key(guid_hash):
          #print('..... 0x%016x: %s' % (guid_hash, guid))
          #print('.....  %d: %s' % (guid_hash, guid))
          pass
        else:
          unique_strs[guid_hash] = 1
          write_output(path_arg, item)
        #print(guid)
        #print('0x%016x: %s' % (guid_hash, guid))
      except:
        print('#FAIL-13 - guid_hash = 0x%016x: %s' % guid_hash)
        return
  except:
    # todo: handle exception...
    print('#FAIL...1')

def write_output(path_arg, item_arg):
  #
  # pull date from path_arg, which is expected to be in the form
  #
  #   '/data2/cn/rss_raw/2010/09/28/05/' +
  #   'cn_rss_raw-aggr.memeo.top-20100928.0533.13.xml'
  #
  pstr = '.*cn_rss_raw-(.*)-(\d{8}\.\d{4}\.\d{2})\.xml'
  #pstr = '.*(cn)_(rss)'
  pattobj = re.compile(pstr)
  matchobj = pattobj.match(path_arg)
  try:
    source = matchobj.group(1)
    tstamp = matchobj.group(2)
  except:
    # todo: handle exception...
    print('#FAIL: write_output(); path=\'%s\'' % path_arg)
    return

  ##
  ## quick kludge to remove reddit
  ##
  #if (source == 'bbs.reddit.new'):
  #  return

  print('start-item:')
  print('path:    %s' % path_arg)
  print('src:     %s' % source)
  print('tstamp:  %s' % tstamp)
  #print('item_arg:')
  #print(item_arg)
  #print('x:  %s' % item_arg['x'])
  print('pubdate: %s' % item_arg['pubdate'])
  print('author:  %s' % item_arg['author'])
  print('guid:    %s' % item_arg['guid'])
  print('url:     %s' % item_arg['url'])
  # todo: clean all text
  #print('title:   %s' % item_arg['title'])
  text_title_clean = clean_text(item_arg['title'])
  try:
    print('title:   %s' % text_title_clean)
  except:
    try:
      print('title:   %s' % text_title_clean.encode('latin-1', 'replace'))
      # todo: this inserts '?' in place of Unicode characters > 0xff
      #print('title:   %s' % text_title_clean.encode('latin-1'))
    except:
      print('#ERROR: can\'t print text_title_clean....')
      print('#  type(text_title_clean): %s' % type(text_title_clean))
      print('#  len(text_title_clean):  %d' % len(text_title_clean))
      hstr = hexdump(text_title_clean)
      print(hstr)
  print('summary: %s' % item_arg['summary'])
  #print('text:    %s' % item_arg['text'])
  text1 = clean_text(item_arg['text'])
  try:
    print('text1:   %s' % text1)
  except:
    try:
      #print('text1:   %s' % text1.encode('latin-1'))
      # todo: this inserts '?' in place of Unicode characters > 0xff
      print('title:   %s' % text_title_clean.encode('latin-1', 'replace'))
    except:
      print('#ERROR: can\'t print text1....')
      print('#  type(text1): %s' % type(text1))
      print('#  len(text1):  %d' % len(text1))
      #print('text1:   %s' % text1.encode('latin-1'))
      hstr = hexdump(text1)
      print(hstr)

  #print('x:  %s' % item_arg['x'])
 
  print('end-item:')
  print('')

def clean_text(text_arg):
  ##
  ## 1. delete all html markup -- anything enclosed in '<' and '>' characters
  ##
  str_new = ''
  sstate = True
  for c in text_arg:
    if c == '<':
      sstate = False
      continue
    if c == '>':
      sstate = True
      str_new += ' '
      continue
    if sstate:
      str_new += c
  #return str_new.strip()

  str1 = str_new.strip()
  #return str1

  ##
  ## 9. line wrap
  ##
  str2 = ''
  l_count = 0
  str2 += '\n '
  for c in str1:
    str2 += c
    if (l_count > 71) and (c == ' '):
      str2 += '\n' # use os-independent newline
      str2 += ' ' # use os-independent newline
      l_count = 0
    l_count += 1
    
  return(str2)

def hexdump(str_arg):
  """
  return string consisting of hexdump of str_arg
  """
  dstr = '#'
  ci = 0
  for c in str_arg:
    dstr += ' %02x' % ord(c)
    ci += 1
    if (ci % 16) == 0:
      dstr += '\n#'
  return(dstr)

def sort_filenames_cron(fn_list_arg):
  """
  sort filelist chronologically.  expect filenames in the form:
  
    'cn_rss_raw-news.washpost-20110101.0004.13.xml'

  """
  cron_list = []
  cron_dict = {}

  for fn in fn_list_arg:
    #print(' %s' % fn)
    #
    # 1. pull out timestamp and source
    #
    pstr = '.*cn_rss_raw-(.*)-(\d{8}\.\d{4}\.\d{2})\.xml'
    #pstr = '.*(cn)_(rss)'
    pattobj = re.compile(pstr)
    matchobj = pattobj.match(fn)
    #print('matchobj: %s' % matchobj)
    try:
      source = matchobj.group(1)
      tstamp = matchobj.group(2)
    except:
      continue
    #print('source: %s' % source)
    #print('tstamp: %s' % tstamp)
    #print('aaa')
    ts_key = '%s.%s' % (tstamp, source)
    #print('ts_key:   %s' % ts_key)
    #print('bbb')
    #print('%s \t%s' % (ts_key, fn))
    #print('ccc')

    #
    # 2. enter in hash, using timestamp + source as key
    #
    cron_dict[ts_key] = fn

  #
  # 3. sort keys alphabetically, then build out_list
  #
  #print('')
  #print('cron_dict:')
  #print(cron_dict)
  #print('')
  cron_dict_keys = cron_dict.keys()
  cron_dict_keys.sort()
  #print('cron_dict_keys')
  #print(cron_dict_keys)
  for cron_dict_key in cron_dict_keys:
    cron_list.append(cron_dict[cron_dict_key])
  
  #print('')
  #print('cron_list:')
  #print(cron_list)
  #for c in cron_list:
  #  print('  %80s' % c)
  #print('')

  return cron_list

if __name__ == '__main__':
  main()

