#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# file:    proc_file_to_solr_json.py
# author:  rbw
# date:    Mon Apr  2 04:53:14 PDT 2018
# purpose: Convert data in CN RSS proc format to Solr JSON format
#   CN RSS proc format:
#     /data1/cn/rss_proc/2018
#   Solr JSON input format:
#     /usr/local/solr-7.2.1/example/exampledocs/books.json
########################################################################
import os, sys

def proc_file_to_solr_json(in_path, out_path):
    pass


if __name__ == '__main__':
    argc = len(sys.argv)
    if (argc < 3):
        print "usage: %s in-path out-path" % sys.argv[0]
        sys.exit(1)
    # print "len(sys.argv): %s" % str(argc)
    # print "current dir:   %s" % os.getcwd()
    in_file = sys.argv[1]
    out_file = sys.argv[2]
    proc_file_to_solr_json(in_file, out_file):

    sys.exit(0)

