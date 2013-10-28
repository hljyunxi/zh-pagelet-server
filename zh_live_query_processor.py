# coding=utf-8

import logging
import os
import json

NODE_NAME_MAP = {}

class LiveQueryProcessor(object):
	@class_method
	def process(cls, queries = []):
		pagelets = []
		return pagelets

	def create_node_instance(cls, node_name = '', meta = ''):
		node_instance = node_name
		return node_instance