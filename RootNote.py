


class RootNote:
  def __init__(self, draft,setup,play):
    self.draft = draft
    self.setup = setup
    self.play = play

class Draft:
  def __init__(self, draft_pool, board, deck, faction_choices_turn_order):
    self.draft_pool = draft_pool

class Win:
  def __init__(self,winner, results):
    self.winner = winner
    self.results = results