file: Install-2.0-on-AWS.md
date: Thu Jan  2 01:40:34 UTC 2020

This documents how to create a new AWS Linux EC2 (virtual machine) that should
be sufficient to run CnRssPoller, and how to install and run it.

1. Log into AWS Console
=======================

  -> http://console.aws.amazon.com
  -> EC2

2. Prerequisites
================

  2.1. Create a Security Group (SG)
  =================================
  -> http://console.aws.amazon.com
  -> EC2
  -> Security groups
  -> Create Security Group
  ... todo: finish this up.  for now use default SG
      when creating EC2

  2.2. Create a keypair (KP)
  ==========================
  -> http://console.aws.amazon.com
  -> EC
  -> Key pairs
  -> Create Key Pair
  Save Key Pair to local Linux Host
  Change permissions of keypair file
    $ chmod 400 <full-path-of-keypare-file>
  ... todo: document how to convert .pem keypair file for Putty

  2.3. Allocate an Elastic IP (EIP) to your account
  =================================================
    -> http://console.aws.amazon.com
    -> EC
    -> Elastic IPs
    -> Allocate Elastic IP address
        -> Scope = VPC
        -> Public IPv4 address pool = Amazons pool of IPv4 addresses
        -> Allocate
    - make note of the Public IPv4 address of the newly created EIP

3. Launch EC2 Instance
======================
  -> http://console.aws.amazon.com
  -> EC
  -> Launch Instance

  3.1. Choose AMI
  ===============
    -> Amazon Linux AMI 2018.03.0 (HVM), SSD Volume Type
       - ami-00eb20669e0990cb4
    -> 64-bit (x86)
    -> Select

  3.2. Choose Instance Type
  =========================
    -> t2.medium - 2 vCPUs, 4 GiB Memory
    -> Next: Configure Instance Details

  3.3. Choose Instance Type
  =========================
    - default settings should be OK
    -> Next: Add Storage

  3.4. Add Storage
  ================
    -> Size = 50 GiB
    -> Volume Type = Magnetic

  3.5. Next: Add Tags
  ===================
    - skip this...
    -> Next: Configure Security Group

  3.6. Configure Security Group (SG)
  ==================================
    - use default SG defalts, e.g. SSH port
    -> Review and Launch

  3.7 Review Instance Launch
  ==========================
    -> Launch
    -> Select a key pair...
      -> Select key pair created in step 2.2 above
      -> Click on "I acknowledge that I have access to the
                   selected private key..."
    -> Launch Instance
    -> View Instances, note the instance ID of the newly created instance

4. Associate Instance with an EIP
=================================
  -> http://console.aws.amazon.com
  -> EC
  -> Elastic IPs
  -> Select IPv4 address allocated in step 2.3 above
     (Click on numeric IPv4 address, NOT the box)
  -> "Associate Elastic IP address" button
  -> Resource Type = Instance
  -> Click on "Instance" box
  -> Select Instance ID of the instance created in step 3.7 above
  -> Associate
  ... ???

5. Log into Instance
====================
  In a Linux shell window:
    $ ssh -i ~/.aws/keypairs/kp.pem ec2-user@54.37.230.37

      (use full path of your keypair and the EIP allocated and associate
       in the steps above)

    $ sudo yum update
    $ sudo yum install git

6. Create account "cn" for CnRssPoller
======================================
  Log into the AWS EC2 instance using step 5 above

    $ sudo adduser cn
    $ sudo passwd cn
      (set password for the "cn" account)
    $ sudo usermod -aG wheel cn

  edit the /etc/sudoers file accordingly:

    $ sudo diff /etc/sudoers.orig /etc/sudoers
    98c98
    < # %wheel      ALL=(ALL)       ALL
    ---
    > %wheel        ALL=(ALL)       ALL
    $

  All subsequent steps below should be run as user "cn"

    $ sudo su - cn
    

7. Create SSH key for github.com
================================
  This is NOT necessary if you only need read-only access to the
  CnRssPoller repo on github.com

  If you need read/write access, follow these steps:
    https://github.com/settings/keys
    https://help.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh

8. Clone CnRssPoller git repo
=============================
  $ sudo su - cn
  $ mkdir ~/Projects
  $ cd ~/Projects
  $ git clone git@github.com:RobertBWeidlich/CnRssPoller.git
  $ git branch -r   # list all branches available at remote git repo
  $ git checkout 2.0-current-dev-20181007
  $ git pull

9. Set Environmental Variables
==============================
  Add the following to the ~cn/.bashrc file:

    $ export CN_HOME=/home/cn/Projects/CnRssPoller/cn_http_poller/py
    $ export CN_DATA=/data/cn
    $ export CN_PIPE=/tmp/p_cn_hpe_out
    $ export CN_TMP=/tmp
    $ export CN_WAIT_OFFSET=17.923
    $ export PYTHONPATH=/home/cn/Projects/CnRssPoller/cn_xml_doc/py:$PYTHONPATH

  Log out of the "cn" account, then log back in.

  Then run:

    $ sudo mkdir -p $CN_DATA
    $ sudo chmod a+w /data
    $ sudo chown -R cn:cn $CN_DATA

10. Start the CnRssPoller Processes
===================================
CnRssPoller consists of two separate Python processes:

  1. cn_hpe.py
  2. cn_rss_proc_json.py

The first process communicates to the second via a Unix pipe whose name is
defined by $CN_PIPE.

To start CnRss Poller, run the following in separate Linux windows:

  10.1. Start cn_hpe.py
  =====================
  In a Linux command shell run:
    $ cd $CN_HOME
    $ nohup ./cn_hpe.py ../config/cn_hpe.cfg > cn_hpe.out &
    $ tail -n 5000 -f ./cn_hpe.out

  10.2. Start cn_rss_proc_json.py
  ===============================
  In a Linux command shell run:
    $ cd $CN_HOME
    $ nohup ./cn_rss_proc_json.py > cn_rss_proc_json.out &
    $ tail -n 5000 -f ./cn_rss_proc_json.out

General Comments, to reduce AWS costs
=====================================
  - Make sure all EC2s turned off when not in use
  - Delete all unused (unassociated) EIPs

