#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# file:    cn_xml_doc.py
# author:  rbw
# date:    101216.2100
# purpose: Parse XML document
########################################################################
import sys
import xml.dom
import xml.dom.minidom

class CnXmlDocument():
  """
  Load data from XML file

  Data is represented as a list of nodes; each node is a node in the XML
  document

  Each node contains three components:

    1. fully-qualified name (element?  tag?) expressed as a Python
       '.' separated string.

    2. attribute/value pairs, represented as a Python dictionary

    3. text, represented as a Python string
  
  """
  def __init__(self, xml_file_arg, debug_arg=False):
    self.version_str = "101029.1900"
    self.xml_file = xml_file_arg
    self.fqn = FullyQualifiedName()
    self.debug = debug_arg

    #
    # the following are used for the XML node list
    #
    self.nodes = []
    self.node =  {}

    if self.debug:
      print("xml file: \"%s\"" % self.xml_file)

    doc = xml.dom.minidom.parse(self.xml_file)
    self.__process_node(doc, 0)
    # append the last node here...
    self.__push_node_list()

  def getNodes(self):
    return self.nodes

  ##
  ## private methods
  ##
  def __process_node(self, n, level):
    indent = "  " * level
    text = ""

    if self.debug:
      print("%s node name: %s" % (indent, n.nodeName))
    if (n.nodeType == xml.dom.minidom.Node.ELEMENT_NODE):
      self.fqn.insert(n.nodeName, level-1)
      if self.debug:
        print("%s nodeType: ELEMENT_NODE" % indent)
        print("%s fqn name:  %s" % (indent, self.fqn.get()))
      #
      # push data from previous node onto nodes list
      #
      """
      first test to see if child nodes contain CDATA sections, if so,
      append to text
      """
      cdata_text = ''
      if (n.hasChildNodes()):
        cnl = n.childNodes
        for cn in cnl:
          #print('cn.nodeType: %s' % cn.nodeType)
          if cn.nodeType == xml.dom.minidom.Node.CDATA_SECTION_NODE:
            #print('CDATA_SECTION_NODE')
            cdata_text += ' ' + cn.nodeValue
        cdata_text = cdata_text.strip()
      self.__push_node_list()
      self.node['attributes'] = {}
      #self.node['text'] = ''
      self.node['text'] = cdata_text
      self.node['fqname'] = self.fqn.get()

    if (n.nodeType == xml.dom.minidom.Node.ATTRIBUTE_NODE):
      if self.debug:
        print("%s nodeType: ATTRIBUTE_NODE" % indent)
    if (n.nodeType == xml.dom.minidom.Node.TEXT_NODE):
      text = n.nodeValue
      if self.debug:
        print("%s nodeType: TEXT_NODE" % indent)
    if (n.nodeType == xml.dom.minidom.Node.CDATA_SECTION_NODE):
      if self.debug:
        print("%s nodeType: CDATA_SECTION_NODE" % indent)
        print('###')
        print('type(n):     %s' % type(n))
        print('n.nodeName:  %s' % n.nodeName)
        print('n.nodeValue: %s' % n.nodeValue)
        print('n:')
        print(n)
        print('###')
    if (n.nodeType == xml.dom.minidom.Node.ENTITY_REFERENCE_NODE):
      if self.debug:
        print("%s nodeType: ENTITY_REFERENCE_NODE" % indent)
    if (n.nodeType == xml.dom.minidom.Node.ENTITY_NODE):
      if self.debug:
        print("%s nodeType: ENTITY_NODE" % indent)
    if (n.nodeType == xml.dom.minidom.Node.PROCESSING_INSTRUCTION_NODE):
      if self.debug:
        print("%s nodeType: ENTITY_NODE" % indent)
    if (n.nodeType == xml.dom.minidom.Node.COMMENT_NODE):
      if self.debug:
        print("%s nodeType: COMMENT_NODE" % indent)
    if (n.nodeType == xml.dom.minidom.Node.DOCUMENT_NODE):
      if self.debug:
        print("%s nodeType: DOCUMENT_NODE" % indent)
    if (n.nodeType == xml.dom.minidom.Node.DOCUMENT_TYPE_NODE):
      if self.debug:
        print("%s nodeType: DOCUMENT_TYPE_NODE" % indent)
    if (n.nodeType == xml.dom.minidom.Node.DOCUMENT_FRAGMENT_NODE):
      if self.debug:
        print("%s nodeType: DOCUMENT_FRAGMENT_NODE" % indent)
    if (n.nodeType == xml.dom.minidom.Node.NOTATION_NODE):
      if self.debug:
        print("%s nodeType: NOTATION_NODE" % indent)

    # show attributes
    al = n.attributes
    if (al):
      av = {}
      for attr_k in al.keys():
        #node['attributes'] = []
        attr_v = al[attr_k]
        av[attr_k] = attr_v.nodeValue
        if self.debug:
          print("%s %s=\"%s\"" % (indent, attr_k, attr_v.nodeValue))
      self.node['attributes'] = av

    # show text
    #print ('len(text): %d' % len(text))
    if (len(text) > 0):
      # todo: make sure we handle all types of text encodings
      clean_text = text.strip()
      self.node['text'] += ' ' + clean_text

      #
      # why is this here??
      #
      cleaner_text = ''
      try:
        cleaner_text = clean_text.encode('latin-1')
      except:
        cleaner_text = clean_text

      if self.debug:
        try:
          print("%s >>>%s<<<" % (indent, cleaner_text))
        except UnicodeEncodeError:
          print("UnicodeEncodeError1...")
          sys.stdout.write("E1>")
          #print(clean_text.encode('latin-1'))
          sys.stdout.write("<E1")
        except:
          print("UnicodeEncodeError2...")
        finally:
          pass

        print("")

    # recurse
    if (n.hasChildNodes()):
      cnl = n.childNodes
      for cn in cnl:
        self.__process_node(cn, level+1)
  # end of def __process_node(self, n, level):

  def __push_node_list(self):
    """
    Explanation of node list:
      self.nodes: list of nodes

    Each node is a dictionary:
      self.node['attributes'] is a dictionary of XML name/value pairs
      self.node['text']       is the text of the XML node
      self.node['fqtag']      is the fully qualified name of the node
                                [or element??]
    """
    if len(self.node) < 1:
      return

    self.node['text'] = self.node['text'].strip()
    self.nodes.append(self.node)
    self.node =      {}


class FullyQualifiedName():
  """
  maintain record of period-delimited name of XML elements
  for example:
  
    "rss.channel.item.description"
  """
  def __init__(self):
    self.fqn = []
    self.len = 0;
    for i in range(256):
      self.fqn.append('')

  def insert(self, text, i):
    """
    insert text at i'th postion, truncating any values beyond i
      FullyQualifiedName.get()            # returns "a.b.c.d.e.f.g.h"
      FullyQualifiedName.insert("zzz", 4) 
      FullyQualifiedName.get()            # returns "a.b.c.d.zzz"
    """
    self.fqn[i] = text;
    self.len = i + 1
    for j in range(self.len, 256): # wipe out stuff at higher indices
      self.fqn[j] = ''

  def getList(self):
    """
    get list of names in the fully qualified name
    """
    return self.fqn

  def get(self):
    """
    get the period-delimited name
    """
    rv = "";
    for i in range(self.len):
      if (i > 0):
        rv += "."
      rv += self.fqn[i]
      
    return rv

