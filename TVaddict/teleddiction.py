import cgi
import datetime
import webapp2
import urllib2
import os
from xml.etree import ElementTree
from google.appengine.ext import ndb
from google.appengine.api import users
from google.appengine.ext.webapp import template

def render_template(handler, templatename, templatevalues):
    path = os.path.join(os.path.dirname(__file__), templatename)
    html = template.render(path, templatevalues)
    handler.response.out.write(html)
	
guestbook_key = ndb.Key('Guestbook', 'default_guestbook')

class Message(ndb.Model):
  userTo = ndb.UserProperty()
  userFrom = ndb.UserProperty()
  sentDate = ndb.DateTimeProperty(auto_now_add=True)
  content = ndb.StringProperty()
  
class User(ndb.Model):
  user = ndb.UserProperty()
  shows = ndb.StringProperty(repeated=True)
  bio = ndb.StringProperty()
  name = ndb.StringProperty()
  age = ndb.IntegerProperty()
  gender = ndb.StringProperty()
  messages = ndb.StructuredProperty(Message, repeated=True)
  
class Greeting(ndb.Model):
  id = ndb.IntegerProperty()
  author = ndb.UserProperty()
  content = ndb.TextProperty()
  date = ndb.DateTimeProperty(auto_now_add=True)
  rating = ndb.IntegerProperty()
  upvoted = ndb.UserProperty(repeated=True)
  downvoted = ndb.UserProperty(repeated=True)

class Episode(ndb.Model):
  tvid = ndb.StringProperty()
  epnumber = ndb.IntegerProperty()
  date = ndb.DateTimeProperty()
  rating = ndb.IntegerProperty()
  commentids = ndb.IntegerProperty(repeated=True)
  
class TVShow(ndb.Model):
  id = ndb.StringProperty()
  name = ndb.StringProperty()
  imgsrc = ndb.StringProperty()
  genre = ndb.StringProperty()
  airtime = ndb.DateTimeProperty()
  runtime = ndb.IntegerProperty()
  rating = ndb.IntegerProperty()
  tracking = ndb.IntegerProperty()
  
class MainPage(webapp2.RequestHandler):
  def get(self):
	user = users.get_current_user()
    
	login_url = ''
	logout_url = ''
	name = ''
	
	if user:
		logout_url = users.create_logout_url('/')
		name = user.nickname()
	else:
		login_url = users.create_login_url('/')
	
	template_values = {
		'login' : login_url,
		'logout' : logout_url,
		'nickname' : name
	}
	
	render_template(self, 'index.html', template_values)
	
class SingleShowPage(webapp2.RequestHandler):
  def get(self):
	user = users.get_current_user()
    
	login_url = ''
	logout_url = ''
	name = ''
	
	if user:
		logout_url = users.create_logout_url('/')
		name = user.nickname()
	else:
		login_url = users.create_login_url('/')
	
	template_values = {
		'login' : login_url,
		'logout' : logout_url,
		'nickname' : name
	}
	
	render_template(self, 'show.html', template_values)
	
class UserProfile(webapp2.RequestHandler):
  def get(self):
	user = users.get_current_user()
    
	login_url = ''
	logout_url = ''
	name = ''
	
	if user:
		logout_url = users.create_logout_url('/')
		name = user.nickname()
	else:
		login_url = users.create_login_url('/')
	
	template_values = {
		'login' : login_url,
		'logout' : logout_url,
		'nickname' : name
	}
	
	render_template(self, 'profile.html', template_values)
		
class EpisodeView(webapp2.RequestHandler):
  def get(self):
	user = users.get_current_user()
    
	login_url = ''
	logout_url = ''
	name = ''
	
	if user:
		logout_url = users.create_logout_url('/')
		name = user.nickname()
	else:
		login_url = users.create_login_url('/')
	
	template_values = {
		'login' : login_url,
		'logout' : logout_url,
		'nickname' : name
	}
	
	render_template(self, 'episode.html', template_values)	
		
class ShowList(webapp2.RequestHandler):
  def get(self):
	user = users.get_current_user()
    
	login_url = ''
	logout_url = ''
	name = ''
	number = 2484
	
	if user:
		logout_url = users.create_logout_url('/')
		name = user.nickname()
	else:
		login_url = users.create_login_url('/')
	
	template_values = {
		'login' : login_url,
		'logout' : logout_url,
		'nickname' : name,
		'number' : number
	}
	
	render_template(self, 'showlist.html', template_values)

