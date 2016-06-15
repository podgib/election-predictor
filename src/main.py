import webapp2
import jinja2
import os
from models.party import Party

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class SummaryHandler(webapp2.RequestHandler):
  def get(self):
    parties = Party.query(Party.num_seats > 0).order(-Party.num_seats).fetch(150)
    template = jinja_environment.get_template('templates/summary.html')
    self.response.out.write(template.render({'parties':parties}))


app = webapp2.WSGIApplication([
    ('/', SummaryHandler)
], debug=True)
