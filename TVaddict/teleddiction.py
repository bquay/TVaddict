import cgi
import datetime
import webapp2
import urllib2
import os
from xml.etree import ElementTree
from google.appengine.ext import ndb
from google.appengine.api import users
from google.appengine.ext.webapp import template
from google.appengine.api import urlfetch

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
  title = ndb.StringProperty()
  
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
	recentlyAired = []
	
	startTime_utc = datetime.datetime.now()
	#endTime_utc = startTime_utc - datetime.timedelta(minutes=30)
	
	#startTime = startTime_utc - datetime.timedelta(hours=5)
	#endTime = endTime_utc - datetime.timedelta(hours=5)
	
	#startTime = startTime.replace(year=1900)
	#startTime = startTime.replace(month=1)
	#startTime = startTime.replace(day=1)
	#endTime = endTime.replace(year=1900)
	#endTime = endTime.replace(month=1)
	#endTime = endTime.replace(day=1)
	
	dateTime = startTime_utc
	dateTime = dateTime.replace(hour=0)
	dateTime = dateTime.replace(minute=0)
	dateTime = dateTime.replace(second=0)
	dateTime = dateTime.replace(microsecond=0)
	
	endDate = dateTime - datetime.timedelta(days=3)
	endDate = endDate.replace(hour=0)
	endDate = endDate.replace(minute=0)
	endDate = endDate.replace(second=0)
	endDate = endDate.replace(microsecond=0)
	
	if user:
		logout_url = users.create_logout_url('/')
		name = user.nickname()
	else:
		login_url = users.create_login_url('/profile')
	
	topRating = ndb.gql('SELECT * FROM TVShow ORDER BY rating DESC LIMIT 7')
	epToday = ndb.gql('SELECT * FROM Episode WHERE date <= :1 AND date >= :2 ORDER BY date DESC LIMIT 7',dateTime, endDate)
	for ep in epToday:
		#showNow = ndb.gql('SELECT * FROM TVShow WHERE airtime <= :1 AND airtime >= :2 AND id = :3',startTime, endTime, ep.tvid)
		showNow = ndb.gql('SELECT * FROM TVShow WHERE id = :1',ep.tvid)
		recentlyAired.append(showNow.get())
	Reality = ndb.gql('SELECT * FROM TVShow WHERE genre = :1 LIMIT 7',"Reality")
	
	template_values = {
		'login' : login_url,
		'logout' : logout_url,
		'nickname' : name,
		'topRated' : topRating,
		'recentlyAired' : recentlyAired,
		'Reality' : Reality
	}
	
	render_template(self, 'index.html', template_values)
	
  def post(self):
	user = users.get_current_user()
	login_url = ''
	logout_url = ''
	name = ''
	recentlyAired = []
	
	startTime_utc = datetime.datetime.now()
	#endTime_utc = startTime_utc - datetime.timedelta(minutes=30)
	
	#startTime = startTime_utc - datetime.timedelta(hours=5)
	#endTime = endTime_utc - datetime.timedelta(hours=5)
	
	#startTime = startTime.replace(year=1900)
	#startTime = startTime.replace(month=1)
	#startTime = startTime.replace(day=1)
	#endTime = endTime.replace(year=1900)
	#endTime = endTime.replace(month=1)
	#endTime = endTime.replace(day=1)
	
	dateTime = startTime_utc
	dateTime = dateTime.replace(hour=0)
	dateTime = dateTime.replace(minute=0)
	dateTime = dateTime.replace(second=0)
	dateTime = dateTime.replace(microsecond=0)
	
	endDate = dateTime - datetime.timedelta(days=3)
	endDate = endDate.replace(hour=0)
	endDate = endDate.replace(minute=0)
	endDate = endDate.replace(second=0)
	endDate = endDate.replace(microsecond=0)
	
	if user:
		logout_url = users.create_logout_url('/')
		name = user.nickname()
	else:
		login_url = users.create_login_url('/profile')
	
	topRating = ndb.gql('SELECT * FROM TVShow ORDER BY rating DESC LIMIT 7')
	epToday = ndb.gql('SELECT * FROM Episode WHERE date <= :1 AND date >= :2 ORDER BY date DESC LIMIT 7',dateTime, endDate)
	for ep in epToday:
		#showNow = ndb.gql('SELECT * FROM TVShow WHERE airtime <= :1 AND airtime >= :2 AND id = :3',startTime, endTime, ep.tvid)
		showNow = ndb.gql('SELECT * FROM TVShow WHERE id = :1',ep.tvid)
		recentlyAired.append(showNow.get())
	Reality = ndb.gql('SELECT * FROM TVShow WHERE genre = :1 LIMIT 7',"Reality")
	
	template_values = {
		'login' : login_url,
		'logout' : logout_url,
		'nickname' : name,
		'topRated' : topRating,
		'recentlyAired' : recentlyAired,
		'Reality' : Reality
	}
	
	render_template(self, 'index.html', template_values)
	
