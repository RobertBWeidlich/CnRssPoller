#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# file:    cn_rss_doc.py
# author:  rbw
# date:    101229.2120
# purpose: provide interface to RSS or Atom document
########################################################################
import sys
import xml.dom
import xml.dom.minidom
from cn_xml_doc import CnXmlDocument

class CnRssDocument(CnXmlDocument):
  def __init__(self, xml_file_arg, debug_arg=False):
    CnXmlDocument.__init__(self, xml_file_arg, debug_arg=False)
    self.itemList = [] # list of dictionaries

  def getRssOrAtom(self):
    """
    return 'rss' if document is RSS, 'atom' if Atom, and 'neither' if
    neither
    """
    nodes = self.getNodes()
    first_node = nodes[0]
    first_node_fqn = nodes[0]['fqname']
    nn = first_node_fqn.lower()
    if nn == 'rss':
      return 'rss'
    if nn == 'feed':
      return 'atom'
    else:
      return 'neither'

  def getItems(self):
    """
    return list of RSS items (or, in the case of Atom, ...
    """
    self.itemList = []
    if (len(self.itemList) < 1):
      self.__build_item_list()

    return self.itemList

  def __build_item_list(self):
    self.itemList = [] # list of dictionaries

    nodes = self.getNodes()
    data_type = self.getRssOrAtom()
    ##
    ## RSS data
    ##
    if data_type == 'rss':
      #print("NODES (RSS):")
      itemDict = {}
      itemDict['title'] =   ''
      itemDict['text'] =    ''
      itemDict['guid'] =    ''
      itemDict['pubdate'] = ''
      itemDict['url'] =     ''
      itemDict['author'] =  ''
      itemDict['summary'] = ''

      item_num = 0
      for node in nodes:
        #print('###')
        #print('node:')
        #print(node)
        #print('###')
        fqn = node['fqname']
        text = node['text']
        text = text.strip()
        #print('fqn: %s' % fqn)
        if (fqn == 'rss.channel.item'):
          #if len(itemDict) > 0:
          if item_num > 0:
            self.itemList.append(itemDict)
            itemDict = {}
            itemDict = {}
            itemDict['title'] =   ''
            itemDict['text'] =    ''
            itemDict['guid'] =    ''
            itemDict['pubdate'] = ''
            itemDict['url'] =     ''
            itemDict['author'] =  ''
            itemDict['summary'] = ''
          item_num += 1
        elif (fqn == 'rss.channel.item.title'):
          itemDict['title'] = text
        elif (fqn == 'rss.channel.item.description'):
          itemDict['text'] = text
        elif (fqn == 'rss.channel.item.guid'):
          itemDict['guid'] = text
        elif (fqn == 'rss.channel.item.link'):
          itemDict['url'] = text

    elif data_type == 'atom':
      itemDict = {}
      itemDict['title'] =   ''
      itemDict['text'] =    ''
      itemDict['guid'] =    ''
      itemDict['pubdate'] = ''
      itemDict['url'] =     ''
      itemDict['author'] =  ''
      itemDict['summary'] = ''

      item_num = 0
      for node in nodes:
        fqn = node['fqname']
        text = node['text']
        text = text.strip()
        #print('fqn: %s' % fqn)
        if (fqn == 'feed.entry'):
          #if len(itemDict) > 0:
          if item_num > 0:
            self.itemList.append(itemDict)
            itemDict = {}
            itemDict = {}
            itemDict['title'] =   ''
            itemDict['text'] =    ''
            itemDict['guid'] =    ''
            itemDict['pubdate'] = ''
            itemDict['url'] =     ''
            itemDict['author'] =  ''
            itemDict['summary'] = ''
          item_num += 1
        elif (fqn == 'feed.entry.title'):
          itemDict['title'] = text
        elif (fqn == 'feed.entry.content'):
          itemDict['text'] = text
        elif (fqn == 'feed.entry.id'):
          itemDict['guid'] = text
        elif (fqn == 'feed.entry.published'):
          itemDict['pubdate'] = text
        elif (fqn == 'feed.entry.link'):
          itemDict['url'] = text
        elif (fqn == 'feed.entry.author.name'):
          itemDict['author'] = text
        elif (fqn == 'feed.entry.summary'):
          itemDict['summary'] = text
      
