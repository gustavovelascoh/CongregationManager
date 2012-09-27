from google.appengine.ext import db

class Congregation(db.Model):
	name = db.StringProperty(required = True)
	
	@classmethod
	def create(cls,name):
		return Congregation(name = name)
	@classmethod
	def by_name(cls, name):
		c = Congregation.all().filter('name =', name).get()
		return c
	
class Group(db.Model):
	captain = db.StringProperty(required = True)
	assistant = db.StringProperty(required = True)
	congregation = db.ReferenceProperty(Congregation,required = True)

class Publisher(db.Model):
	
	username = db.StringProperty(required = True)
	password = db.StringProperty(required = True)
	name = db.StringProperty(required = True)
	lastname = db.StringProperty(required = True)
	email = db.EmailProperty()
	group = db.ReferenceProperty(Group)	
	
	# @classmethod
    # def by_id(cls, uid):
		# return Publisher.get_by_id(uid, parent = users_key())

    # @classmethod
    # def by_name(cls, name):
		# u = Publisher.all().filter('username =', name).get()
		# return u

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
	
	
	
	
