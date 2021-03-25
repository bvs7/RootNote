from typing import Optional, List, NewType, Set

# Hmmm want to associate a faction with Pieces...

Faction = NewType("Faction",str)
Factions : List[Faction] = []

class Cardboard:
  def __init__(self, name:str, faction:Faction):
    self.name = name
    self.faction = faction

  def __repr__(self):
    return "<{}({}): {}>".format(self.__class__.__name__, self.faction, self.name)

class Building(Cardboard):
  pass

Buildings : List[Building] = []

class Token(Cardboard):
  pass

Tokens : List[Token] = []