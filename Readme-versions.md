#file:    Readme-versions.py
author:  rbw
date:    Sat Mar 31 14:26:40 PDT 2018

Version 1.0:

  - Polls RSS sites
  - Saves all RSS data to files
  - Dedups data
  - Saves deduped data to files

Version 2.0:

  - Polls RSS sites
  - Saves all RSS data to files
  - Dedups data
  - Saves deduped data to files in a Solr-compatible JSON format
  - Sends deduped data to Kafka for a NRT (Near RealTime) data feed

Version 2.1:

  - Experiments to build processors to pull data from Kafka, process
    that data, then push results back to Kafka

