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
import re
import json


def proc_file_to_solr_json(in_path, out_path):
    #
    # regex to match fields such as "abc-def:" or "abcdef:"
    #
    ps1 = '^([a-zA-Z][a-zA-Z-]*)\:$'
    po1 = re.compile(ps1)

    #
    # regex to match fields such as "abc-def: data" or "abcdef: data"
    #
    ps2 = '^([a-zA-Z][a-zA-Z-]*)\:\s*(\S.*)$'
    po2 = re.compile(ps2)

    pl = []  # list to convert to JSON
    po = {}  # dictionaries to store in list pl
    inside_item = False
    cur_field = ""
    in_file = open(in_path, 'r')
    line_no = 0

    for line in in_file.readlines():
        # 1. trim newline char
        line = line.rstrip()

        # 2. skip comments
        if (len(line) > 0) and (line[0] == "#"):
            continue

        line_no += 1
        print "%d >>>%s<<<" % (line_no, line)
        if line_no > 30:
            break

        if line == "end-item:":
            if len(po) > 0:
                pl.append(po)
                po = {}
            inside_item = False
            continue
        elif line == "start-item:":
            if len(po) > 0:
                pl.append(po)
                po = {}
            inside_item = True
            continue

        if inside_item and len(line) > 0:
            # new field?
            pm1 = po1.match(line)
            if pm1:
                print "MATCH 1"
                pass
            else:
                pm2 = po2.match(line)
                if pm2:
                    print "MATCH 2"
                    pass


            # continuation line
            if line[0] == ' ':
                pass

    in_file.close()



    print "HERE - 1420"


if __name__ == '__main__':
    argc = len(sys.argv)
    if (argc < 3):
        print "usage: %s in-path out-path" % sys.argv[0]
        sys.exit(1)
    # print "len(sys.argv): %s" % str(argc)
    # print "current dir:   %s" % os.getcwd()
    in_file = sys.argv[1]
    out_file = sys.argv[2]
    proc_file_to_solr_json(in_file, out_file)

    sys.exit(0)

