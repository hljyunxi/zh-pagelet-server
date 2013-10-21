# coding=utf-8

# import webapp2
# import jinja2
import os
import time, datetime
import json

# jinja_environment = jinja2.Environment(
#   loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__) + '/../templates/default')))

class ZNodeDefaultRenderer(object):
	template = ''
	view_data = {}
	def __init__(self, template = '', view_data = {}):
		super(ZNodeDefaultRenderer, self).__init__()

	def render(self):
		return 'Implement your own template renderer is required.'
		# template = jinja_environment.get_template(self.template)
 	  # return template.render(self.view_data)
