file: Install-2.0-on-AWS.md

This documents how to create a new AWS Linux AMI (virtual machine) that should
be sufficient to run CnRssPoller.

1. Log into AWS

  -> http://console.aws.amazon.com
  -> EC

2. Create a keypair
  -> http://console.aws.amazon.com
  -> EC
  -> Key pairs
  -> Create Key Pair
  Save Key Pair to local Linux Host

3. Create a Elastic IP
  -> http://console.aws.amazon.com
  -> EC
  -> Elastic IPs

4. Launch EC2 Instance
  -> http://console.aws.amazon.com
  -> EC
  -> Launch Instance

  A. Select AMI
    -> Amazon Linux AMI 2018.03.0 (HVM), SSD Volume Type
       - ami-00eb20669e0990cb4
    -> 64-bit (x86)
    -> Select

  B. Choose an Instance Type
    -> t2.medium - 2 vCPUs, 4 GiB Memory
    -> Next: Configure Instance Details





