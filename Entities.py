from google.appengine.ext import db
from secure import *

class Congregation(db.Model):
	name = db.StringProperty(required = True)
	city = db.StringProperty(required = True)
	
	@classmethod
	def create(cls,name,city):
		return Congregation(name = name,city = city)
	@classmethod
	def by_name(cls, name):
		c = Congregation.all().filter('name =', name).get()
		return c
	
class Group(db.Model):
	captainID = db.IntegerProperty(required = True)
	assistantID = db.IntegerProperty(required = True)
	congregation = db.ReferenceProperty(Congregation,required = True)

class Publisher(db.Model):
	
	username = db.StringProperty(required = True)
	password = db.StringProperty(required = True)
	name = db.StringProperty(required = True)
	lastname = db.StringProperty(required = True)
	email = db.EmailProperty()
	group = db.ReferenceProperty(Group)
	congregation = db.ReferenceProperty(Congregation,required = True)	
	
	@classmethod
	def by_id(cls, uid):
		return Publisher.get_by_id(uid)

	@classmethod
	def by_name(cls, name):
		u = Publisher.all().filter('username =', name).get()
		return u
	@classmethod
	def register(cls, username, name, lastname, password, congregation, email=None, group=None):
		
		k = db.Key.from_path('Congregation',congregation)
		
		pw_hash = make_pw_hash(name, password)
		p =  Publisher(username = username,
						name = name,
						lastname = lastname,
						password = pw_hash,
						congregation = k)
		if email:
			p.email = email
		if group:
			p.group = group
		
		return p
	
	@classmethod
	def login(cls, name, pw):
		u = cls.by_name(name)
		if u:
			if valid_pw(u.name, pw, u.password):
				return u
			else:
				return -1
		else:
			return -2
		

class Report(db.Model):
	timestamp = db.DateTimeProperty(required = True)
	publisher = db.ReferenceProperty(Publisher)
	date = db.DateProperty(required = True)
	hours = db.IntegerProperty(required = True)
	minutes = db.IntegerProperty(required = True)
	books = db.IntegerProperty()
	brochures = db.IntegerProperty()
	magazines = db.IntegerProperty()
	revisits = db.IntegerProperty()
	studies = db.IntegerProperty()
	
class FinalReport(db.Model):
	publisher = db.ReferenceProperty(Publisher)
	year = db.StringProperty(required = True)
	month = db.StringProperty(required = True)
	hours = db.IntegerProperty(required = True)
	minutes = db.IntegerProperty(required = True)
	books = db.IntegerProperty()
	brochures = db.IntegerProperty()
	magazines = db.IntegerProperty()
	revisits = db.IntegerProperty()
	studies = db.IntegerProperty()
	remain_h = db.IntegerProperty(required = True)
	minutes = db.IntegerProperty(required = True)
	
class Schedule(db.Model):
	day = db.StringProperty(required = True)
	init = db.StringProperty(required = True)
	finish = db.StringProperty()
	
class Student(db.Model):
	name = db.StringProperty(required = True)
	lastname = db.StringProperty(required = True)
	schedule = db.StringListProperty()
	
	
	
	
