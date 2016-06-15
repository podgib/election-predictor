from HTMLParser import HTMLParser
from seat import Seat, Candidate
from synonyms import SYNONYMS

import re

class State:
  START = 0
  LIST = 1
  SEAT = 2
  SEAT_HEADER = 3
  NAME = 4
  CANDIDATE = 5
  CANDIDATE_NAME = 6
  PRICE = 7


class Parser(HTMLParser):
  def __init__(self):
    HTMLParser.__init__(self)
    self.state = State.START
    self.seats = []
    self.candidate_name = None
    self.price = None

  def find_attr(self, attrs, name):
    for attr in attrs:
      if attr[0] == name:
        return attr[1]
    return None

  def handle_starttag(self, tag, attrs):
    if tag == 'ul':
      clazz = self.find_attr(attrs, 'class')
      if self.state == State.START and clazz == 'accordion-main':
        self.state = State.LIST
    elif tag == 'li':
      if self.state == State.LIST:
        self.state = State.SEAT
    elif tag == 'div':
      clazz = self.find_attr(attrs, 'class')
      if clazz == 'event-selection':
        if self.state == State.SEAT:
          self.state = State.SEAT_HEADER
    elif tag == 'a':
      clazz = self.find_attr(attrs, 'class')
      if self.state == State.SEAT_HEADER:
        self.state = State.NAME
      elif self.state == State.SEAT:
        if clazz and 'price' in clazz:
          self.state = State.CANDIDATE
    elif tag == 'span':
      clazz = self.find_attr(attrs, 'class')
      if self.state == State.CANDIDATE:
        if not clazz:
          pass
        elif 'team-name' in clazz:
          self.state = State.CANDIDATE_NAME
        elif 'price-val' in clazz:
          self.state = State.PRICE

  def handle_endtag(self, tag):
    if tag == 'li':
      if self.state == State.SEAT:
        self.state = State.LIST
    elif tag == 'div':
      if self.state == State.SEAT_HEADER:
        self.state = State.SEAT
    elif tag == 'a':
      if self.state == State.NAME:
        self.state = State.SEAT
      elif self.state == State.CANDIDATE:
        self.state = State.SEAT
        self.seats[-1].add_candidate(self.candidate_name, self.price)
    elif tag == 'span':
      if self.state == State.CANDIDATE_NAME or self.state == State.PRICE:
        self.state = State.CANDIDATE

  def handle_data(self, data):
    if len(data.strip()) == 0:
      return
    if self.state == State.NAME:
      # Seats are listed as eg. 'Higgins (VIC)'
      p = re.compile('([a-zA-Z\-\s\']*)\s*\(([A-Za-z]*)\)')
      m = p.match(data.strip())
      self.seats.append(Seat(m.group(1).strip(), m.group(2).upper()))
    if self.state == State.CANDIDATE_NAME:
      name = data
      if name.find('(') > 0:
        name = name[0:name.find('(')]
      name = name.strip()
      for s in SYNONYMS:
        if name in s:
          name = s[0]
      self.candidate_name = name
    if self.state == State.PRICE:
      self.price = float(data.strip())
