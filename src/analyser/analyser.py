from src.scraper.scraper import Scraper

class Analyser:
  def __init__(self, seats):
    self.seats = seats

  def predict(self):
    parties = {}
    seats = {}
    probabilistic_seats = {}
    for seat in self.seats:
      winner = ''
      lowest_odds = 1000
      sum_p = 0
      for c in seat.candidates:
        sum_p = sum_p + 1 / c.price
        if c.price < lowest_odds:
          winner = c.name
          lowest_odds = c.price

      if winner in parties:
        parties[winner] = parties[winner] + 1
        seats[winner].append(seat.name)
      else:
        parties[winner] = 1
        seats[winner] = [seat.name]

      for c in seat.candidates:
        name = c.name
        if name.find('(') > 0:
          name = name[0:name.find('(')]
        name = name.strip()

        if name in probabilistic_seats:
          probabilistic_seats[name] = probabilistic_seats[name] + 1 / (c.price * sum_p)
        else:
          probabilistic_seats[name] = 1 / (c.price * sum_p)

    print parties
    print probabilistic_seats
    print seats

if __name__ == "__main__":
  scraper = Scraper()
  seats = scraper.scrape_all()
  analyser = Analyser(seats)
  analyser.predict()