class SingleShowPage(webapp2.RequestHandler):
  def get(self):
	user = users.get_current_user()
    
	login_url = ''
	logout_url = ''
	name = ''
	show = ''
	episodes = ''
	
	showid = self.request.get('showselect')
	show_query = TVShow.query((TVShow.id == showid))
	show = show_query.get()
	
	if show:
		episodes = Episode.query(Episode.tvid == show.id).fetch()
		episodes.sort(key=lambda x: x.date, reverse=True)
	
	if user:
		logout_url = users.create_logout_url('/')
		name = user.nickname()
	else:
		login_url = users.create_login_url('/profile')
	
	template_values = {
		'login' : login_url,
		'logout' : logout_url,
		'nickname' : name,
		'show' : show,
		'episodes' : episodes
	}
	
	render_template(self, 'show.html', template_values)
	
  def post(self):
	user = users.get_current_user()
    
	login_url = ''
	logout_url = ''
	name = ''
	show = ''
	episodes = ''
	
	showid = self.request.get('showselect')
	show_query = TVShow.query((TVShow.id == showid))
	show = show_query.get()
	
	if show:
		episodes = Episode.query(Episode.tvid == show.id).fetch()
		episodes.sort(key=lambda x: x.date, reverse=True)
	
	if user:
		logout_url = users.create_logout_url('/')
		name = user.nickname()
	else:
		login_url = users.create_login_url('/profile')
	
	template_values = {
		'login' : login_url,
		'logout' : logout_url,
		'nickname' : name,
		'show' : show,
		'episodes' : episodes
	}
	
	render_template(self, 'show.html', template_values)
	
class UserProfile(webapp2.RequestHandler):
  def get(self):
	user = users.get_current_user()
    
	login_url = ''
	logout_url = ''
	newUser =''
	shows = []
	
	if user:
		logout_url = users.create_logout_url('/')
	
		user_query = User.query((User.user == user))
		oldUser = user_query.get()
		if oldUser:
			newUser = oldUser
			for userShow in oldUser.shows:
				userShows_query = TVShow.query(TVShow.id == userShow)
				shows.append(userShows_query.get())
		else:
			newUser = User()
			newUser.user = user
			newUser.put()
	else:
		login_url = users.create_login_url('/profile')
	
	template_values = {
		'login' : login_url,
		'logout' : logout_url,
		'user' : newUser,
		'shows' : shows
	}
	
	render_template(self, 'profile.html', template_values)
	
  def post(self):
	user = users.get_current_user()
    
	login_url = ''
	logout_url = ''
	newUser =''
	shows = []
	
	if user:
		logout_url = users.create_logout_url('/')
	
		user_query = User.query((User.user == user))
		oldUser = user_query.get()
		if oldUser:
			newUser = oldUser
			for userShow in oldUser.shows:
				userShows_query = TVShow.query(TVShow.id == userShow)
				shows.append(userShows_query.get())
		else:
			newUser = User()
			newUser.user = user
			newUser.put()
	else:
		login_url = users.create_login_url('/profile')
	
	template_values = {
		'login' : login_url,
		'logout' : logout_url,
		'user' : newUser,
		'shows' : shows
	}
	
	render_template(self, 'profile.html', template_values)
	
