# coding=utf-8

# import webapp2
# import jinja2
import os
import time, datetime
import json
from zh_node_default_renderer import ZNodeDefaultRenderer

#NOTE: Do we need provide a method to set template name at runtime?
class ZNode(object):
  template = ''
  # eg. Seajs module path, this give info to client to load it's script, before create the node.
  # the script and it's childs's script will be batch fetched at once.
  # Should be assign by subclass.
  constructor_name = ''
  js_path = ''
  css_path = ''
  meta = {}
  # End for assign.
  client_id = ''
  child_nodes = []
  root_node_id = 'ROOT'
  infor_map = None
  context = None
  is_root = False
  
  def __init__(self, meta = {}, parent_node = None):
    self.view_data = {}
    # self.config = config 
    self.meta = meta

    if parent_node:
      self.root_node_id = parent_node.root_node_id
      self.set_infor_map(parent_node.infor_map)
      self.set_context(parent_node.context)
    else:
      self.marked_as_root_node()

  def get_css_path(self):
    return self.css_path

  def set_infor_map(self, infor_map):
    self.infor_map = infor_map
    if not self.client_id:
      self.set_client_id(self.infor_map.generate_client_id())
      if self.is_root:
        self.root_node_id = self.get_client_id()
        self.infor_map.add_relationship('ROOT', self)

      self.infor_map.add_tree_dependency(self.root_node_id, self.js_path)

  def set_context(self, context):
    self.entity_context = context

  def marked_as_root_node(self):
    self.is_root = True

  def get_module_name(self):
    return self.js_path

  def get_constructor_name(self):
    return self.constructor_name
    
  #NOTE: Should set by ClientInfoMap.  
  def set_client_id(self, client_id):
    self.client_id = client_id
    
  def get_client_id(self):
    return self.client_id

  
  def add_child(self, child_node):
    # We don't need a pointer to parent node.
    #child_node.set_parent(self)
    self.infor_map.add_relationship(parent_node = self, child_node = child_node)
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
  
  def get_node_attribute(self):
    meta_data = self.meta
    # m = '&'.join(['{0}={1}'.format(k, str(meta_data[k]).replace('=', '○').replace('&', '⊕')) for k in meta_data ])
    # m = '&'.join(['{0}={1}'.format(k, str(meta_data[k]).replace('=', u'○').replace('&', u'⊕')) for k in meta_data ])
    m = json.dumps(meta_data)
    
    return {
      'id': self.get_client_id(),
      'meta': m
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
    self.fetch_data()
    node_attribute = self.get_node_attribute()
    self.set_view_data_item('node_client_id', node_attribute['id'])
    self.set_view_data_item('node_meta_json', node_attribute['meta'])
    renderer = self.get_renderer(template = self.template, view_data = self.view_data)
    return renderer.render()
    
    