# coding=utf-8

# import webapp2
# import jinja2
import os
import time, datetime
import json
import uuid

class ClientInfoMap(object):
	info_map = {}
	root_node_list = {}
	inc_id = 0
	# Create a unique prefix.
	prefix = uuid.uuid1().hex[0:5]

	def generate_client_id(self):
		new_id = self.prefix + '-' + str(self.inc_id)
		self.inc_id += 1
		return new_id

	# Write out to page.
	def get_info_map_json(self):
		return json.dumps(self.info_map)

	# Write out to page.
	def get_root_list_json(self):
		return json.dumps(self.root_node_list)

	# def assign_unique_id_(self, new_node):
	# 	pass

	# def add_root_node(self, root_node):
	# 	self.root_node_list.append(root_node)

	def add_tree_dependency(self, root_node_id, js_path):
		if root_node_id in self.root_node_list.keys():
			self.root_node_list[root_node_id].append(js_path)
		else:
			self.root_node_list[root_node_id] = [js_path];

	def add_relationship(self, parent_node = 'ROOT', child_node = None):
		if parent_node != 'ROOT':
			parent_id = parent_node.get_client_id()
		else:
			parent_id = parent_node

		if parent_id in self.info_map.keys():
			# 'constructorName, ClientId'
			self.info_map[parent_id].append([child_node.get_constructor_name(), child_node.get_client_id()])
		else:
			self.info_map[parent_id] = [child_node.get_constructor_name(), child_node.get_client_id()]