class OtherProfile(webapp2.RequestHandler):
  def get(self):
	self.redirect('/')
	
  def post(self):
	login_url = ''
	logout_url = ''
	otherUser =''
	shows = []
	user = users.get_current_user()
	
	if user:
		logout_url = users.create_logout_url('/')
		
		otherUserName = self.request.get('userSelect')
		user_query = User.query((User.name == otherUserName))
		otherUser = user_query.get()
		
		for userShow in otherUser.shows:
			userShows_query = TVShow.query(TVShow.id == userShow)
			shows.append(userShows_query.get())
	else:
		login_url = users.create_login_url('/profile')
	
	template_values = {
		'login' : login_url,
		'logout' : logout_url,
		'user' : otherUser,
		'shows' : shows
	}
	
	render_template(self, 'otherProfile.html', template_values)
	
class EpisodeView(webapp2.RequestHandler):
  def get(self):
	user = users.get_current_user()
    
	login_url = ''
	logout_url = ''
	name = ''
	episode =''
	up = []
	down = []
	comments = []
	show = ''
	
	if user:
		logout_url = users.create_logout_url('/')
		name = user.nickname()
	else:
		login_url = users.create_login_url('/profile')
	
	eptvid = self.request.get('episodeselectTVID')
	epnum = int(self.request.get('episodeselectEPNUM'))
	episode = Episode.query((Episode.tvid == eptvid),(Episode.epnumber == epnum)).get()

	if episode.commentids:
		for comID in episode.commentids:
			comment_query = Greeting.query(Greeting.id == comID).get()
			comments.append(comment_query)
	
		try:
			comments.sort(key=lambda x: x.rating, reverse=True)
		except AttributeError:
			comments = comments
			
		if user:				
			for comment in comments:
				try:
					if user in comment.upvoted:
						up.append(comment.id)
				except AttributeError:
					up = []
				try:
					if user in comment.downvoted:
						down.append(comment.id)
				except AttributeError:
					down = []
	
	show = TVShow.query(TVShow.id == episode.tvid).get()
	
	template_values = {
		'login' : login_url,
		'logout' : logout_url,
		'nickname' : name,
		'episode' : episode,
		'up' : up,
		'down' : down,
		'comments' : comments,
		'show' : show
	}
	
	render_template(self, 'episode.html', template_values)
  
  def post(self):
	user = users.get_current_user()
    
	login_url = ''
	logout_url = ''
	name = ''
	episode =''
	up = []
	down = []
	comments = []
	show = ''
	
	if user:
		logout_url = users.create_logout_url('/')
		name = user.nickname()
	else:
		login_url = users.create_login_url('/profile')
	
	eptvid = self.request.get('episodeselectTVID')
	epnum = int(self.request.get('episodeselectEPNUM'))
	episode = Episode.query((Episode.tvid == eptvid),(Episode.epnumber == epnum)).get()

	if episode.commentids:
		for comID in episode.commentids:
			comment_query = Greeting.query(Greeting.id == comID).get()
			comments.append(comment_query)
		
		try:
			comments.sort(key=lambda x: x.rating, reverse=True)
		except AttributeError:
			comments = comments
	
		if user:				
			for comment in comments:
				try:
					if user in comment.upvoted:
						up.append(comment.id)
				except AttributeError:
					up = []
				try:
					if user in comment.downvoted:
						down.append(comment.id)
				except AttributeError:
					down = []
	
	show = TVShow.query(TVShow.id == episode.tvid).get()
	
	template_values = {
		'login' : login_url,
		'logout' : logout_url,
		'nickname' : name,
		'episode' : episode,
		'up' : up,
		'down' : down,
		'comments' : comments,
		'show' : show
	}
	
	render_template(self, 'episode.html', template_values)
		
