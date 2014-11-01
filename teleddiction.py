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
import cgi
import datetime
import webapp2
import urllib2
from xml.etree import ElementTree
from google.appengine.ext import ndb
from google.appengine.api import users

guestbook_key = ndb.Key('Guestbook', 'default_guestbook')

class Greeting(ndb.Model):
  author = ndb.UserProperty()
  content = ndb.TextProperty()
  date = ndb.DateTimeProperty(auto_now_add=True)


class MainPage(webapp2.RequestHandler):
  def get(self):
    self.response.out.write("""<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
    	<meta http-equiv="content-type" content="text/html; charset=utf-8" />
		<title>Teleddiction</title>
		<link type="text/css" rel="stylesheet" href="stylesheets/default.css" />
    </head>
    <body>
    <div id="header">
	<div id="logo">
		<h1>Teleddiction</h1>
		<h2>By Group 3</h2>
	</div>
	<div id="menu">
		<ul>
			<li><a href="#">Home</a></li>
			<li><a href="#">About</a></li>
			<li><a href="#">Search</a></li>
		</ul>
	</div>
</div>
<div>""")

    greetings = ndb.gql('SELECT * '
                        'FROM Greeting '
                        'WHERE ANCESTOR IS :1 '
                        'ORDER BY date DESC LIMIT 10',
                        guestbook_key)

    for greeting in greetings:
      if greeting.author:
        self.response.out.write('<b>%s</b> wrote:' % greeting.author.nickname())
      else:
        self.response.out.write('An anonymous person wrote:')
      self.response.out.write('<blockquote>%s</blockquote>' %
                              cgi.escape(greeting.content))


    self.response.out.write("""</div><div>
          <form action="/sign" method="post">
            <div><textarea name="content" rows="3" cols="60"></textarea></div>
            <div><input type="submit" value="Sign Guestbook"></div>
          </form></div>
		  <div id="footer">
			<p id="legal">&copy;2014 Teleddiction. All Rights Reserved. Designed by Group 3</p>
		  </div>
        </body>
      </html>""")


class Guestbook(webapp2.RequestHandler):
  def post(self):
    greeting = Greeting(parent=guestbook_key)

    if users.get_current_user():
      greeting.author = users.get_current_user()

    greeting.content = self.request.get('content')
    greeting.put()
    self.redirect('/')

class GetShows(webapp2.RequestHandler):
  def get(self):
	url = 'http://services.tvrage.com/feeds/show_list.php'
	u = urllib2.urlopen(url)
	self.response.out.write(u)
	
	
app = webapp2.WSGIApplication([
  ('/', MainPage),
  ('/sign', Guestbook),
  ('/getShows', GetShows)
], debug=True)