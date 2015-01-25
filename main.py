#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import webapp2
from google.appengine.ext import ndb
from urllib2 import urlopen
import  json 
import time
import jinja2
import os

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class userMember(ndb.Model):
  Store_tags = ndb.StringProperty()

  

class MainHandler(webapp2.RequestHandler):
    def get(self):
    	user="karanisverma"
    	url="http://feeds.delicious.com/v2/json/networkmembers/"+user
    	obj = urlopen(url)
    	network_Members=json.load(obj)
    	
    	for network_Member in network_Members:
    		nm_dict=network_Member
    		nm_username=nm_dict["user"]
    		nm_date=nm_dict["dt"]
		template_values = {
				'members':nm_dict,
		        'user': nm_username,
		        'date':nm_date
		    }

		template = JINJA_ENVIRONMENT.get_template('index.html')
		self.response.write(template.render(template_values))

class UserProfile(webapp2.RequestHandler):
	def get(self, user=None):
		nm_tags=urlopen("http://feeds.delicious.com/v2/json/tags/"+user+"?count=10")
		nm_tags_obj=json.load(nm_tags)

		template_values = {
			'user':user,
			'tag_dict':nm_tags_obj
			}

		template = JINJA_ENVIRONMENT.get_template('tag.html')
		self.response.write(template.render(template_values))		

class FormPost(webapp2.RequestHandler):
	def post(self):
		self.response.write(self.request.POST.get('user'))
		#self.response.write("user1 value is="+self.request.POST.get('user1'))
		um=userMember(Store_tags=self.request.POST.get('user'))
		um.put()
		





app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/user/(\w+)',UserProfile),
    ('/submit', FormPost),
], debug=True)

