#!/usr/bin/env python

import os
import re
from datetime import *
from Entities import *
from string import *

import webapp2
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

def render_str(template, **params):
	t = jinja_env.get_template(template)
	return t.render(params)

class BaseHandler(webapp2.RequestHandler):
	def render_str(self, template, **params):
		return render_str(template, **params)

	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)
	
	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

def render_post(response, post):
	response.out.write('<b>' + post.subject + '</b><br>')
	response.out.write(post.content)
		
class Index(BaseHandler):
	def get(self):
		error = self.request.get('error')
		self.render("index.html")
	
	def post(self):
		username = self.request.get('username')
		password = self.request.get('password')
		error = self.request.get('error')
		if not error:
			if username and password:
				pub = db.GqlQuery("SELECT * FROM Publisher WHERE username = '%s'" % username)			
				
				#	print pub,'\n'
				if pub.count() == 0:
					self.render("index.html",error = 'No existe el usuario')
				
				elif pub[0].password != password:
					self.render("index.html",error = 'Error en el password')
				else:
					self.render('welcome.html', name = pub[0].name, lastname = pub[0].lastname)
			else:
				self.render("index.html", error = 'Datos incompletos', username = username)
		else:
			self.render("index.html", error = error, username = username)

class newUser(BaseHandler):
	def get(self):
		name = self.request.get('nombre')
		self.render("newUser.html")
	
	def post(self):
		name = self.request.get('name')
		lastname = self.request.get('lastname')
		username = self.request.get('username')
		password = self.request.get('password')
		
		params = dict(username = username,
                      name = name,
                      lastname = lastname)

		if name and lastname and username and password:
			pub = Publisher(username = username,
							name = name,
							lastname = lastname,
							password = password)
			pub.put();
			params['success'] = "Se ha creado un nuevo usuario"
			self.render('newUser.html',**params)

		else:
			params['error'] = "Datos incompletos"
			self.render('newUser.html', **params)

class listPub(BaseHandler):
	def get(self):
		#pubs = db.GqlQuery("SELECT * FROM Publisher")
		pubs = Publisher.all();
		#reps = Report.all();

		self.render('list.html',pubs = pubs)#, reps = reps)#, pk = pk)
	
	def post(self):
		id = int(self.request.get('id'))
		
		if id:
			k = db.Key.from_path('Publisher',id)
			#print 'myKey = %s', k			
			pubs = Publisher.all()
			pubs.filter('__key__ =', k)
						
			#print 'count = ',pubs.count(),
			
			if pubs.count() > 0:
				reps = pubs[0].report_set
				rep_len = reps.count()			
				#print 'len = ',rep_len
				ret = '%s;' % (rep_len)
			else:
				ret = '0;'
			if rep_len > 0:
				for r in reps:
					ret += "%s;%s;%s;%02d:%02d;%s;%s;%s;" % (r.date,r.books,r.brochures,r.hours, r.minutes,r.magazines,r.revisits,r.studies)
			
			self.write(ret);			
		else:
			self.write('no ID');
			
			
		

class newReport(BaseHandler):
	def get(self):
		pubs = Publisher.all();
		name = self.request.get('name')
		error = self.request.get('error')
		
		if error:			
			self.render("newReport.html", error = error)
		else:
			success = self.request.get('success')
			if success:				
				self.render("newReport.html", success = success)
			else:				
				self.render("newReport.html", pubs = pubs)
	
	def post(self):
		publisher = int(self.request.get('pu'))
		dateR = self.request.get('date')
		hours = self.request.get('ho')
		minutes = self.request.get('mi')
		books = self.request.get('bo')
		brochures = self.request.get('br')
		magazines = self.request.get('ma')
		revisits = self.request.get('re')
		studies = self.request.get('st')
		
		#print "hola"
		#print datetime.today(),'||', publisher,'||',date,'||',int(hours),'||',int(minutes),'||',int(books),'||',int(brochures),'||',int(magazines),'||',int(revisits),'||',int(studies)
		
		if publisher and dateR and hours:
			
			k = db.Key.from_path('Publisher',publisher)
			dateR = dateR.split('-')

			rep = Report(timestamp = datetime.today(),
						publisher = k,
						date = date(int(dateR[0]),int(dateR[1]),int(dateR[2])),#fix
						hours = int(hours),
						minutes = int(minutes),
						books = int(books),
						brochures = int(brochures),
						magazines = int(magazines),
						revisits = int(revisits),
						studies = int(studies))
			rep.put()

			self.write('success')
		else:
			#error = "Datos incompletos"
			#self.render('newReport.html', error = error)
			self.write('error')
			#self.redirect('/')
class newCong(BaseHandler):
	def get(self):
		
		c_name = self.request.get('c_name')
		
		if c_name:
			dupl = Congregation.by_name(c_name)
			
			if dupl:
				success = 'Existe ...'
			else:
				success = 'NO Existe ...'
			#cong = Congregation.create(c_name)			
			#cong.put()				
			
			success += "Se ha creado la congregacion %s" % c_name
			self.render("newCong.html", success = success)
		else:				
			self.render("newCong.html")
		
	def post(self):
		pass
			
app = webapp2.WSGIApplication([('/', Index),
							  ('/newUser', newUser),
							  ('/list',listPub),
							  ('/newReport',newReport),
							  ('/newCong',newCong),
							  #('/newGroup',newGroup),
							  #('/welcome',welcome),
							  ], debug=True)
