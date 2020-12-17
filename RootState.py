from typing import List

# Base class for other factions
class Faction:
  pass

class MapState:

  def init(self):
    # Clearings
    # Items
    # VPs
    # Forests
    # etc
    pass

class RootState:
  """ State of a root game """

  def __init__(self):
    self.factions:List[Faction] = []
    self.map:MapState = MapState()