class Candidate:
  def __init__(self, name, price):
    self.name = name
    self.price = price

class Seat:
  def __init__(self, name, state):
    self.name = name
    self.state = state
    self.candidates = []

  def add_candidate(self, name, price):
    self.candidates.append(Candidate(name, price))

