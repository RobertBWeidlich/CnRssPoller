#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# file:    cn_rss_proc.py  (RSS post-processor)
# author:  rbw
# date:    Sat Mar  2 19:48:20 UTC 2013
# purpose: Post-processor for RSS files - dedup, convert to plain text
#          and feed to text mining apps.
# dependencies:
#          Unix pipe '/tmp/p_cn_hpe_out'
########################################################################
import os, sys, time, re, anydbm
from cn_rss_doc import CnRssDocument
import socket

def main(hostname):
  #
  # get environmental variables, and verify they refer to existing
  # objects
  #
  # (todo: put this in a separate file)
  #
  if not os.environ.has_key('CN_HOME'):
    print 'ERROR: environmental variable \'CN_HOME\' not defined'
    sys.exit(1)
  ENV_CN_HOME = os.environ['CN_HOME']
  if not os.path.exists(ENV_CN_HOME):
    print 'ERROR: directory \"' + ENV_CN_HOME + '\" ' + \
          'defined by environmental ' + \
          'variable \'CN_HOME\'' + ' does not exist'
    sys.exit(1)

  if not os.environ.has_key('CN_DATA'):
    print 'ERROR: environmental variable \'CN_DATA\' not defined'
    sys.exit(1)
  ENV_CN_DATA = os.environ['CN_DATA']
  if not os.path.exists(ENV_CN_DATA):
    print 'ERROR: directory \"' + ENV_CN_DATA + '\" ' + \
          ' defined by environmental ' + \
          'variable \'CN_DATA\'' + ' does not exist'
    sys.exit(1)

  if not os.environ.has_key('CN_PIPE'):
    print 'ERROR: environmental variable \'CN_PIPE\' not defined'
    sys.exit(1)
  ENV_CN_PIPE = os.environ['CN_PIPE']
  if not os.path.exists(ENV_CN_PIPE):
    os.mkfifo(ENV_CN_PIPE)
    print 'creating pipe file \"' + ENV_CN_PIPE + '\"'
    #print 'ERROR: pipe file \"' + ENV_CN_PIPE + '\ " ' + \
    #      'defined by environmental ' + \
    #      'variable \'CN_PIPE\'' + ' does not exist'
    #sys.exit(1)

  if not os.environ.has_key('CN_TMP'):
    print 'ERROR: environmental variable \'CN_TMP\' not defined'
    sys.exit(1)
  ENV_CN_TMP = os.environ['CN_TMP']
  if not os.path.exists(ENV_CN_TMP):
    print 'ERROR: tmp file \"' + ENV_CN_TMP + '\" ' + \
          ' defined by environmental ' + \
          'variable \'CN_TMP\'' + ' does not exist'
    sys.exit(1)

  if not os.environ.has_key('CN_WAIT_OFFSET'):
    print 'ERROR: environmental variable \'CN_WAIT_OFFSET\' not defined'
    sys.exit(1)
  ENV_CN_WAIT_OFFSET  = os.environ['CN_WAIT_OFFSET']

  print 'ENV_CN_HOME:        ' + ENV_CN_HOME
  print 'ENV_CN_DATA:        ' + ENV_CN_DATA
  print 'ENV_CN_PIPE:        ' + ENV_CN_PIPE
  print 'ENV_CN_TMP:         ' + ENV_CN_TMP
  print 'ENV_CN_WAIT_OFFSET: ' + ENV_CN_WAIT_OFFSET

  BASE_DIR_PROC = ENV_CN_DATA
  if not BASE_DIR_PROC.endswith(os.sep):
    BASE_DIR_PROC += os.sep
  BASE_DIR_PROC += 'rss_proc'
  
  POSTPROC_OUT_PIPE = ENV_CN_PIPE
  WAIT_OFFSET = float(ENV_CN_WAIT_OFFSET);

  f = open(POSTPROC_OUT_PIPE, 'r')

  o_path = set_output_path_proc(BASE_DIR_PROC)
  print('# opening \'%s\'' % o_path);
  ofp = open(o_path, 'a')
  ofp.write('#starting cn_rss_proc.py\n')
  ofp.flush()
  ofp_name = o_path

  while True:
    line = f.readline()
    if len(line) < 1:  # producer has disconnected
      print('waiting for producer to connect...')
      time.sleep(1)
      continue
    line = line.strip()

    #
    # create output file - but only for new-day rollover
    #
    o_path = set_output_path_proc(BASE_DIR_PROC)
    if (o_path != ofp_name):
      ofp.flush()
      ofp.close()
      print('## opening \'%s\'' % o_path);
      ofp = open(o_path, 'a')
      ofp_name = o_path

    proc_rss_file(line, ofp, ENV_CN_TMP)
    ofp.flush()