class ShowList(webapp2.RequestHandler):
  def get(self):
	user = users.get_current_user()
    
	login_url = ''
	logout_url = ''
	name = ''
	shows = ''
	
	if user:
		logout_url = users.create_logout_url('/')
		name = user.nickname()
	else:
		login_url = users.create_login_url('/profile')
	
	shows = TVShow.query(TVShow.name != None).fetch(20)
	
	template_values = {
		'login' : login_url,
		'logout' : logout_url,
		'nickname' : name,
		'shows' : shows
	}
	
	render_template(self, 'showlist.html', template_values)
	
  def post(self):
	user = users.get_current_user()
    
	login_url = ''
	logout_url = ''
	name = ''
	shows =''
	
	if user:
		logout_url = users.create_logout_url('/')
		name = user.nickname()
	else:
		login_url = users.create_login_url('/profile')
	
	shows = TVShow.query(TVShow.name != None).fetch(20)
	
	template_values = {
		'login' : login_url,
		'logout' : logout_url,
		'nickname' : name,
		'shows' : shows
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
		login_url = users.create_login_url('/profile')
	
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
  def get(self):
	self.redirect('/')
	
  def post(self):
	greeting = Greeting(parent=guestbook_key)

	if users.get_current_user():
		greeting.author = users.get_current_user()
	
	result = ndb.gql('SELECT * FROM Greeting')
	number = result.count()
	
	eptvid = self.request.get('episodeTVID')
	epnum_str = self.request.get('episodeEPNUM')
	epnum = int(epnum_str)
	episode_query = Episode.query((Episode.tvid == eptvid),(Episode.epnumber == epnum))
	episode = episode_query.get()
	
	episode.commentids.append(number)
	episode.put()
		
	greeting.id = number;
	greeting.content = self.request.get('content')
	greeting.rating = 0
	greeting.put()
	
	self.redirect('/episode?episodeselectTVID=' + eptvid + '&episodeselectEPNUM=' + epnum_str)

class Rate(webapp2.RequestHandler):
  def get(self):
	self.redirect('/')
	
  def post(self):
	eptvid = self.request.get('tvid')
	epnum = self.request.get('epnum')
	toVote = self.request.get('updown')
	comId = int(self.request.get('comId'))
	user = users.get_current_user()
	
	com_query = Greeting.query((Greeting.id == comId))
	com = com_query.get()
	
	if( toVote == "1"):
		if not user in com.upvoted:
			com.rating = com.rating + 1;
			if not user in com.downvoted:
				com.upvoted.append(user)
			else:
				com.downvoted.remove(user)
	else:
		if not user in com.downvoted:
			com.rating = com.rating - 1;
			if not user in com.upvoted:
				com.downvoted.append(user)
			else:
				com.upvoted.remove(user)
		
	com.put()
	self.redirect('/episode?episodeselectTVID=' + eptvid + '&episodeselectEPNUM=' + epnum)
	
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
	urlfetch.set_default_fetch_deadline(600)
	tvshow_query = TVShow.query((TVShow.name == None))
	shows = tvshow_query.fetch(limit=100)
	for show in shows:
		url = 'http://services.tvrage.com/feeds/full_show_info.php?sid=' + show.id
		request = urllib2.Request(url, headers={"Accept" : "application/xml"})
		u = urllib2.urlopen(request)
		tree = ElementTree.parse(u)
		rootElem = tree.getroot()
		
		try:
			show.imgsrc = rootElem.find('image').text
		except AttributeError:
			show.imgsrc = "/stylesheets/images/placeholder.png"
		try:
			show.genre = rootElem.find('classification').text
		except AttributeError:
			show.genre = "general"
		try:
			airtimeStr = rootElem.find('airtime').text
		except AttributeError:
			airtimeStr = "12:00"
		try:
			show.runtime = int(rootElem.find('runtime').text)
		except AttributeError:
			show.runtime = 30
		try:
			show.airtime = datetime.datetime.strptime(airtimeStr, "%H:%M")
		except ValueError:
			show.airtime = datetime.datetime.strptime("12:00", "%H:%M")
		
		show.rating = 0;
		
		episodes = rootElem.findall(".//episode")
		i = 0
		for episode in reversed(episodes):
			if (i == 200):
				break
			try:
				dateStr = episode.find('airdate').text
				try:
					checkDate = datetime.datetime.strptime(dateStr, "%Y-%m-%d")
				except ValueError:
					continue
				epi_query = Episode.query((Episode.tvid == show.id),(Episode.date == checkDate))
				epiResult = epi_query.get()
				if not epiResult:
					epi = Episode()
					try:
						epi.epnumber = int(episode.find('epnum').text)
					except AttributeError:
						epi.epnumber = 0
					epi.tvid = show.id
					epi.date = checkDate
					epi.rating = 0
					try:
						epi.title = episode.find('title').text
					except:
						epi.title = ''
					epi.put()
			except AttributeError:
				print "Delete TVShow with id=", show.id
			
			i = i + 1;
		show.name = rootElem.find('name').text
		show.put()
		u.close()

class Search(webapp2.RequestHandler):
  def get(self):
	self.redirect('/')
		
  def post(self):
	user = users.get_current_user()
    
	login_url = ''
	logout_url = ''
	name = ''
	show = ''
	user ='' 
	
	if user:
		logout_url = users.create_logout_url('/')
		name = user.nickname()
	else:
		login_url = users.create_login_url('/profile')
	
	search = self.request.get('searchbar')
	show_query = TVShow.query((TVShow.name == search))
	show = show_query.get()
	
	user_query = User.query((User.name == search))
	user = user_query.get()
	
	template_values = {
		'login' : login_url,
		'logout' : logout_url,
		'nickname' : name,
		'show' : show,
		'user' : user
	}
	
	render_template(self, 'searchResults.html', template_values)
	
class FixPng(webapp2.RequestHandler):	
  def get(self):
	shows = TVShow.query((TVShow.imgsrc == "placeholder.png")).fetch()
	if shows:
		for show in shows:
			show.imgsrc = "/stylesheets/images/placeholder.png"
			show.put()
	
class Track(webapp2.RequestHandler):
  def get(self):
	self.redirect('/')
	
  def post(self):
	trackShowID = self.request.get('trackShowID')
	user = users.get_current_user()
	
	user_query = User.query((User.user == user))
	trackUser = user_query.get()
	
	show_query = TVShow.query(TVShow.id == trackShowID)
	show = show_query.get()
	
	if not trackShowID in trackUser.shows:
		trackUser.shows.append(trackShowID)
		trackUser.put()
		if show.tracking:
			show.tracking = show.tracking + 1
		else:
			show.tracking = 1
		show.put()
		
	self.redirect('/show?showselect=' + trackShowID)

class setComID(webapp2.RequestHandler):
  def get(self):
	episodes = Episode.query(Episode.tvid == "30876")

	for episode in episodes:
		if ((0 in episode.commentids) and (episode.epnumber != 19)):
			episode.commentids.remove(0)
			episode.put()
	
class setUserInfo(webapp2.RequestHandler):
  def post(self):
	name = self.request.get('firstname')
	bio = self.request.get('bio')
	gender = self.request.get('chosenGender')
	age = int(self.request.get('age'))
	user = users.get_current_user()

	user_query = User.query((User.user == user))
	oldUser = user_query.get()
	oldUser.name = name
	oldUser.bio = bio
	oldUser.age = age
	oldUser.gender = gender
	oldUser.put()
	
	self.redirect('/profile')

class RateShow(webapp2.RequestHandler):
  def get(self):
	self.redirect('/')
	
  def post(self):
	rating = int(self.request.get('rateShow'))
	showID = self.request.get('showID')
	show_query = TVShow.query((TVShow.id == showID))
	show = show_query.get()
	if (rating == 1):
		show.rating = show.rating + 1;
	else:
		show.rating = show.rating - 1;
		
	show.put()
	self.redirect('/show?showselect=' + showID)
	
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
  ('/searchShow', SearchShow),
  ('/search', Search),
  ('/fixPNG', FixPng),
  ('/track', Track),
  ('/setcom', setComID),
  ('/otherUser', OtherProfile),
  ('/setUserInfo', setUserInfo),
  ('/rateShow', RateShow)
], debug=True)