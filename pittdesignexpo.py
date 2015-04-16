import webapp2
import os
import collections
import datetime
from google.appengine.ext import ndb
from google.appengine.api import users
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler


def render_template(handler, templatename, templatevalues):
    path = os.path.join(os.path.dirname(__file__), templatename)
    html = template.render(path, templatevalues)
    handler.response.out.write(html)

class TopThree(ndb.Model):
  one = ndb.StringProperty()
  two = ndb.StringProperty()
  three = ndb.StringProperty()
  onecount = ndb.IntegerProperty()
  twocount = ndb.IntegerProperty()
  threecount = ndb.IntegerProperty()
	
class Poster(ndb.Model):
  number = ndb.StringProperty()
  count = ndb.IntegerProperty()
  tags = ndb.StringProperty(repeated=True)
  
class Vote(ndb.Model):
  id = ndb.StringProperty()
  posterNumber = ndb.StringProperty()
  time = ndb.DateTimeProperty()

class StartStop(ndb.Model):
  startstop = ndb.BooleanProperty()
  
class MainPage(webapp2.RequestHandler):
  def get(self):
	template_values = {
	}
	
	render_template(self, 'index.html', template_values)

class ReceiveMail(InboundMailHandler):
  def receive(self, message):
	ss_query = StartStop.query()
	ssResult = ss_query.get()
	if ssResult.startstop == True:
		_id = message.sender
		_pn = message.subject
		
		vote_query = Vote.query(Vote.id == _id)
		voteResult = vote_query.get()
		if not voteResult:
			vote = Vote()
			vote.id = _id
			vote.posterNumber = _pn
			vote.time = datetime.datetime.now()
			vote.put()
			
			poster_query = Poster.query(Poster.number == _pn)
			posterResult = poster_query.get()
			if not posterResult:
				poster = Poster()
				poster.number = _pn
				poster.count = 1
				poster.put()
			else:
				posterResult.count = posterResult.count + 1
				posterResult.put()
	else:
		print("Got into receive mail")
		
class Results(webapp2.RequestHandler):
  def get(self):
	posters = ndb.gql('SELECT * FROM Poster ORDER BY count DESC LIMIT 10')
	trends = ndb.gql('SELECT * FROM TopThree').get()
	
	template_values = {
		'posters' : posters,
		'trends' : trends
	}
	
	render_template(self, 'results.html', template_values)
	
class StopVoting(webapp2.RequestHandler):
  def get(self):
	ss_query = StartStop.query()
	ssResult = ss_query.get()
	if not ssResult:
		ss = StartStop()
		ss.startstop = False
		ss.put()
	else:
		ssResult.startstop = False
		ssResult.put()
		
	template_values = {
		"stopVote" : True,
	}
	
	render_template(self, 'stopVote.html', template_values)
	
class StartVoting(webapp2.RequestHandler):
  def get(self):
	ss_query = StartStop.query()
	ssResult = ss_query.get()
	if not ssResult:
		ss = StartStop()
		ss.startstop = True
		ss.put()
	else:
		ssResult.startstop = True
		ssResult.put()
		
	template_values = {
		"startVote" : True,
	}
	
	render_template(self, 'startVote.html', template_values)

class ClearDB(webapp2.RequestHandler):
  def get(self):
	posters = ndb.gql('SELECT * FROM Poster')
	votes = ndb.gql('SELECT * FROM Vote')
	topthree = ndb.gql('SELECT * FROM TopThree')
	for p in posters:
		p.key.delete()
	for v in votes:
		v.key.delete()
	for t in topthree:
		t.key.delete()
		
	template_values = {
		"clearDB" : True,
	}
	
	render_template(self, 'clearDB.html', template_values)

class AddPosters(webapp2.RequestHandler):		
  def get(self):
	poster1 = Poster()
	poster1.number = "1"
	poster1.count = 0
	poster1.tags.append("robots")
	poster1.tags.append("cs")
	poster1.tags.append("radio")
	poster1.put()
	
	poster1 = Poster()
	poster1.number = "2"
	poster1.count = 0
	poster1.tags.append("robots")
	poster1.tags.append("medical")
	poster1.tags.append("nano")
	poster1.put()
	
	poster1 = Poster()
	poster1.number = "3"
	poster1.count = 0
	poster1.tags.append("human")
	poster1.tags.append("engineering")
	poster1.tags.append("software")
	poster1.put()
	
	poster1 = Poster()
	poster1.number = "4"
	poster1.count = 0
	poster1.tags.append("robots")
	poster1.tags.append("cs")
	poster1.tags.append("software")
	poster1.put()
  
class GetTrends(webapp2.RequestHandler):
  def get(self):
	currTime = datetime.datetime.now()
	threeHours = currTime - datetime.timedelta(hours=3)
	recVotes = ndb.gql('SELECT * FROM Vote WHERE time >= :1',threeHours)
	
	recPost = []
	for vote in recVotes:
		recPost.append(Poster.query(Poster.number == vote.posterNumber).get())
		
	tags = []
	for rp in recPost:
		for tag in rp.tags:
			tags.append(tag)
	
	topThree = collections.Counter(tags).most_common(3)
	three = []
	cthree = []
	for top in topThree:
		three.append(top[0])
		cthree.append(top[1])
		
	tT_query = TopThree.query()
	tTResult = tT_query.get()
	if not tTResult:
		if three:
			tT = TopThree()
			tT.one = three[0]
			tT.two = three[1]
			tT.three = three[2]
			tT.onecount = cthree[0]
			tT.twocount = cthree[1]
			tT.threecount = cthree[2]
			tT.put()
	else:
		if three:
			tTResult.one = three[0]
			tTResult.two = three[1]
			tTResult.three = three[2]
			tTResult.onecount = cthree[0]
			tTResult.twocount = cthree[1]
			tTResult.threecount = cthree[2]
			tTResult.put()
	
app = webapp2.WSGIApplication([
  ('/', MainPage),
  ('/results', Results),
  ('/stopVoting', StopVoting),
  ('/startVoting',StartVoting),
  ('/getTrends', GetTrends),
  ('/clearDB', ClearDB),
  ('/addPosters', AddPosters),
  ReceiveMail.mapping(),
], debug=True)