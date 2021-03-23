from ..RootState import * # pylint: disable=unused-wildcard-import
from ...util import VEnum, OrderedVEnum, auto

# "Victory Points" details victory condition
# Common operations:
# vp = VP()
#  Add or subtract vps
# vp += n __add__, __iadd__ (__sub__, __isub__)
#  Check for lowest or highest vp faction
# vp <= others __le__, __ge__
#  Check for dom victory
# vp == Suit.M __eq__
#  Set dom victory?
# self.vp = Suit.M
# vp in Suit __contains__

class VictoryException(RootException):
  pass

class VP:
  def __init__(self, faction:Faction, vp = 0):
    self.faction = faction
    self.vp : Union[int,Suit,Faction] = vp
    self.team = [] # Note friends in case of victory

  def victory(self):
    raise VictoryException(self.faction, self.team)
  
  def dominance(self, suit:Suit):
    self.vp = suit

  def coalition(self, faction:Faction):
    self.vp = faction

  def recv_coalition(self, vp):
    self.team.append(vp)

  def __add__(self, n):
    """ Return self plus n """
    if isinstance(n, int):
      if isinstance(self.vp,int):
        self.vp += n
        if self.vp >= 30:
          self.victory()
      return self
    raise ValueError
  
  def __sub__(self,n):
    if isinstance(n, int):
      return self.__add__(-n)
    elif isinstance(n, self.__class__):
      return self.__add__(-n.vp)
    raise ValueError

  def __int__(self):
    if isinstance(self.vp, int):
      return self.vp
    return -1

  def __repr__(self):
    if isinstance(self.vp, int):
      return "<%s VP: %d>" % (self.faction.name, self.vp)
    if isinstance(self.vp, Suit):
      return "<%s Dominance: %s>" % (self.faction.name, self.vp.name)
    if isinstance(self.vp, Faction):
      return "<%s Coalition: %s>" % (self.faction.name, self.vp.name)
    raise NotImplementedError

  def __eq__(self,other):
    if type(other) == type(self.vp): # Works for other => int, Suit, Faction
      return self.vp == other
    if isinstance(other, self.__class__): # Works for other => VP
      return self.vp == other.vp
    return False
  
  # Implment all four below so that dom/coalition are neither gt or lt int
  def __lt__(self,other):
    if isinstance(self.vp, int):
      if isinstance(other, int):
        return self.vp < other
      if isinstance(other, self.__class__):
        return self.vp < other.vp
    return False

  def __le__(self,other):
    if isinstance(self.vp, int):
      if isinstance(other, int):
        return self.vp <= other
      if isinstance(other, self.__class__):
        return self.vp <= other.vp
    return False

  def __gt__(self,other):
    if isinstance(self.vp, int):
      if isinstance(other, int):
        return self.vp > other
      if isinstance(other, self.__class__):
        return self.vp > other.vp
    return False
    
  def __ge__(self,other):
    if isinstance(self.vp, int):
      if isinstance(other, int):
        return self.vp >= other
      if isinstance(other, self.__class__):
        return self.vp >= other.vp
    return False

  # Check if we are teamed
  def __contains__(self,other):
    if isinstance(other, self.__class__):
      return other in self.team
    return False

class Track:
  def __init__(self, limit:int, start:int):
    self.limit = limit
    self.n = start

  def use(self):
    self.n -= 1
    assert self.n >= 0
    return self.points

  def ret(self):
    self.n += 1
    assert self.n <= self.limit

  def __getattribute__(self, name):
    if isinstance(self.__dict__[name], list):
      i = self.limit-self.n
      return self.__dict__[name][i]
    else:
      return object.__getattribute__(self,name)

class FactionState:
  def __init__(self, faction:Faction, root_state:RootState):
    self.faction = faction
    self.root_state = root_state
    self.hand : int = 0
    self.warrior_supply = 0
    self.crafted_improvements : List[Card] = []
    self.vp : VP = VP(faction)
  
  def __setattr__(self, name, value):
    if name == "vp" and name in self.__dict__:
      if isinstance(value, Suit):
        self.vp.dominance(value)
      if isinstance(value, Faction):
        self.vp.coalition(value)
    else:
      object.__setattr__(self,name,value)

 