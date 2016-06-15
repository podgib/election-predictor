from google.appengine.ext import ndb

class Seat(ndb.Model):
  name = ndb.StringProperty()
  state = ndb.StringProperty()
