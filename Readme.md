file:    cn_http_poller/py/Readme.py
author:  rbw
date:    Wed Mar 20 21:18:17 EDT 2013
purpose: How to bootstrap CN RSS polling and processing tools

To run CN RSS Poller:

  1. Create a "cn" user on the Linux machine running this.

  2. Set these environmental variable in ~cn/.bashrc:

      [todo: define what each is]

      export CN_HOME=/home/cn/Projects2013/cn_http_poller/py
      export CN_DATA=/data1/cn
      export CN_PIPE=/tmp/p_cn_hpe_out
      export CN_TMP=/tmp
      export CN_WAIT_OFFSET=13.283
      export PYTHONPATH=/home/cn/Projects2013/cn_xml_doc/py:$PYTHONPATH

      Note: do NOT use "~" to denote home directory in Python code, but it
            seems to be OK in .bashrc.

  3. make sure $CN_DATA directory exists and is writeable by the cn user

  4. Make sure cn_xml_doc is installed:

    "cd ~/Desktop/Projects2011"

    "git clone ssh://compellingnarrative@compellingnarrative.com/" +
    "~/git_repos/cn_xml_doc.git"
      [append the above 2 lines as a single command line -
       no space between the two lines.]

    Append the following line in ~/.bashrc:
      "export PYTHONPATH=~/Desktop/Projects2011/cn_xml_doc/py:$PYTHONPATH"

  5A. In one window run:

       cd $CN_HOME
       ./cn_hpe.py ../config/cn_hpe.cfg &

  5B. In a second window run:

       cd $CN_HOME
       ./cn_rss_proc.py &

  5B. In a third window run:

       ##########################################################
       NOTE: you must set up credentials for FTP destination host
       before running this
       ##########################################################

       cd $CN_HOME
       ./cn_ftp_proc.py &

Additional projects:

  cn_dump_nyt.py:
    Dump all nytimes data to a single file.

  cn_proc_rss_to_html.py:
    Convert latest data to HTML

