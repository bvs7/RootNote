
from typing import List, Dict

class MC_Building(Building):
  pass

# Just do these as enums?
# Dynamically add to Building Enum?
class Sawmill(MC_Building):
  pass

class Workshop(MC_Building):
  pass

class Recruiter(MC_Building):
  pass


class MC_Track(Track):
  def __init__(self, building:MC_Building):
    super().__init__(6,6)
    self.building = building
    self.costs = [0,1,2,3,3,4,None] # at 0 built -> 0, at 1 built -> 1, etc
    if building == Sawmill:
      self.points = [0,0,1,2,3,3,4] # 0 for 0th place, 0 for 1st, 1 for 2nd, etc
    elif building == Workshop:
      self.points = [0,0,2,2,3,4,5]
    elif building == Recruiter:
      self.points = [0,0,1,2,3,4,5]
      self.card_draw = [1,1,1,2,2,3,3]


# TODO: make more functional?
class MC_State(FactionState):
  def __init__(self, state:RootState):
    super().__init__(Faction.MC, state)
    self.warrior_supply = 25
    self.wood = 8
    self.tracks = {
      Sawmill : MC_Track(Sawmill),
      Workshop: MC_Track(Workshop),
      Recruiter : MC_Track(Recruiter),
    }
    self.crafted_items : List[Item] = []
    self.crafting_ability : Dict[Suit,int] = {}

  

  def place_wood(self, cs : List[int]):
    sm = Sawmill
    sm_track = self.tracks[sm]
    n_sm = sm_track.limit - sm_track.n
    if self.wood < n_sm:
      # Uh oh, not enough wood, must be chosen
      assert n_sm == len(cs), "Incorrect number of wood placements"
      c_dict = {}
      for c in cs:
        if not c in c_dict:
          c_dict[c] = 0
        c_dict[c] += 1
      for c in c_dict:
        n = c_dict[c]
        cl = self.board_state[c]
        assert len([s for s in cl.buildings if s == sm]) >= n
        self.wood -= n
        cl.tokens.append(Token.wood)
    else:
      for cl in self.board_state.clearings:
        sm_s = [s for s in cl.buildings if s == sm]
        for s in sm_s:
          self.wood -= 1
          cl.tokens.extend([Token.wood]*n_sm)

  def get_crafting_ability(self):
    capability : Dict[Suit,int] = {Suit.M:0,Suit.F:0,Suit.R:0}
    for c in self.board_state.clearings:
      n_ws = len(ws for ws in c.buildings if ws == Workshop)
      capability[c.suit] += n_ws
    

  def craft(self, card:Card):
    # assume card is in hand
    self.hand -= 1
    # Either goes to crafted improvements
    if card.crafted_improvement:
      self.crafted_improvements.append(card)
    # Or makes an item
    if card.item:
      item = card.item
      assert self.board_state.items[item] > 0
      self.crafted_items.append(Item(item))
      self.board_state.items[item] -= 1
      self.vp += card.vp
  
  def build(self, building:Building, clearing:int, wood:List[int]):
    track = self.tracks[building]
    assert track.n > 0
    c = self.board_state.clearings[clearing]
    assert c.rule() == Faction.MC
    assert len(c.buildings)+1 <= c.build_slots
    # Ensure wood can get here, or find if wood is trivial
    reachable_clearings = self.reachable_clearings(c.n)
    for wood_clearing in wood:
      assert wood_clearing in reachable_clearings
      wc = self.board_state.clearings[wood_clearing]
      assert Token.wood in wc.tokens
      wc.tokens.remove(Token.wood)
    c.buildings.append(building)
    self.vp += track.use()

  def reachable_clearings(self, clearing:int):
    ps = self.board_state.paths
    paths = [p for p in ps if ps[p] in self.movable]
    reachable_clearings = set()
    frontier_clearings = {clearing}
    added_clearings = set()
    not_done = True
    while not_done:
      not_done = False
      for c in frontier_clearings:
        for p in paths:
          oc = None
          if c == p[0]:
            oc = p[1]
          if c == p[1]:
            oc = p[0]
          if not oc == None:
            if (self.board_state.clearings[oc].rule() == self.faction and
              not oc in reachable_clearings | frontier_clearings):
              not_done = True
              added_clearings.add(oc)
      reachable_clearings |= frontier_clearings
      frontier_clearings = added_clearings
      added_clearings = set()
    return reachable_clearings

  def move(self, n:int, start:int, dest:int):
    start_c = self.board_state.clearings[start]
    dest_c = self.board_state.clearings[dest]
    p = sorted(start_c,dest_c)
    p = (p[0],p[1])
    assert p in self.board_state.paths[p]
    path = self.board_state.paths[p]
    assert path in self.movable
    assert start_c.rule() == self.faction or dest_c.rule() == self.faction
    for _ in range(n):
      start_c.warriors.remove(self.faction)
      dest_c.warriors.append(self.faction)
    
    if Token.sympathy in dest_c.tokens:
      # Trigger outrage!
      pass

  def recruit(self, cs:List[int]):
    rec_track = self.tracks[Recruiter]
    n_rec = rec_track.limit - rec_track.n
    if n_rec > self.warrior_supply:
      for c in cs:
        cl = self.board_state.clearings[c]
        cl.warriors.append(Faction.MC)
    else:
      for c in self.board_state.clearings:
        n_r = len([rec for rec in c.buildings if rec == Recruiter])
        c.warriors.extend([Faction.MC] * n_r)

  def draw(self):
    rec_track = self.tracks[Recruiter]
    n_draw = rec_track.card_draw
    self.board_state.deck.draw(n_draw)
    self.hand += n_draw

  def discard(self, cards:List[Card]):
    for card in cards:
      self.board_state.deck.discard(card)
      self.hand -= 1
