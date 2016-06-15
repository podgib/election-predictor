import logging
import webapp2
from google.appengine.ext import ndb
from scraper.scraper import Scraper
from models.seat import Seat
from models.party import Party
from models.price import Price
from models import party

class ScrapeRunner(webapp2.RequestHandler):
  def get(self):
    self.post()

  def post(self):
    logging.info("Running scrape handler")
    scraper = Scraper()
    scrape_result = scraper.scrape_all()

    seats = []
    parties = []
    prices = []
    winners = {}
    for s in scrape_result:
      if s.name not in seats:
        seats.append(Seat(name=s.name, state=s.state, id=s.name))
        seats[-1].put()

      lowest_price = 1000
      winner = ''
      for c in s.candidates:
        if c.name not in parties:
          parties.append(Party(name=c.name, id=c.name))
        party_key = ndb.Key(Party, c.name)
        seat_key = ndb.Key(Seat, s.name)
        price = Price(party=party_key, seat=seat_key, price=c.price)
        price.put()

        if c.price < lowest_price:
          lowest_price = c.price
          winner = c.name

      if winner in winners:
        winners[winner] += 1
      else:
        winners[winner] = 1

    for party in parties:
      if party.name in winners:
        party.num_seats = winners[party.name]
      else:
        party.num_seats = 0
      party.put()
    self.response.out.write(winners)

app = webapp2.WSGIApplication([
  ('/worker/scrape', ScrapeRunner)
], debug=True)
