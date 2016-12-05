#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# file:    cn_ftp_proc.py
# author:  rbw
# date:    Sun Apr 14 14:05:55 EDT 2013
# purpose: send updates of the post-processed data files to a remote
#          ftp client
#
# todo:    it would be cleaner to encapsulate logic to get new
#          items in a class.
#
#          test hostname to determine BASE_DIR_PROC
#          (see how it's done in cn_hpe.py)
########################################################################
import os, sys, time, ftplib
from cn_hp_utils import get_current_utc_hms, get_last_n_proc_data_items

def main():
  #
  # get environmental variables, and verify they refer to existing
  # objects
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

  #
  # create data directories, if necessary
  #
  # BASE_DIR_RAW =     ENV_CN_DATA + '/rss_raw'
  # BASE_DIR_PROC =    ENV_CN_DATA + '/rss_proc'
  # BASE_DIR_CURRENT = ENV_CN_DATA + '/rss_current'
  #
  BASE_DIR_RAW = ENV_CN_DATA
  if not BASE_DIR_RAW.endswith(os.sep):
    BASE_DIR_RAW += os.sep
  BASE_DIR_RAW += 'rss_raw'
  print 'BASE_DIR_RAW:       ' + BASE_DIR_RAW
  if not os.path.exists(BASE_DIR_RAW):
    print 'creating \"' + BASE_DIR_RAW + '\"'
    os.mkdir(BASE_DIR_RAW)

  BASE_DIR_PROC = ENV_CN_DATA
  if not BASE_DIR_PROC.endswith(os.sep):
    BASE_DIR_PROC += os.sep
  BASE_DIR_PROC += 'rss_proc'
  print 'BASE_DIR_PROC:      ' + BASE_DIR_PROC
  if not os.path.exists(BASE_DIR_PROC):
    print 'creating \"' + BASE_DIR_PROC + '\"'
    os.mkdir(BASE_DIR_PROC)

  BASE_DIR_CURRENT = ENV_CN_DATA
  if not BASE_DIR_CURRENT.endswith(os.sep):
    BASE_DIR_CURRENT += os.sep
  BASE_DIR_CURRENT += 'rss_current'
  print 'BASE_DIR_CURRENT:   ' + BASE_DIR_CURRENT
  if not os.path.exists(BASE_DIR_CURRENT):
    print 'creating \"' + BASE_DIR_CURRENT + '\"'
    os.mkdir(BASE_DIR_CURRENT)

  #
  # for now, ignore ENV_CN_WAIT_OFFSET
  #
  WAIT_OFFSET =    55.572 # give cn_hpe.py time to finish
  NUM_DATA_ITEMS = 500

  ##
  ## loop - iterate every 60 seconds
  ##
  loopi = 0
  last_item_ts_this_time = '';
  last_item_ts_last_time = '';

  while 1:
    loopi += 1
    data = get_last_n_proc_data_items(BASE_DIR_PROC, NUM_DATA_ITEMS)
    last_item = data[-1:][0]
    last_item_ts = last_item['tstamp']
    last_item_ts_last_time = last_item_ts_this_time
    last_item_ts_this_time = last_item_ts

    #
    # create new data
    #
    new_flag = False;
    data_new = []
    #print 'last time: %s' % last_item_ts_last_time
    #print 'this time: %s' % last_item_ts_this_time
    if len(last_item_ts_last_time) > 0:
      for d in data:
        if new_flag == False:
          #print '  %s > %s??' % (d['tstamp'], last_item_ts_last_time)
          if d['tstamp'] > last_item_ts_last_time:
            new_flag = True
          else:
            continue;
        data_new.append(d)

    #
    # dump items
    #
    #for d in data:
    for d in data_new:
      #print d
      print ''
      print 'src:      %s' % d['src']
      print 'url:      %s' % d['url']
      print 'tstamp:   %s' % d['tstamp']
      print 'path:     %s' % d['path']
      print 'pubdate:  %s' % d['pubdate']
      print 'author:   %s' % d['author']
      print 'summary:  %s' % d['summary']
      print 'guid:     %s' % d['guid']
      print 'title:    %s' % d['title']
      print 'text1:    %s' % d['text1']
      print ''
      print ''
    print 'last_item_ts: %s' % last_item_ts
    print ''

    print 'size of data:     %d' % len(data)
    print 'size of new data: %d' % len(data_new)

    if (len(data_new)):
      path = write_to_data_file(BASE_DIR_CURRENT, data_new, last_item_ts)
      ftp_transfer(path)

    ##
    ## wait until the top of the minute + WAIT_OFFSET
    ##
    hms = get_current_utc_hms()
    #print hms
    poll_min = hms[1]
    print 'poll_min: %s' % poll_min

    sec = hms[2]
    wait_time = (60.0 - sec) + WAIT_OFFSET
    # todo: clean up the next 3 lines
    wait_time %= 60.0 
    if wait_time < 30.0:
      wait_time += 60.0
    wait_time += 120.0
    print 'waiting for %f seconds' % wait_time
    print ''

    time.sleep(wait_time)

#
# write list to file
#
# return full path of new data file
#
def write_to_data_file(base_dir, data_list, tstamp):
  NL = os.linesep

  base_dir_slash = base_dir
  if (not base_dir_slash.endswith(os.path.sep)):
    base_dir_slash += os.path.sep

  path = base_dir_slash + tstamp + '.txt'
  print '    path:          %s' % path

  print 'opening \"%s\" for writing' % path
  of = open(path, 'w')
  for data in data_list:
    of.write("start-item:" + NL)
    if data.has_key('path'):
      of.write('path:    %s\n' % data['path'])
    if data.has_key('src'):
      of.write('src:     %s\n' % data['src'])
    if data.has_key('tstamp'):
      of.write('tstamp:  %s\n' % data['tstamp'])
    if data.has_key('pubdate'):
      of.write('pubdate: %s\n' % data['pubdate'])
    if data.has_key('author'):
      of.write('author:  %s\n' % data['author'])
    if data.has_key('guid'):
      of.write('guid:    %s\n' % data['guid'])
    if data.has_key('url'):
      of.write('url:     %s\n' % data['url'])
    if data.has_key('title'):
      of.write('title:   %s\n' % data['title'])
    if data.has_key('summary'):
      of.write('summary: %s\n' % data['summary'])
    if data.has_key('text1'):
      of.write('text1:   %s\n' % data['text1'])

    of.write("end-item:" + NL)
    of.write(NL)

  of.close()

  return path

#
# todo: hard-coded variables should be specified in a config file
#
def ftp_transfer(pathname):
  print '  ftp_transfer(\"%s\") ' % pathname

  ##
  ## Before using this, add credentials for the host to which you
  ## want to FTP data
  ##

  R_HOSTNAME = 'acme.com'
  R_DIR =      'acme.com/data/cn/rss_current'
  R_U =        'edit_this'
  R_P =        'edit_this'

  #
  # convert pathname to dir and file
  #
  l_dir = ''
  l_file = ''

  lsi = pathname.rindex('/')
  l_dir = pathname[:lsi]
  l_file = pathname[lsi+1:]

  try:
    f = ftplib.FTP(host = R_HOSTNAME, timeout=30)
    f.login(R_U, R_P)

    f.cwd(R_DIR)
    #f.retrlines('LIST')

    fp = open(pathname)
    print 'transferring %s to %s' % (pathname, R_DIR)
    d = f.storlines('STOR %s' % l_file, fp)
    fp.close
    f.close();
  except:
    print '#WARNING: failed to ftp to %s' % R_HOSTNAME


if __name__ == '__main__':
  main()

