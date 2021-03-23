from .FactionState import * # pylint: disable=unused-wildcard-import

class Decree:
  def __init__(self):
    self.recruit :List[Suit] = []
    self.move : List[Suit] = []
    self.battle : List[Suit] = []
    self.build : List[Suit] = []
    self.cards : List[Card] = []
  
  # Turmoil? return humiliation and discard cards
  def turmoil(self):
    full_decree = self.recruit + self.move + self.battle + self.build
    humiliate = sum([1 for s in full_decree if s == Suit.B])
    discard = self.cards
    self.cards = []
    return (humiliate, discard)

class RoostTrack(Track):
  def __init__(self):
    super().__init__(7,7)
    self.score = [0,1,2,3,4,4,5]
    self.card_draw = [1,1,2,2,2,3,3]

class ED_State(FactionState):
  def __init__(self, board_state:Board):
    super().__init__(Faction.ED, board_state)
    self.warrior_supply : int = 20
    self.decree = Decree()
    self.leader : Leader = None
    self.roost_track = RoostTrack()
    self.crafted_items : List[Item] = []