def proc_rss_file(path_arg, ofp_arg, tmp_dir):
  of = ofp_arg
  fn_patt_str  = '.*cn_rss_raw-(.*)-(\d{8}\.\d{4}\.\d{2})\.xml$'
  fn_patt_obj = re.compile(fn_patt_str)
  fn_match_obj = fn_patt_obj.match(path_arg)
  if fn_match_obj == None:
    # todo: flag as error
    return
  src = fn_match_obj.group(1)
  tstamp = fn_match_obj.group(2)
  #print('#path:   %s' % path_arg)
  #print('#src:    %s' % src)
  #print('#tstamp: %s' % tstamp)
  #print('')

  try:
    gxp = CnRssDocument(path_arg, False)
    doc_type = gxp.getRssOrAtom()
  except:
    #print('#WARNING: CnRssDocument(\"%s\", False) failed' % path_arg)
    #print('end-item:')
    #print('')
    of.write('#WARNING: CnRssDocument(\"%s\", False) failed\n' % path_arg)
    of.write('end-item:\n')
    of.write('\n')
    return
  print('#processing %s (%s)' % (path_arg, doc_type))
  of.write('#processing %s (%s)\n' % (path_arg, doc_type))
  items = gxp.getItems()
  for item in items:
    uid = item['guid']
    if len(uid) < 1:
      uid = item['url']
    #if False:
    if len(uid) < 1:
      # todo: look for better alternatives for guid?? - rbw, 20121009.1943
      if len(uid) < 1:
        uid = item['url']
        print ''
        print '  item[guid]: \"%s\"' % item['guid']
        print '    type: ', type(item['guid'])
        print '    len:  ', len(item['guid'])
        print '  item[title]: \"%s\"' % item['title']
        print '  item[text]: \"%s\"' % item['text']
        print '  item[pubdate]: \"%s\"' % item['pubdate']
        print '  item[url]: \"%s\"' % item['url']
        print '  item[author]: \"%s\"' % item['author']
        print '  item[summary]: \"%s\"' % item['summary']
        print ''

    #if isUniqueGuid(item['guid'], src, tstamp, tmp_dir):
    if isUniqueGuid(uid, src, tstamp, tmp_dir):
      #print('item:')
      #print(item)
      #db_key = db_key.encode('latin-1', 'replace')
      pubdate_cl = item['pubdate'].encode('latin-1', 'replace')
      author_cl = item['author'].encode('latin-1', 'replace')
      guid_cl = item['guid'].encode('latin-1', 'replace')
      url_cl = item['url'].encode('latin-1', 'replace')
      of.write('start-item:\n')
      of.write('path:    %s\n' % path_arg)
      of.write('src:     %s\n' % src)
      of.write('tstamp:  %s\n' % tstamp)
      #of.write('pubdate: %s\n' % item['pubdate'])
      #of.write('author:  %s\n' % item['author'])
      #of.write('guid:    %s\n' % item['guid'])
      #of.write('url:     %s\n' % item['url'])
      of.write('pubdate: %s\n' % pubdate_cl)
      of.write('author:  %s\n' % author_cl)
      of.write('guid:    %s\n' % guid_cl)
      of.write('url:     %s\n' % url_cl)

      text_title_clean = clean_text(item['title'])
      try:
        #print('title:   %s' % text_title_clean)
        of.write('title:   %s\n' % text_title_clean)
      except:
        try:
          #print('title:   %s' % text_title_clean.encode('latin-1', 'replace'))
          of.write('title:   %s\n' % text_title_clean.encode('latin-1', 'replace'))
        except:
          of.write('#ERROR: can\'t print title...\n')
          hstr = hexdump(text_title_clean)
          of.write('%s\n' % hstr)

      #print('summary: %s' % item['summary'])
      sum_cl = item['summary'].encode('latin-1', 'replace')
      of.write('summary: %s\n' % sum_cl)

      text1 = clean_text(item['text'])
      try:
        of.write('text1:   %s\n' % text1)
      except:
        try:
          of.write('text1:  %s\n' % text1.encode('latin-1', 'replace'))
        except:
          of.write('#ERROR: can\'t print text1...\n')
          hstr = hexdump(text1)
          print('%s\n' % hstr)

      #of.write('...\n')
      of.write('end-item:\n')
      of.write('\n')
    # end of if isUniqueGuid()


  return

