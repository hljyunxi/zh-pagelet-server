# coding=utf-8

import logging
import os
import json

class AjaxResponse(object):
  def __init__(self, parents_map):
    self.error_flag = 0
    self.message = ''
    self.redirect_url = ''
    self.refresh_flag = 0
    self.pagelets = []
    self.extra_data = None
    self.parents_map = parents_map
  
  """Extra json data object send to client.
    Custom json data.
  """
  def set_data(self, extra_data):
    self.extra_data = extra_data
    return self
    
  def set_refresh(self, is_refresh):
    if is_refresh:
      self.refresh_flag = 1
    else:
      self.refresh_flag = 0
    
    return self
  
  """Redirect url
    if message is set, show msg first then redirect to this url.
  """
  def set_redirect(self, redirect_url):
    self.redirect_url = redirect_url
    return self
  
  def set_error_flag(self, is_error):
    if is_error:
      self.error_flag = 1
    else:
      self.error_flag = 0
    
    return self
      
  """String message send to client
    Success or fail message.
  """
  def set_message(self, message):
    self.message = message
    return self
    
  def get_pagelet_json_objects(self):
    pagelet_json_objects = [ p.get_json_object() for p in self.pagelets]
    return pagelet_json_objects
    
  def clear_all_pageletes(self):
    self.pagelets = [];
  
  def get_json(self):
    #ru: redirect_url, rf: refresh_flag, p: pagelets, d: extra_data, rn:root_nodes, mp: parents_map

    result = {
      'r': self.error_flag,
      'msg': self.message,
      'ru': self.redirect_url,
      'rf': self.refresh_flag,
      'd': self.extra_data,
      'mp': self.parents_map.get_parents_map(),
      'rn': self.parents_map.get_root_nodes(),
      'p': self.get_pagelet_json_objects()
    }
    return json.dumps(result)
  
  def get_pagelet_by_type(self, type_string):
    for p in self.pagelets:
      if p.type_string == CLIENT_TYPE_MAP[type_string]:
        return p
        
  def get_pagelets_by_type(self, type_string):
    found = []
    for p in self.pagelets:
      if p.type_string == CLIENT_TYPE_MAP[type_string]:
        found.append(p)
    
    return found
    
  def add_pagelet(self, pagelet):
    self.pagelets.append(pagelet)