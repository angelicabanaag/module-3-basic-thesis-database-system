import webapp2
from google.appengine.ext import ndb
import jinja2
import os
import logging
import json



JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class Thesis(ndb.Model):
	year = ndb.IntegerProperty()
	thesis_title = ndb.StringProperty(indexed = True)
	abstract = ndb.StringProperty(indexed = True)
	adviser = ndb.StringProperty(indexed = True)
	section = ndb.IntegerProperty() 
	date = ndb.DateTimeProperty(auto_now_add=True)



class MainPageHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render())
    def post(self):
    	thesis = Thesis()
    	thesis.year = self.request.get('year')
    	thesis.thesis_title = self.request.get('thesis_title')
    	thesis.abstract = self.request.get('abstract')
    	thesis.adviser = self.request.get('adviser')
    	thesis.section = self.request.get('section')
    	thesis.put()
    	self.redirect('/success')


class APIThesisHandler(webapp2.RequestHandler):
    def get(self):
        thesises = Thesis.query().order(-Thesis.date).fetch()
        thesis_list = []
        for thesis in thesises:
            thesis_list.append({
                'id': thesis.key.urlsafe(),
                'year': thesis.year,
                'thesis_title': thesis.thesis_title,
                'abstract': thesis.abstract,
                'adviser': thesis.adviser,
                'section': thesis.section
                })
        response = {
            'result': 'OK',
            'data': thesis_list
            }
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(response))

    def post(self):
        thesis = Thesis()
        thesis.year = int(self.request.get('year'))
        thesis.thesis_title = self.request.get('thesis_title')
        thesis.abstract = self.request.get('abstract')
        thesis.adviser = self.request.get('adviser')
        thesis.section = int(self.request.get('section'))
        thesis.put()
        self.response.headers['Content-Type'] = 'application/json'
        response = {
            'result': 'OK',
            'data': {
                'id': thesis.key.urlsafe(),
                'year': thesis.year,
                'thesis_title': thesis.thesis_title,
                'abstract': thesis.abstract,
                'adviser': thesis.adviser,
                'section': thesis.section
            }
        }
        self.response.out.write(json.dumps(response));


class Success(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		self.response.write('Success!')



app = webapp2.WSGIApplication([
	('/api/thesis',APIThesisHandler),
    ('/home', MainPageHandler),
    ('/', MainPageHandler),
    ('/success', Success)
   
], debug=True)