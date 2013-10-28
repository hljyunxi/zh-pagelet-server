# coding=utf-8

import logging
import os
import json

class AjaxResponse(object):
  def __init__(self, pagelets = []):
    self.error_flag = 0
    self.message = ''
    self.redirect_url = ''
    self.refresh_flag = 0
    self.pagelets = pagelets
    self.extra_data = None
  
  """Extra json data object send to client.
    Custom json data.
  """
  def set_data(self, extra_data = None):
    self.extra_data = extra_data
    return self
    
  def set_refresh(self, is_refresh = 1):
    self.refresh_flag = is_refresh  
    return self
  
  """Redirect url
    if message is set, show msg first then redirect to this url.
  """
  def set_redirect(self, redirect_url = ''):
    self.redirect_url = redirect_url
    return self
  
  def set_error_flag(self, is_error = 1):
    self.error_flag = 1
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
      'error': self.error_flag,
      'message': self.message,
      'redirect': self.redirect_url,
      'refresh': self.refresh_flag,
      'data': self.extra_data,
      'pagelets': self.get_pagelet_json_objects()
    }
    return json.dumps(result)
    
  def add_pagelet(self, pagelet):
    self.pagelets.append(pagelet)