#!/usr/bin/python3

from wsgiref.handlers import CGIHandler
import os
import traceback
import linecache
import sys
import site 
from pprint import pprint

f1 = open('./testfile.txt','w+')

site.addsitedir('/public/homepages/s1245947/cgi/site-packages')

app = None
try:
	import d3_style
	app = d3_style.app
except Exception as e:
			exc_type, exc_value, exc_tb = sys.exc_info()
			pprint(traceback.format_exception(exc_type, exc_value, exc_tb), stream=f1)

class ScriptNameStripper(object):
	def __init__(self, app):
		self.app = app
	def __call__(self, environ, start_response):
		environ['SCRIPT_NAME'] = 'http://homepages.inf.ed.ac.uk/cgi/s1245947/'
		try:       
			return self.app(environ, start_response)
		except Exception as e:
			exc_type, exc_value, exc_tb = sys.exc_info()
			pprint(traceback.format_exception(exc_type, exc_value, exc_tb), stream=f1)

app = ScriptNameStripper(app)

	
try:
	CGIHandler().run(app)
except Exception as e:
			exc_type, exc_value, exc_tb = sys.exc_info()
			pprint(traceback.format_exception(exc_type, exc_value, exc_tb), stream=f1)
