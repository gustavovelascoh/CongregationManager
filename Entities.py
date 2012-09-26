from google.appengine.ext import db

class Publisher(db.Model):
	
	username = db.StringProperty(required = True)
	password = db.StringProperty(required = True)
	name = db.StringProperty(required = True)
	lastname = db.StringProperty(required = True)
	email = db.EmailProperty()
	
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
	
