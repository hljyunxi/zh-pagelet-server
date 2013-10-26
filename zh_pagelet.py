import logging
import os
import json
import zh_node


class Pagelet(object):
  no_contents_ = False
  def __init__(self, znode_instance, type_string = '', client_id = '', markup = ''):
    self.znode = None
    if znode_instance:
      self.znode = znode_instance
      self.type_string = znode_instance.get_type()
      self.client_id = znode_instance.get_client_id()
    else:
      self.type_string = type_string
      self.client_id = client_id
      self.markup = markup
      
    self.ref_element = ''
    # default set to decoration, case most use case is in the handler, to append
    # extra pagelet to page, and in live query, default set to UPDATING.
    self.render_type = PAGELET_RENDER_TYPE.DECORATION
    self.render_position = PAGELET_RENDER_POSITION.APPEND
    self.event_type = ''
    self.event_args = '' #Should be json object.
    
  def set_no_contents(self):
    self.no_contents_ = True
    
  def set_ref_element(self, ref_element):
    self.ref_element = ref_element
    return self
  
  def set_render_type(self, render_type):
    self.render_type = render_type
    return self
    
  def set_render_position(self, render_position):
    self.render_position = render_position
    return self
    
  def set_event(self, event_type_string, event_arg_string):
    #NOTE: Currently we don't support multi events.
    self.event_type = event_type_string
    self.event_args = event_arg_string
    return self
    
  def get_node_instance(self):
    return self.znode
  
  def get_json_object(self):
    if self.znode:
      node_meta_json = self.znode.get_pagelet_meta()
    else:
      node_meta_json = [
        self.type_string,
        self.client_id,
        self.markup
      ]
      
    # Clear all html contents.
    if self.no_contents_:
      node_meta_json[2] = ''
      
    node_meta_json.extend([
      self.ref_element,
      self.render_type,
      self.render_position,
      self.event_type,
      self.event_args
    ])
    return node_meta_json