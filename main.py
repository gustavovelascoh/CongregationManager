import os
#import re
from datetime import date,datetime
from src.Entities import *
#from Entities import *
from string import *

import webapp2
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

def render_str(template, **params):
	t = jinja_env.get_template(template)
	return t.render(params)

class LoginHandler(webapp2.RequestHandler):

	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)
	
	def render_str(self, template, **params):
		params['user'] = self.user
		return render_str(template, **params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))
		
	def set_secure_cookie(self, name, val):
		cookie_val = secure.make_secure_val(val)
		self.response.headers.add_header(
            'Set-Cookie',
            '%s=%s; Path=/' % (name, cookie_val))

	def read_secure_cookie(self, name):
		cookie_val = self.request.cookies.get(name)
		return cookie_val and secure.check_secure_val(cookie_val)

	def login(self, user):
		self.set_secure_cookie('user_id', str(user.key().id()))

	def logout(self):
		self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')
	
	def initialize(self, *a, **kw):
		webapp2.RequestHandler.initialize(self, *a, **kw)
		uid = self.read_secure_cookie('user_id')
		self.user = uid and Publisher.by_id(int(uid))

class BaseHandler(webapp2.RequestHandler):
	def render_str(self, template, **params):
		return render_str(template, **params)

	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)
	
	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))
	
	def set_secure_cookie(self, name, val):
		cookie_val = secure.make_secure_val(val)
		self.response.headers.add_header(
            'Set-Cookie',
            '%s=%s; Path=/' % (name, cookie_val))
	
	def read_secure_cookie(self, name):
		cookie_val = self.request.cookies.get(name)
		return cookie_val and secure.check_secure_val(cookie_val)

	def login(self, user):
		self.set_secure_cookie('user_id', str(user.key().id()))

	def logout(self):
		self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

	def initialize(self, *a, **kw):
		webapp2.RequestHandler.initialize(self, *a, **kw)
		uid = self.read_secure_cookie('user_id')
		self.user = uid and User.by_id(int(uid))

def render_post(response, post):
	response.out.write('<b>' + post.subject + '</b><br>')
	response.out.write(post.content)
	
class Home(LoginHandler):
	def get(self):
		self.user = self.read_secure_cookie('user_id')
		error = self.request.get('error')
		if self.user is None:			
			self.render("base_5.html", error = error)
		else:
			#welcome to your dashboard
			pass

class New(LoginHandler):
	def get(self):
		self.user = self.read_secure_cookie('user_id')
		item = self.request.get('item')
		if self.user is None:
			if item is None:
				self.render("base_5.html",logged = 0)
			else:
				self.render("edit.html",item = item)				
		else:
			if item is None:
				self.redirect('/home'+'?error=user'+ item)
			else:
				self.render("edit.html",item = item)
	def post(self):
		pass
	
class Signin(LoginHandler):
	def post(self):
		username = self.request.get('name')
		pw = self.request.get('pw')
		item = self.request.get('item')
		
		if username and pw:			
			pub = Publisher.by_name(username.lower())
			
			if pub:
				error = 'Existe un usuario con este nombre'
				self.render("edit.html",item = item, error = error)
			else:
				pub = Publisher.register(username, pw)				
				pub.put()
				
				self.render("edit.html",item = item, error = 'todo bien')
		else:
			self.render("edit.html",item = item, error = 'sdfasdf')
			
				
class Index(BaseHandler):
	def get(self):
		error = self.request.get('error')
		login = 0
		self.render("index.html",login = login, error = error)
	
	def post(self):
		username = self.request.get('username')
		password = self.request.get('pass')
		error = self.request.get('error')
		if not error:
			if username and password:
				pub = Publisher.login(username,password)		
				
				if pub == -1:
					self.render("index.html",error = 'Error en el password')
				elif pub == -2:
					self.render("index.html",error = 'Error en el username')
				else:
					self.login(pub)
					self.render('welcome.html', name = pub.name, lastname = pub.lastname)
			else:
				self.render("index.html", error = 'Datos incompletos', username = username)
		else:
			self.render("index.html", error = error, username = username)

class newUser(BaseHandler):
	def get(self):
		name = self.request.get('nombre')
		congs = Congregation.all()
		self.render("newUser.html",congs = congs)
	
	def post(self):
		self.name = self.request.get('name')
		self.lastname = self.request.get('lastname')
		self.username = self.request.get('username')
		self.password = self.request.get('password')
		self.email = self.request.get('email')
		self.congregation = int(self.request.get('congregation'))
		self.group = self.request.get('group')
				
		params = dict(username = self.username,
                      name = self.name,
                      lastname = self.lastname,
                      email = self.email,
                      group = self.group,
                      congregation = self.congregation)
		

		if self.name and self.lastname and self.username and self.password and self.congregation>0:
			pub = Publisher.register(self.username, self.name, self.lastname, self.password,self.congregation,self.email,self.group)
			if pub:
				pub.put();
				params['success'] = "Se ha creado un nuevo usuario"
				self.render('newUser.html',**params)
			else:
				params['error'] = "Datos incompletos"
				self.render('newUser.html', **params)

		else:
			params['error'] = "Datos incompletos"
			self.render('newUser.html', **params)

class list(BaseHandler):
	def get(self):
		#pubs = db.GqlQuery("SELECT * FROM Publisher")
		pubs = Publisher.all();
		#reps = Report.all();

		self.render('list.html',pubs = pubs)#, reps = reps)#, pk = pk)
	
	def post(self):
		id = int(self.request.get('id'))
		month = self.request.get('month')
		year = self.request.get('year')
		
		if id:
			k = db.Key.from_path('Publisher',id)
			#print 'myKey = %s', k			
			pubs = Publisher.all()
			pubs.filter('__key__ =', k)
			
			if pubs.count() > 0:
				reps = pubs[0].report_set
				
				if year and month:
					month = int(month)
					year = int(year)
					min = date(year, month, 1)
					if month != 12:
						max = date(year, month+1, 1)
					else:
						max = date(year+1, 1, 1)
					
					reps.filter('date >= ',min)	
					reps.filter('date < ',max)
								
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
		c_city = self.request.get('c_city')
		
		if c_name:
			dupl = Congregation.by_name(c_name)
			
			if dupl:
				success = 'Existe ...'
			else:
				success = 'NO Existe ...'
			
				cong = Congregation.create(c_name, c_city)			
				cong.put()				
			
				success += "Se ha creado la congregacion %s" % c_name
				self.render("newCong.html", success = success)
				return
		else:				
			self.render("newCong.html")
		
	def post(self):
		pass
			
app = webapp2.WSGIApplication([('/', Index),
								('/home', Home),
								('/new', New),
								('/signin', Signin),
							  ('/newUser', newUser),
							  ('/list',list),
							  ('/newReport',newReport),
							  ('/newCong',newCong),
							  #('/newGroup',newGroup),
							  #('/welcome',welcome),
							  ], debug=True)