class Comments(webapp2.RequestHandler):
  def get(self):
	user = users.get_current_user()
    
	login_url = ''
	logout_url = ''
	name = ''
	up = []
	down = []
	
	if user:
		logout_url = users.create_logout_url('/comments')
		name = user.nickname()
	else:
		login_url = users.create_login_url('/comments')
	
	greetings = ndb.gql('SELECT * '
						'FROM Greeting '
						'WHERE ANCESTOR IS :1 '
						'ORDER BY rating DESC LIMIT 10',
						guestbook_key)
	if user:					
		for greeting in greetings:
			for upped in greeting.upvoted:
				if user == upped:
					up.append(greeting.id)
			for downed in greeting.downvoted:
				if user == downed:
					down.append(greeting.id)
		
	template_values = {
		'login' : login_url,
		'logout' : logout_url,
		'nickname' : name,
		'comments' : greetings,
		'up' : up,
		'down' : down
	}
	
	render_template(self, 'comments.html', template_values)
	
class Comment(webapp2.RequestHandler):
  def post(self):
	greeting = Greeting(parent=guestbook_key)

	if users.get_current_user():
		greeting.author = users.get_current_user()
	
	result = ndb.gql('SELECT * FROM Greeting')
	number = result.count()
	
	greeting.id = number;
	greeting.content = self.request.get('content')
	greeting.rating = 0
	greeting.put()
	self.redirect('/comments')

class Rate(webapp2.RequestHandler):
  def post(self):
	toVote = self.request.get('updown')
	comId = int(self.request.get('comId'))
	user = users.get_current_user()
	
	com_query = Greeting.query((Greeting.id == comId))
	com = com_query.get()
	
	if( toVote == "1"):
		com.rating = com.rating + 1;
		com.upvoted.append(user)
		for downed in com.downvoted:
			if user == downed:
				com.downvoted.remove(user)
				com.rating = com.rating + 1;
	else:
		com.rating = com.rating - 1;
		com.downvoted.append(user)
		for upped in com.upvoted:
			if user == upped:
				com.upvoted.remove(user)
				com.rating = com.rating - 1;
		
	com.put()
	self.redirect('/comments')
	
class GetShows(webapp2.RequestHandler):
  def get(self):
	url = 'http://services.tvrage.com/feeds/show_list.php'
	request = urllib2.Request(url, headers={"Accept" : "application/xml"})
	u = urllib2.urlopen(request)
	tree = ElementTree.parse(u)
	rootElem = tree.getroot()
	
	self.response.out.write("""<html><body>""")
	
	for show in rootElem.findall('show'):
		if( show.find('status').text == "1"):
			if(show.find('country').text == "US"):
				id = show.find('id').text
				tvshow_query = TVShow.query((TVShow.id == id))
				show = tvshow_query.get()
				if not show:
					tvshow = TVShow()
					tvshow.id = id
					tvshow.put()
	
	u.close()
	self.response.out.write("""</body></html>""")
	
  def post(self):
	url = 'http://services.tvrage.com/feeds/show_list.php'
	request = urllib2.Request(url, headers={"Accept" : "application/xml"})
	u = urllib2.urlopen(request)
	tree = ElementTree.parse(u)
	rootElem = tree.getroot()
		
	self.response.out.write("""<html><body>""")
		
	for show in rootElem.findall('show'):
		if( show.find('status').text == "1"):
			if(show.find('country').text == "US"):
				id = show.find('id').text
				tvshow_query = TVShow.query((TVShow.id == id))
				show = tvshow_query.get()
				if not show:
					tvshow = TVShow()
					tvshow.id = id
					tvshow.put()
	
	u.close()
	self.response.out.write("""</body></html>""")
	
class SearchShow(webapp2.RequestHandler):
  def get(self):
	tvshow_query = TVShow.query((TVShow.name == None))
	shows = tvshow_query.fetch(limit=10)
	for show in shows:
		url = 'http://services.tvrage.com/feeds/full_show_info.php?sid=' + show.id
		request = urllib2.Request(url, headers={"Accept" : "application/xml"})
		u = urllib2.urlopen(request)
		tree = ElementTree.parse(u)
		rootElem = tree.getroot()
		
		show.imgsrc = rootElem.find('image').text
		show.genre = rootElem.find('classification').text
		airtimeStr = rootElem.find('airtime').text
		show.airtime = datetime.datetime.strptime(airtimeStr, "%H:%M")
		show.runtime = int(rootElem.find('runtime').text)
		show.rating = 0;
		
		episodes = rootElem.findall(".//episode")
		for episode in episodes:
			epi = Episode()
			epi.tvid = show.id
			epi.epnumber = int(episode.find('epnum').text)
			dateStr = episode.find('airdate').text
			epi.date = datetime.datetime.strptime(dateStr, "%Y-%m-%d")
			epi.rating = 0
			epi.put()
		
		show.name = rootElem.find('name').text
		show.put()
		
		u.close()
		
app = webapp2.WSGIApplication([
  ('/', MainPage),
  ('/comment', Comment),
  ('/show', SingleShowPage),
  ('/profile',UserProfile),
  ('/showlist', ShowList),
  ('/episode', EpisodeView),
  ('/comments', Comments),
  ('/rate', Rate),
  ('/getShows', GetShows),
  ('/searchShow', SearchShow)
], debug=True)