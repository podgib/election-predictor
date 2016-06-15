from google.appengine.ext import ndb

class Party(ndb.Model):
  name = ndb.StringProperty()
  num_seats = ndb.IntegerProperty(default=0)