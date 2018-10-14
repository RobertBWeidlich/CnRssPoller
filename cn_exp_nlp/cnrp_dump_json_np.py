#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# file:    cnrp_dump_json_np.py
# author:  rbw
# date:    Fri Oct 12 18:09:04 PDT 2018
# purpose: NiFi processor to convert JSON textual data to textual data
#          to aid in cleaning out HTML artifacts from text.
########################################################################
import os
import sys
import json

def cnrp_dump_json_np(json_data):
    print "JSON DATA:"
    print ">>>"
    print "%s" % json_data
    print "<<<"

    # convert JSON to python object
    jo = json.loads(json_data)
    #print "%s" % str(jo)
    #print "type: %s" % (str(type(jo)))
    jo_keys = jo.keys()
    jo_keys.sort()
    #print jo_keys
    for jo_key in jo_keys:
        print "%s:" % jo_key
        print ">>>"
        print jo[jo_key]
        print "<<<"

if __name__ == '__main__':
    #
    # usage: ./cnrp_dump_json_np [file.json]
    #
    TEST_HC_FILE = True

    argc = len(sys.argv)
    #print "argc:     %d" % argc
    #print "sys.argv: %s" % str(sys.argv)

    in_buf = ""

    #
    # 1. if TEST_HC_FILES set to True, process hardcoded file
    #
    if TEST_HC_FILE:
        TEST_INPUT_FILE1 = "/tmp/nf_01_from_kafka_cnrt-nrt-feed/" + \
            "331338843061776"

        TEST_INPUT_FILE = TEST_INPUT_FILE1
        in_file = TEST_INPUT_FILE1

        with open(in_file) as f:
            for line in f.readlines():
                in_buf += line


    #
    # 2. if test file specified from command line, process that file
    #
    elif argc >= 2:
        in_file = sys.arg[1]
        with open(in_file) as f:
            for line in f.readlines():
                in_buf += line

    #
    # 3. if no test file specified, read from stdin.
    #    this is standard NiFi processor mode
    #
    else:
        in_buf = sys.stdin.read()

    cnrp_dump_json_np(in_buf)









    sys.exit(0)





