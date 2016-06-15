import urllib2
import logging

from parser import Parser


class Scraper:
  BASE_URL = "http://www.sportsbet.com.au/betting/politics/australian-federal-politics/outrights?&ev_oc_grp_id="
  IDS = ["1971028", "1971052", "1956097", "1971071", "1971079", "1971095", "1971122", "1971123"]

  def scrape_all(self):
    seats = []
    for id in Scraper.IDS:
      url = Scraper.BASE_URL + id
      seats.extend(self.scrape(url))

    return seats


  def scrape(self, url):
    try:
      result = urllib2.urlopen(url)
    except:
      logging.error("Could not fetch URL");

    parser = Parser()
    content = False
    for line in result:
      if not content and 'content-panel-sport' in line:
        content = True
      if content:
        parser.feed(line)

    return parser.seats

if __name__ == "__main__":
  scraper = Scraper()
  seats = scraper.scrape_all()
  print "Done"
