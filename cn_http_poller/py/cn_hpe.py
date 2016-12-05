#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# file:    cn_hpe.py (HTTP Poll Engine)
# author:  rbw
# date:    Sat Mar  2 19:48:20 UTC 2013
# purpose: periodically poll list of HTTP sites for HTML, RSS, and Atom
#          data
# dependencies:
#          create pipe: 'mkfifo /tmp/p_cn_hpe_out' for cn_rss_proc.py
########################################################################
import os, sys, urllib, time
import threading
import socket
from cn_hpe_cfg import CnHpeCfg
from cn_hp_thr import CnHpThr
from cn_hp_utils import get_current_utc_hms

def main(cfg_file_arg, hostname):
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

  POSTPROC_OUT_PIPE = ENV_CN_PIPE

  print 'ENV_CN_HOME:        ' + ENV_CN_HOME
  print 'ENV_CN_DATA:        ' + ENV_CN_DATA
  print 'POSTPROC_OUT_PIPE:  ' + POSTPROC_OUT_PIPE
  print 'ENV_CN_TMP:         ' + ENV_CN_TMP
  print 'ENV_CN_WAIT_OFFSET: ' + ENV_CN_WAIT_OFFSET

  WAIT_OFFSET = float(ENV_CN_WAIT_OFFSET);

  cfg_file_dt = 0.0  # time config file last updated
  cfg_data = CnHpeCfg(cfg_file_arg)
  cfg_data.update()
  cfg_data.dump()

  #
  # open pipe to post-processing application
  # 
  print 'opening Unix pipe \"%s\"' % POSTPROC_OUT_PIPE
  p_file = open(POSTPROC_OUT_PIPE, 'w')
  p_file.write('#cn_hpe.py starting up\n')
  p_file.flush()
  time.sleep(1)
  p_file.close()
  time.sleep(1)
  p_file = open(POSTPROC_OUT_PIPE, 'w')
  p_file.write('#cn_hpe.py starting up\n')
  p_file.flush()
  print 'hostname: %s' % hostname

  # loop - iterate every 60 seconds
  logmutex = threading.Lock()
  threads = []
  loopi = 0
  while 1:
    ##
    ## wait until top of the minute + WAIT_OFFSET
    ##
    hms = get_current_utc_hms()

    sec = hms[2]
    t_str1 = hms[3]
    t_str2 = hms[4]

    wait_time = (60.0 - sec) + WAIT_OFFSET
    #print 'waiting for %f seconds' % wait_time

    time.sleep(wait_time)
    #print 'finished sleeping'
   
    #
    # now ready to poll
    # 
    hms = get_current_utc_hms()
    print ''
    #print '%s: finished waiting; ready to poll' % hms[4]
    print '%s: ready to poll' % hms[4]
    updated = cfg_data.update() # update if config file has been updated
    if updated:
      print 'config file updated...'
      cfg_data.dump()

    hms = get_current_utc_hms()
    poll_min = hms[1]
    print 'poll_min: %d' % poll_min

    sitename_list = cfg_data.get_namelist_by_min(poll_min)
    print 'polling sites:'
    for site in sitename_list:
      url = cfg_data.get_url_by_name(site)
      output_path_raw = set_output_path_raw(BASE_DIR_RAW, site)
      #
      # todo: we can probably get rid of the following line
      #
      output_path_proc = set_output_path_proc(BASE_DIR_PROC)
      #print '## %s %s' % (site, url)
      #print 'output path: \"%s\"' % output_path_raw
      #
      # run poller as thread
      #
      # site should be changed by a unique ID
      #
      thread = CnHpThr(site, url, output_path_raw, output_path_proc, \
                       p_file, logmutex)
      thread.start()
      #
      # don't append to threads list until we figure out how to manage it
      #
    print ''

    loopi += 1

def set_output_path_raw(base_dir_arg, tag_arg):
  """
  1. create raw RSS directory in the form:
 
    rss_dir = base_dir_arg + '/YYYY/MM/DD/HH'
 
  2. generate RSS file path name in the form:
 
    rss_path = rss_dir + '/' + "cn_rss_raw-" + tag_arg + YYYYMMDD.MMSS.SS.xml
 
     return rss_path
  """
  dir = ''
  path = ''
  if base_dir_arg.endswith(os.sep):
    dir_w_path = base_dir_arg
  else:
    dir_w_path = base_dir_arg + os.sep

  # generate current UTC timestamp
  #tnow = time.time()
  ##anow = time.asctime(time.localtime(tnow))
  #anow = time.asctime(time.gmtime(tnow))
  tnow = time.time()
  tn = time.gmtime(tnow)

  dir = dir_w_path + \
         '%04d' % tn.tm_year + os.sep + \
         '%02d' % tn.tm_mon +  os.sep + \
         '%02d' % tn.tm_mday + os.sep + \
         '%02d' % tn.tm_hour

  #
  # create data directory 
  #
  try:
    #print 'CREATING DIR \"' + dir + '\"'
    os.makedirs(dir)
  except OSError:
    # this happens when directory alread exists...
    #print 'FAILED TO CREATE DIR \"' + dir + '\"'
    pass
  else:
    pass

  file = 'cn_rss_raw-' + tag_arg + '-' \
         '%04d%02d%02d.%02d%02d.%02d.xml' \
         % (tn.tm_year, tn.tm_mon, tn.tm_mday, \
            tn.tm_hour, tn.tm_min, tn.tm_sec)
  #print 'dir:  %s' % dir
  #print 'file: %s' % file

  path = dir + os.sep + file

  print 'path: %s' % path

  return path

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
    print 'making: \"' + dir + '\"'
  except OSError:
    # this happens when directory already exists
    pass

  #rss_path_proc = rss_dir_proc + '/' + cn_rss_proc-YYYYMMDD.txt'
  file = 'cn_rss_proc-' + \
         '%04d%02d%02d' % (tn.tm_year, tn.tm_mon, tn.tm_mday) + \
         '.txt'

  path = dir + os.sep + file

  if False:
    print '##'
    print '## dir:  %s ' % dir
    print '## file: %s ' % file
    print '## path: %s ' % path
    print '##'

  return path


if __name__ == '__main__':
  if len(sys.argv) < 2:
    sys.stderr.write("usage: %s <config-file>\n" % sys.argv[0])
    sys.exit(1)

  hostname = socket.gethostname()
  print 'hostname: %s' % hostname

  cfg_file = sys.argv[1]
  main(cfg_file, hostname)


