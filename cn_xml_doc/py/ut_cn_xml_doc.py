#!/usr/bin/env python3
# -*- coding: utf-8 -*-
########################################################################
# file:    ut_cn_xml_doc.py
# author:  rbw
# date:    Sat Jan 13 16:17:40 PST 2018
# purpose: Unit test for cn_xml_doc.py
#
# todo:    Test with a non-RSS XML file
########################################################################
import os
import sys
from cn_xml_doc import CnXmlDocument


def main():
    cd = os.getcwd()
    print("current directory: " + cd)

    data_dir = "../../resources/data/"
    path_01 = data_dir + "cn_rss_raw-news.latimes-20180113.2304.13.xml"
    path_02 = data_dir + "cn_rss_raw-news.sweden.thelocal-20180113.2304.13.xml"
    path_03 = data_dir + "cn_rss_raw-news.upi-20180113.2305.13.xml"
    path_04 = data_dir + "cn_rss_raw-news.washpost.world-20180113.2307.13.xml"

    path = path_01

    print('testing on file \"%s\"' % path)

    gxp = CnXmlDocument(xml_file_arg=path, debug_arg=False)
    print('###Items###')
    nodes = gxp.getNodes()
    for node in nodes:
        print('########')
        print('node:')
        print(node)
        print('########')

    sys.exit(0)


if __name__ == '__main__':
    main()
