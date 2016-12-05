#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# file:    cn_hpe_cfg.py
# author:  rbw
# date:    110130.2030
# purpose: maintain information from CN HTTP Poller Exec (cn_hpe.py)
#          configuration file
########################################################################
import sys, time, os

#class cn_hpe_cfg():
class CnHpeCfg():

  def __init__(self, cfg_file_arg):
    self.cfg_file = cfg_file_arg

    #
    # name to URL dictionary - 
    # map 'news.cnn.topstories' to
    #     'http://rss.cnn.com/rss/cnn_topstories.rss'
    #
    self.n2u_dict = {}

    #
    # time to poll list -
    # list of times (0 to 59) - each element contains a list of names of
    # sites to poll.  At 13 past the hour, the 14th element...
    # 
    self.ttpl_list = []

    self.last_update_time = 0.0

    self.update()

  #
  # if file has been updated since the last read, then update information
  #
  def update(self):
    #
    # compare self.last_update_time to file's time of last modification
    #
    last_mod_time = os.stat(self.cfg_file).st_mtime
    #print 'self.last_update_time: %f' % self.last_update_time
    #print 'last_mod_time:         %f' % last_mod_time
    #if (last_mod_time > self.last_update_time):
    if (last_mod_time < self.last_update_time):
      return False
    #print 'FILE MODIFED'

    self.update_uncond()
    return True

  #
  # update whether or not config file has been updated
  #
  def update_uncond(self):
    #
    # load data from file
    #
    self.n2u_dict = {}
    self.ttpl_list = []
    for i in range(0, 60):
      self.ttpl_list.append([])

    cfile = open(self.cfg_file, 'r')
    line_num = 0
    for line in cfile.readlines():
      line_num += 1
      #print '1>>%s<<' % line
      #
      # 1. trim leading and trailing spaces in line
      #
      line = line.strip()

      #print '2>>%s<<' % line
      #print ''

      #
      # 2. ignore blank lines
      #
      if len(line) < 1:
        #print 'BLANK'
        continue

      #
      # 3. ignore comment lines (first non-space character is '#'
      #
      if line[0] == '#':
        #print 'COMMENT'
        continue

      #
      # now expect 3 tokens:
      #   1. comma-separated list of minutes
      #   2. name of site
      #   3. URL of site
      #
      toks = line.split()
      if len(toks) < 3:
        sys.stderr.write(\
          'WARNING: config file \"%s\" line %d: expecting 3 tokens%s' \
          % (self.cfg_file, line_num, os.linesep))
        continue

      cfg_mins_str = toks[0].split(',')
      #
      # config minute strings to int
      #
      cfg_mins = []
      for min in cfg_mins_str:
        cfg_mins.append(int(min))
        
      cfg_site_name = toks[1]
      cfg_site_url = toks[2]

      #
      # add to URL dictionary
      # todo: make sure this entry is not already in the dictionary
      #
      self.n2u_dict[cfg_site_name] = cfg_site_url

      #
      # add name to entries for appropriate minutes in self.ttpl_list
      #
      #print 'cfg_mins: %s' % cfg_mins
      for i in range(0, 60):
        if i in cfg_mins:
          #print 'i: %d' % i
          self.ttpl_list[i].append(cfg_site_name)
          #print 'X%d' % i
        #else:
        #  print ' %d' % i

    tnow = time.time();
    self.last_update_time = tnow

  #
  # show contents of configuration to stdout
  #
  def dump(self):
    print ''
    print 'dumping configuration:'
    print ' Name to URL dictionary:'
    keys = self.n2u_dict.keys()
    keys.sort()

    #
    # first size the columns
    # 
    max1 = 0
    max2 = 0
    for key in keys:
      #print '  %s %s' % (key, self.n2u_dict[key])
      k = key
      kl = len(k)
      v = self.n2u_dict[k]
      vl = len(v)
      if kl > max1: max1 = kl
      if vl > max2: max2 = vl
      #print 'max1: %d' % max1
      #print 'max2: %d' % max2
    print ''
    #print 'kl: %d' % kl
    #print 'vl: %d' % vl

    #
    # print header
    #
    sep = ' ' * (max1-(len('Name')+1))
    print '  Name %s URL' % sep
    #print '  %s %s' % (('=' * kl), ('=' * vl))
    print '  %s %s' % (('=' * max1), ('=' * max2))

    #
    # print values
    #
    for key in keys:
      sep1 = ' ' * (max1-(len(key)))
      #print 'sep1: >>%s<<' % sep1
      #print 'len(sep1): >>%d<<' % len(sep1)
      print '  %s %s%s' % (key, sep1, self.n2u_dict[key])

    print ''
    print ' Poll List (which sites to poll each minute):'
    print '  Min Name'
    print '  %s %s' % (('=' * 3), ('=' * 67))
    for i in range(0, 60):
      plist = self.ttpl_list[i]
      plist.sort()
      if len(plist) < 1:
        print '   %02d %s' % (i, '-')

      for p in plist:
        print '   %02d %s' % (i, p)

  #
  # get list of names of sites to poll.  min_arg must be 0 - 59, and
  # correspond to current minute.
  #
  def get_namelist_by_min(self, min_arg):
    return self.ttpl_list[min_arg]

  #
  # map sitename (specified by name_arg) to URL of site
  #
  def get_url_by_name(self, name_arg):
    return self.n2u_dict[name_arg]

