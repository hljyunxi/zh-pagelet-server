# coding=utf-8

# import webapp2
# import jinja2
import os
import time, datetime
import json
from zh_node_default_renderer import ZNodeDefaultRenderer

#NOTE: Do we need provide a method to set template name at runtime?
class ZNode(object):
  template_ = ''
  # eg. Seajs module path, this give info to client to load it's script, before create the node.
  # the script and it's childs's script will be batch fetched at once.
  js_path = ''
  css_path = ''
  meta = {}
  root_node_id = None
  child_nodes = []
  
  def __init__(self, meta = {}, root_node_id = None, entity_context = None):
    self.view_data = {}
    self.template = self.template_
    # self.config = config 
    self.meta = meta
    
  #NOTE: Should set by ClientInfoMap.  
  def set_client_id(self, client_id):
    self.client_id = client_id
    
  def get_client_id(self):
    return self.client_id

  
  def add_child(self, child_node):
    child_node.set_parent(self)
    self.child_nodes.append(child_node)
    
  def get_view_data_item(self, key):
    if key in self.view_data.keys():
      return self.view_data[key]

  def set_view_data_item(self, key, data_item):
    self.view_data[key] = data_item

  def set_view_data(self, data):
    self.view_data = data

  def set_template(self, template):
    self.template = template
      
  def fetch_data(self):
    #NOTE: Subclass will override self method.
    pass
    
  def set_meta(self, key, value):
    self.meta[key] = value
    
  def get_meta(self, key):
    if key in self.meta:
      return self.meta[key]
    elif self.get_parent():
      return self.get_parent().get_meta(key)
      
    
  # def get_config(self, key):
  #   return self.config[key]
  
  def node_attribute(self):
    meta_data = self.meta
    # m = '&'.join(['{0}={1}'.format(k, str(meta_data[k]).replace('=', '○').replace('&', '⊕')) for k in meta_data ])
    # m = '&'.join(['{0}={1}'.format(k, str(meta_data[k]).replace('=', u'○').replace('&', u'⊕')) for k in meta_data ])
    m = json.dumps(meta_data)
    
    return ' id="{0}" data-meta=\'{1}\''.format(self.get_client_id(), m)
      
  def get_pagelet_meta(self):
    # self.type_string,
    # self.instance_identity,
    # self.markup,
    # self.child_nodes,
    # return [
    #   self.get_type(),
    #   self.get_client_id(),
    #   self.render()
    # ]
    # # TODO: WHY child nodes here ? Do we need this method?
    # return [
    #   self.get_type(),
    #   self.get_client_id(),
    #   self.render(),
    #   self.child_nodes
    # ]  
    pass  

  def get_renderer(self):
    return ZNodeDefaultRenderer(self.template, self.view_data)
      
  def render(self):
    self.fetch_data()
    self.set_view_data_item('node_attribute', self.node_attribute)
    renderer = self.get_renderer(self.template, self.view_data)
    return renderer.render()
    
    