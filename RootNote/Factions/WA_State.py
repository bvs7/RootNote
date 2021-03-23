from .FactionState import * # pylint: disable=unused-wildcard-import

class SympathyTrack(Track):
  def __init__(self):
    super().__init__(10,10)
    self.points = [0,0,1,1,1,2,2,3,4,4,4] 
    self.cost = [1,1,1,2,2,2,3,3,3,3] # First should cost 1, not zero

class Bases(set):
  def __init__(self):
    super().__init__([Building.Mbase,Building.Fbase,Building.Rbase])

  def __getattribute__(self,name):
    if name == "card_draw":
      return 4 - len(self)
    else:
      return super().__getattribute__(name)

class WA_State(FactionState):
  def __init__(self, board_state:Board):
    super().__init__(Faction.WA,board_state)
    self.warrior_supply : int = 10
    self.officers : int = 0
    self.sympathy_track : SympathyTrack = SympathyTrack()
    self.bases : Bases = Bases()
    self.crafted_items : List[Item] = []

