import logging
import os
import json
import zh_node

class PAGELET_RENDER_TYPE(object):
  UPDATING = 'updating'
  DECORATION = 'decoration'
  UN_RENDER = 'un_render'
    
class PAGELET_RENDER_POSITION(object):
  INNER = 'inner'
  APPEND = 'append'
  BEFORE = 'before'
  AFTER = 'after'

class Pagelet(object):
  @classmethod
  def from_node_instance(cls, node_instance):
    return Pagelet(node_instance = node_instance)

  @classmethod
  def update_for_node(cls, node_client_id = '', node_module_name = ''):
    return Pagelet(node_client_id = node_client_id, node_module_name = node_module_name)

  def __init__(self, node_instance = None, node_client_id = '', node_module_name = ''):
    self.znode = node_instance
    
    # no instance is passing means we just want pass some message or un-render
    if not self.znode:
      self.root_nodes = {
        'ROOT': [{"id": node_client_id, "js": node_module_name}]
      }

    self.html = '' # from render() of znode instance.
    #root_nodes  from znode instance.
    # infor_map from znode instance.
    self.refer_node = ''
    # default set to decoration, case most use case is in the handler, to append
    # extra pagelet to page, and in live query, default set to UPDATING.
    self.render_type = PAGELET_RENDER_TYPE.DECORATION
    self.render_position = PAGELET_RENDER_POSITION.APPEND
    self.message = [] # Form events.
    
  def set_refer_node(self, refer_node):
    self.refer_node = refer_node
    return self
  
  def set_render_type(self, render_type):
    self.render_type = render_type
    return self
    
  def set_render_position(self, render_position):
    self.render_position = render_position
    return self
    
  def add_event(self, event_type_string, event_arg_string):
    # TBD: event_arg_string could be a json string.
    self.message.appen([event_type_string, event_arg_string])
    return self
    
  def get_node_instance(self):
    return self.znode
  
  def get_json_object(self):
    return {
      'html': self.znode.render if self.znode else '',
      'root_nodes': self.znode.get_infor_map().get_root_list_json() if self.znode else self.root_nodes,
      'infor_map': self.znode.get_infor_map().get_infor_map_json() if self.znode else {},
      'refer_node': self.refer_node,
      'render_type': self.render_type,
      'render_position': self.render_position,
      'message': self.message
    }
    