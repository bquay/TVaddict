import webapp2
import os
from google.appengine.ext import ndb
from google.appengine.api import users
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler


def render_template(handler, templatename, templatevalues):
    path = os.path.join(os.path.dirname(__file__), templatename)
    html = template.render(path, templatevalues)
    handler.response.out.write(html)
	
class Poster(ndb.Model):
  number = ndb.StringProperty()
  count = ndb.IntegerProperty()
  
class Vote(ndb.Model):
  id = ndb.StringProperty()
  posterNumber = ndb.StringProperty()

class StartStop(ndb.Model):
  startstop = ndb.BooleanProperty()
  
class MainPage(webapp2.RequestHandler):
  def get(self):
	template_values = {
	}
	
	render_template(self, 'index.html', template_values)
	
  def post(self):
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
	
	template_values = {
		'posters' : posters
	}
	
	render_template(self, 'results.html', template_values)
	
  def post(self):
	posters = ndb.gql('SELECT * FROM Poster ORDER BY count DESC LIMIT 10')
	
	template_values = {
		'posters' : posters
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
	
  def post(self):
	ss_query = StartStop.query()
	ssResult = ss_query.get()
	if not ssResult:
		ss = StartStop()
		ss.startstop = False
		ss.put()
	else:
		ssResult.startstop = False
		ssResult.put()
	
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
	
  def post(self):
	ss_query = StartStop.query()
	ssResult = ss_query.get()
	if not ssResult:
		ss = StartStop()
		ss.startstop = True
		ss.put()
	else:
		ssResult.startstop = True
		ssResult.put()
	
app = webapp2.WSGIApplication([
  ('/', MainPage),
  ('/results', Results),
  ('/stopVoting', StopVoting),
  ('/startVoting',StartVoting),
  ReceiveMail.mapping(),
], debug=True)