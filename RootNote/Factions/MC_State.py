from .FactionState import *

class MC_Track(Track):
  def __init__(self, building:Building):
    super().__init__(6,6)
    self.building = building
    self.costs = [0,1,2,3,3,4,None] # at 0 built -> 0, at 1 built -> 1, etc
    if building == Building.sawmill:
      self.points = [0,0,1,2,3,3,4] # 0 for 0th place, 0 for 1st, 1 for 2nd, etc
    elif building == Building.workshop:
      self.points = [0,0,2,2,3,4,5]
    elif building == Building.recruiter:
      self.points = [0,0,1,2,3,4,5]
      self.card_draw = [1,1,1,2,2,3,3]

class MC_State(FactionState):
  def __init__(self, board_state:Board):
    super().__init__(Faction.MC, board_state)
    self.board_state = board_state
    self.warrior_supply = 25
    self.wood = 8
    self.tracks = {
      Building.sawmill : MC_Track(Building.sawmill),
      Building.workshop: MC_Track(Building.workshop),
      Building.recruiter : MC_Track(Building.recruiter),
    }
    self.crafted_items : List[Item] = []
