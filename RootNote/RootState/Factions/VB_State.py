from .FactionState import *

class TeaTrack(Track):
  def __init__(self):
    super().__init__(3,0)
    self.refresh = [9,7,5,3]

class CoinTrack(Track):
  def __init__(self):
    super().__init__(3,0)
    self.card_draw = [4,3,2,1]

class BagTrack(Track):
  def __init__(self):
    super().__init__(3,0)
    self.capacity = [12,10,8,6]

class Satchel:
  def __init__(self):
    self.items : List[Item]
    self.broken : List[Item]
    self.tea_track = TeaTrack()
    self.coin_track = CoinTrack()
    self.bag_track = BagTrack()

class VB_State(FactionState):
  def __init__(self, board_state:Board):
    super().__init__(Faction.VB, board_state)
    self.location = None
    self.satchel = Satchel()
    self.relationships : Dict[Faction,Relation] = {}

if __name__ == "__main__":
  vb = VB_State(None)
  vb.satchel.tea_track.refresh