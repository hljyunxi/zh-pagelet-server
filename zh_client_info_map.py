# coding=utf-8

# import webapp2
# import jinja2
import os
import time, datetime
import json
import uuid

class ClientInfoMap(object):
	def __init__(self):
		super(ClientInfoMap, self).__init__()
		self.infor_map = {}
		self.dependency_tree = []
		self.inc_id = 0
		# Create a unique prefix.
		self.prefix = uuid.uuid1().hex[0:5]

	def generate_client_id(self):
		new_id = self.prefix + '-' + str(self.inc_id)
		self.inc_id += 1
		return new_id

	# Write out to page.
	def get_infor_map_json(self):
		return json.dumps(self.infor_map)

	# Write out to page.
	def get_dependency_tree_json(self):
		return json.dumps(self.dependency_tree)

	# def assign_unique_id_(self, new_node):
	# 	pass

	# def add_root_node(self, root_node):
	# 	self.root_node_list.append(root_node)

	def add_tree_dependency(self, js_path):
		self.dependency_tree.append(js_path)

	def add_relationship(self, parent_node = 'ROOT', child_node = None):
		if parent_node != 'ROOT':
			parent_id = parent_node.get_client_id()
		else:
			parent_id = parent_node

		if parent_id not in self.infor_map.keys():
			self.infor_map[parent_id] = []

		# self  .infor_map[parent_id].append({'id': child_node.get_client_id(), 'js': child_node.get_module_name()})
		self.infor_map[parent_id].append({'id': child_node.get_client_id(), 'js': child_node.get_module_name(), 'css': child_node.get_css_path(), 'meta': child_node.meta})



