#!/usr/bin/env python
##
## test ftp
##
import sys, re
import ftplib

f = ftplib.FTP('polyticker.com')
# insert username and password
f.login('**********', '***********')

f.cwd('polyticker.com/data/cn/rss_current')
#f.retrlines('LIST')

fp = open('/home/ec2-user/data2/cn/rss_current/20121002.0034.13.txt')
d = f.storlines('STOR 20121002.0034.13.txt', fp)
fp.close();
f.close();


