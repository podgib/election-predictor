from google.appengine.ext import ndb
from party import Party
from seat import Seat


class Price(ndb.Model):
  party = ndb.KeyProperty(kind=Party)
  seat = ndb.KeyProperty(kind=Seat)
  date = ndb.DateProperty(auto_now_add=True)
  price = ndb.FloatProperty(required=True)