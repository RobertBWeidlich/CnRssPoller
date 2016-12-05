#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# file:    cn_proc_rss_to_html.py
# author:  rbw
# date:    111021.2021
# purpose: Simple conversion of CN processed RSS data to HTML table
# note:    Some "text1" fields don't have spaces in the first lines...
#          This could bread this if the first token ends in the
#          ':' character.
########################################################################
import sys, os
import time, re

DEF_DATA_DIR =   '/data2/cn/rss_proc'
HTML_FILE_PATH = '/tmp/cn.html'

def main(dir_arg):
  
  loopi = 0

  while True:
    """
    1.  Delay
    """
    if loopi > 0:
      time.sleep(60)
    loopi += 1

    """
    2.  find last RSS processed file
    """
    curr_cn_rp_path = getCurrentCNRssProcPath(dir_arg)

    """
    3.  convert all records to list of dictionaries
    """
    if True:
      print 'curr_cn_rp_path: %s ' % curr_cn_rp_path
    data_lod = parse_cn_rss_proc_file(curr_cn_rp_path)

    """
    4.  last N records
    """

    """
    5.  convert to HTML
    """
    data_html = proc_html(data_lod)

    """
    6.  move file to httpd data directory
    """
    print 'end of loop: %d' % loopi
    print '[Debugging exit]'
    sys.exit(1)

def getCurrentCNRssProcPath(base_data_dir):
  fn_patt_obj_y4 = re.compile('^\d{4}$')  ## match year string '2011'

  ##
  ## match CN RSS processed file 'cn_rss_proc-20111001.txt'
  ##
  fn_patt_obj_cpf = re.compile('^cn_rss_proc-\d{8}\.txt$')

  ## A: find last year dir, which we presume to be the current year
  ## 
  yr_data_dirs = []
  data_dirs = os.listdir(base_data_dir)
  for d in data_dirs:
    if fn_patt_obj_y4.match(d):
      yr_data_dirs.append(d)

  yr_data_dirs.sort()
  curr_yr_data_dir = yr_data_dirs[-1]

  curr_yr_data_dir_path = base_data_dir + os.sep + curr_yr_data_dir

  ##
  ## B: find last CN RSS processed file in current year directory,
  ##
  cn_rp_files = []
  files = os.listdir(curr_yr_data_dir_path)

  for f in files:
    if fn_patt_obj_cpf.match(f):
      cn_rp_files.append(f)

  cn_rp_files.sort()
  curr_cn_rp_file = cn_rp_files[-1]
  curr_cn_rp_path = curr_yr_data_dir_path + os.sep + curr_cn_rp_file

  return curr_cn_rp_path
  # end of getCurrentCNRssProcPath():


def parse_cn_rss_proc_file(path_arg):
  """
  Convert CN processed RSS data to list of dictionaries.  Each record
  is an RSS/Atom feed
  """
  item_lines =      []
  item_lines_list = []
  recs =            []
  rec =             {}

  dfile = open(path_arg)

  ##
  ## A. build item_lines_list - a list of list of strings
  ##
  line_num = 0
  in_item = False  # between 'start-item:' and 'end-item' tags
  for line in dfile.readlines():
    line_num += 1
    if line.startswith('start-item:'):
      in_item = True
      item_lines = []
    elif line.startswith('end-item:'):
      in_item = False
      item_lines_list.append(item_lines)
      item_lines = []
    elif in_item:
      item_lines.append(line)

  ##
  ## B. go thru item_lines_list and build the recs list
  ##
  num_items = len(item_lines_list)
  print 'Number of items: %d' % num_items
  for i in range(num_items):
    item_lines = item_lines_list[i]
    rec = convert_to_hash(item_lines)

    if False:
      print '@@@'
      print 'rec:'
      print rec
      print '@@@'
      print ''

    recs.append(rec)

  return recs
  # end of parse_cn_rss_proc_file(path_arg):


def convert_to_hash(sl):
  """
  convert list of strings to hash.  Strings expected to look like:
    a:  String one
    b:  String two
    c:  
        String three
        String four
  """
  h = {}
  a = ''   # attribute
  v = ''   # value
  patt_obj_1 = re.compile('^([\w-]+)\:')  # attribute
  patt_obj_2 = re.compile('^([\w-]+)\:\s*(\S.*)$')  # attribute + value
  #print '####'
  for l in sl:
    #print '>>>%s<<<' % l
    match_obj_1 = patt_obj_1.match(l)
    if match_obj_1:
      # discovered attribute (aka 'tag', or python dictionary key)
      #print 'MATCH'
      a = match_obj_1.group(1)
      #print '  a: \"%s\"' % a
      match_obj_2 = patt_obj_2.match(l)
      if match_obj_2:
        #print 'MATCH 2'
        v = match_obj_2.group(2)
        h[a] = v
        #print 'v: \"%s\"' % v
      else:
        v = ''
        h[a] = v
    else:
      #first_char = ''
      #if len(l) > 0:
      #  first_char = l[0]
      #print '$$%s$$' % l
      if len(a) > 0:
        h[a] += l
        #print '@@@'
        #print 'a: %s' % a
        #print 'a: %s' % a
        #print '@@@'
        #print ''
      
  #print '####'
  #print ''

  return h
  # end of convert_to_hash(sl):


def proc_html(data_list):

  ho = open(HTML_FILE_PATH, 'w')

  ##
  ## header info
  ##
  d_hdr = """\
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
    "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
  <head>
    <title>Compelling Narrative Raw RSS Data</title>
  </head>
  <body>
"""
  d_end = """\
  </table width="100%">
  </body>
</html>
"""
  ho.write(d_hdr)

  ##
  ## beginning of HTML Table info
  ## 
  t_start = """
<table border cellspacing=0 cellpadding=4>
  <caption align=top>CN Raw RSS Feed [Put Data Here...]</caption>
"""
  ho.write(t_start)

  print 'type(data_list): %s ' % type(data_list)
  for item in data_list:
    print 'type(item): %s ' % type(item)
    print '@@@'
    print 'item:'
    print item
    print '@@@'
    print ''

  ho.write(d_end)
  ho.close()

  return ''


if __name__ == '__main__':
  path = ''
  if len(sys.argv) < 2:
    path = DEF_DATA_DIR
  else:
    path = sys.argv[1]

  main(path)

  sys.exit(1)

