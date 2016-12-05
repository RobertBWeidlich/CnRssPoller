#!/usr/bin/env python
##
## test regular expressions
##
import sys, re

test_str_01 = "tstamp:  20120924.0000.13"
test_str_02 = "tstamp:  20120924.0000.13 aasdf wer wer 23 "
test_str_03 = "tstamp:"
test_str = test_str_03

re_patt_str = "^(ts).*(\d{4})*"          # one group works
re_patt_str = "^(\w{1,20}\S\w{1,20}):.*$" # matches all of first group
re_patt_str = "^(\w{1,20}\-*\w{1,20}):.*$" # matches hyphen
re_patt_str = "^(\w{1,20}\-*\w{1,20}):(.*)$" # matches 2 groups
re_patt_str = "^(\w{1,20}\-*\w{1,20}):\s*(\S*.*)$" # matches 2 groups
re_patt_str = "^(\w+\-*\w+):\s*(\S*.*)$" # more compact version of above
re_patt_str = "^(\w+\-?\w+):\s*(\S*.*)$" # better - 0 or 1 hyphen

# todo: handle multiple hyphens

re_patt_obj = re.compile(re_patt_str)

match_obj = re_patt_obj.match(test_str)

if (not match_obj):
  print 'RE failed...'
  sys.exit(0)

print match_obj

#print 'number of groups: %d' % 

print 'group 1: \"%s\"' % match_obj.group(1)
print 'group 2: \"%s\"' % match_obj.group(2)




