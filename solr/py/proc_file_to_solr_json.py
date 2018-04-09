#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# file:    proc_file_to_solr_json.py
# author:  rbw
# date:    Sun Apr  8 07:46:20 PDT 2018
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
    # regex to match fields such as "abc-def7:" or "abcdef7:"
    #
    ps1 = '^([a-zA-Z][a-zA-Z0-9-]*)\:$'
    po1 = re.compile(ps1)

    #
    # regex to match fields such as "abc-def7: data" or "abcdef7: data"
    #
    ps2 = '^([a-zA-Z][a-zA-Z0-9-]*)\:\s*(\S.*)$'
    po2 = re.compile(ps2)

    pl = []  # list to convert to JSON
    po = {}  # dictionaries to store in list pl
    inside_item = False
    cur_field = ""
    in_file = open(in_path, 'r')
    line_no = 0

    for line in in_file.readlines():
        line_no += 1
        # 1. trim newline char
        line = line.rstrip()

        # 2. skip comments
        if (len(line) > 0) and (line[0] == "#"):
            continue

        print "%d >>>%s<<<" % (line_no, line)
        #if line_no > 60:
        #    break
        if line == "end-item:":
            if len(po) > 0:
                pl.append(po)
                po = {}
            inside_item = False
            cur_field = ""
            continue
        elif line == "start-item:":
            if len(po) > 0:
                pl.append(po)
                po = {}
            inside_item = True
            cur_field = ""
            continue

        if inside_item and len(line) > 0:
            # new field?
            pm1 = po1.match(line)
            if pm1:
                #print "group 1 0: \"%s\": " % pm1.group(0)
                #print "group 1 1: \"%s\": " % pm1.group(1)
                fld_name = pm1.group(1)
                cur_field = fld_name
                po[cur_field] = ""
                #print "MATCH 1"
            else:
                pm2 = po2.match(line)
                if pm2:
                    # print "group 2 0: \"%s\": " % pm2.group(0)
                    # print "group 2 1: \"%s\": " % pm2.group(1)
                    # print "group 2 2: \"%s\": " % pm2.group(2)
                    fld_name = pm2.group(1)
                    cur_field = fld_name
                    if cur_field == 'text1':
                        print "HERE..."
                    text = pm2.group(2).strip()
                    po[cur_field] = text
                    # print "MATCH 2"
                    continue

                #  continuation line
                if line[0] == ' ':
                    text = line
                    try:
                        po[cur_field] += text
                    except:
                        print "ERROR: cur_field %s not correct" % cur_field

    in_file.close()


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

