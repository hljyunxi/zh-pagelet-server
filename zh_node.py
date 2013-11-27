# coding=utf-8

import os
import time, datetime
import json
from zh_node_default_renderer import ZNodeDefaultRenderer
import zh_client_info_map

#NOTE: Do we need provide a method to set template name at runtime?
class ZNode(object):
  def __init__(self, meta = {}, parent_node = None):
    super(ZNode, self).__init__()
    self.template = ''
    # eg. Seajs module path, this give info to client to load it's script, before create the node.
    # the script and it's childs's script will be batch fetched at once.
    # Should be assign by subclass.
    self.js_path = '' 
    self.css_path = '' 
    self.meta = {} 
    self.config = {} # This won't be transfered during update.
    # End for assign.
    self.client_id = ''
    self.child_nodes = []
    self.parent_node_id = None
    self.infor_map = None
    self.is_root_node_ = False

    self.view_data = {} 
    self.meta = meta # Merge all config options here.

  def get_css_path(self):
    return self.css_path

  def is_root_node(self):
    return self.is_root_node_

  def set_infor_map(self, infor_map):
    self.infor_map = infor_map
    self.infor_map.add_tree_dependency(self.js_path)

  def get_infor_map(self):
    if not self.infor_map:
      self.set_infor_map(zh_client_info_map.ClientInfoMap())
      self.self.is_root_node_ = True

    return self.infor_map

  def get_js_module_name(self):
    return self.js_path
    
  #NOTE: Should set by ClientInfoMap.  
  def set_client_id_(self, client_id):
    self.client_id = client_id
    
  def get_client_id(self):
    if not self.client_id:
      self.set_client_id_(self.get_infor_map().generate_client_id())
    return self.client_id

  def add_child(self, child_node):
    if child_node.is_root_node():
      raise Exception('Can not add root node as child.')

    child_node.set_infor_map(self.get_infor_map())

    self.infor_map.add_relationship(parent_node = self, child_node = child_node)
    # Why we want keep a child_nodes refference?
    # TBD
    # self.child_nodes.append(child_node)
    
  def get_view_data_item(self, key):
    if key in self.view_data.keys():
      return self.view_data[key]

  def set_view_data_item(self, key, data_item):
    self.view_data[key] = data_item

  def set_view_data(self, data):
    self.view_data = data
      
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
  
  def get_node_attribute(self):
    return {
      'id': self.get_client_id(),
      'meta': json.dumps(self.meta),
      'config': json.dumps(self.config)
    }
      
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

  def get_renderer(self, template = '', view_data = None):
    return ZNodeDefaultRenderer(template, view_data)
      
  def render(self):
    if self.is_root_node():
      self.get_infor_map().add_relationship('ROOT', self)
    
    self.fetch_data()
    node_attribute = self.get_node_attribute()
    self.set_view_data_item('node_client_id', node_attribute['id'])
    # self.set_view_data_item('node_meta_json', node_attribute['meta'])
    # self.set_view_data_item('node_config_json', node_attribute['config'])
    renderer = self.get_renderer(template = self.template, view_data = self.view_data)
    return renderer.render()
    
    