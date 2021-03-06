from google.appengine.ext import db
import secure 

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
	name = db.StringProperty()
	lastname = db.StringProperty()
	email = db.EmailProperty()
	
	@classmethod
	def by_id(cls, uid):
		return Publisher.get_by_id(uid)
	
	@classmethod
	def by_username(cls, username):
		u = Publisher.all().filter('username =', username.lower()).get()
		return u
	
	@classmethod
	def register(cls, username, password):
						
		pw_hash = secure.make_pw_hash(username.lower(), password)
		p =  Publisher(username = username.lower(),
						password = pw_hash)		
		return p
	
	@classmethod
	def login(cls, username, pw):
		u = cls.by_username(username)
		if u:
			if secure.valid_pw(u.username, pw, u.password):
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
	
	
	
	
