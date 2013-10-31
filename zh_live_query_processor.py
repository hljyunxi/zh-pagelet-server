# coding=utf-8

import logging
import os
import json
import zh_client_info_map

NODE_NAME_MAP = {}

class LiveQueryProcessor(object):
	@classmethod
	def process(cls, queries = []):
		pagelets = []
		return pagelets

	@classmethod
	def create_node_instance(cls, node_name = '', meta = ''):
		node_instance = None
		if node_name in NODE_NAME_MAP.keys():
			node_constructor = NODE_NAME_MAP[node_name]
			node_instance = node_constructor(meta = meta)
			node_instance.set_infor_map(zh_client_info_map.ClientInfoMap())
			# How about context object ?Which should be IMP by user own.
	
		return node_instance