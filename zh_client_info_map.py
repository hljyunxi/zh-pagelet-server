# coding=utf-8

# import webapp2
# import jinja2
import os
import time, datetime
import json


class ClientInfoMap(object):
	map = {}
	root_node_list = []

	def add_root_node_(self, root_node):
		pass

	def assign_unique_id_(self, new_node):
		pass

	def add_relatiionship(self, parent_node, child_node = None):
		if not child_node:
			pass
			# This is a root node
		pass