def isUniqueGuid(guid_arg, source_arg, tstamp_arg, tmp_dir):
  """
  Use anydbm to store guids.  Operate on today and yesterday -- anydbm
  does not support deletion of old guids.

  dbm file name will be in the form "/tmp/cn_rss_guids-YYMMDD"
  """
  #print(' %s %-24s %s' % (tstamp_arg, source_arg, guid_arg))

  t_today = int(time.time())
  t_yesterday = t_today - 86400

  t_today_parts =     time.gmtime(t_today)
  t_yesterday_parts = time.gmtime(t_yesterday)

  timestamp = '%04d%02d%02d.%02d%02d.%02d' %       \
                           (t_today_parts.tm_year, \
                            t_today_parts.tm_mon,  \
                            t_today_parts.tm_mday, \
                            t_today_parts.tm_hour, \
                            t_today_parts.tm_min,  \
                            t_today_parts.tm_sec)

  dbm_fname_today =     '%04d%02d%02d.db' %               \
                           (t_today_parts.tm_year,     \
                           t_today_parts.tm_mon,       \
                           t_today_parts.tm_mday)
  dbm_fname_yesterday = '%04d%02d%02d.db' %               \
                          (t_yesterday_parts.tm_year,  \
                           t_yesterday_parts.tm_mon,   \
                           t_yesterday_parts.tm_mday)

  #dbm_pname_today =     '%s%s%s%s' % \
  #                        ('/tmp', os.sep, 'cn_hp_thr-', dbm_fname_today)
  #dbm_pname_yesterday = '%s%s%s%s' % \
  #                        ('/tmp', os.sep, 'cn_hp_thr-', dbm_fname_yesterday)
  dbm_pname_today =     '%s%s%s%s' % \
                          (tmp_dir, os.sep, 'cn_hp_thr-', dbm_fname_today)
  dbm_pname_yesterday = '%s%s%s%s' % \
                          (tmp_dir, os.sep, 'cn_hp_thr-', dbm_fname_yesterday)
  is_unique = True
  #
  # key/value pair to be stored in dbm file:
  #
  #  db_key = <source_arg>:<guid_arg>
  #  db_val = <timestamp>
  #
  db_key = source_arg + ':' + guid_arg
  db_key = db_key.encode('latin-1', 'replace')
  db_val = timestamp

  #
  # first check today's dbm file
  #
  db_today = anydbm.open(dbm_pname_today, 'c')
  try:
    # ERROR - 110216.0750 - for unicode characters
    #guid_arg_str = str(guid_arg) # error here
    if db_today.has_key(db_key):
      is_unique = False
    else:
      db_today[db_key] = timestamp # register this key
      db_yesterday = anydbm.open(dbm_pname_yesterday, 'c')
      if db_yesterday.has_key(db_key):
        # confirm this feature works...
        print('# found in yesterday, not today: \"%s\"' % db_key)
        is_unique = False
      db_yesterday.close()
    db_today.close()
  except:
    # todo: try a little harder...
    return False

  #print('## is_unique: %s' % is_unique)
  return is_unique

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

def set_output_path_proc(base_dir_arg):
  """
  1. create a processed RSS directory in the form:

       rss_dir_proc = base_dir_arg + '/' + YYYY

  2. generate processes RSS file path name in the form:

       rss_path_proc = rss_dir_proc + '/' + cn_rss_proc-YYYYMMDD.txt'

     return rss_path_proc
  """
  dir = ''
  path = ''
  if base_dir_arg.endswith(os.sep):
    dir_w_path = base_dir_arg
  else:
    dir_w_path = base_dir_arg + os.sep

  #
  # generate current UTC timestamp
  #
  tnow = time.time()
  tn = time.gmtime(tnow)

  dir = dir_w_path + '%04d' % tn.tm_year

  #
  # create data directory
  #
  try:
    os.makedirs(dir)
  except OSError:
    # this happens when directory already exists
    pass

  #rss_path_proc = rss_dir_proc + '/' + cn_rss_proc-YYYYMMDD.txt'
  file = 'cn_rss_proc-' + \
         '%04d%02d%02d' % (tn.tm_year, tn.tm_mon, tn.tm_mday) + \
         '.txt'

  path = dir + os.sep + file

  #print '##'
  #print '## dir:  %s ' % dir
  #print '## file: %s ' % file
  #print '## path: %s ' % path
  #print '##'

  return path

if __name__ == '__main__':
  if len(sys.argv) < 2:
    #sys.stderr.write("usage: %s <config-file>\n" % sys.argv[0])
    #sys.exit(1)
    pass

  #cfg_file = sys.argv[1]
  #main(cfg_file)
  hostname = socket.gethostname()
  main(hostname)


