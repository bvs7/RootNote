
from typing import NewType, Mapping, Set, Dict, Tuple, List

from .BaseTypes import Faction, Factions, Building, Buildings, Token, Tokens
from .util import VEnum, auto

# Here, only import necessary Factions?

from .MC_Types import * # pylint: disable=unused-wildcard-import
from .ED_Types import * # pylint: disable=unused-wildcard-import
from .WA_Types import * # pylint: disable=unused-wildcard-import
from .VB_Types import * # pylint: disable=unused-wildcard-import

class Suit(VEnum):
  M = "M"
  F = "F"
  R = "R"
  B = "B"

  def __le__(self,other):
    if isinstance(other, str):
      other = self.__getattribute__(other)
    return other == self.B or self == other
  def __lt__(self,other):
    if isinstance(other, str):
      other = self.__getattribute__(other)
    return self != self.B and other == self.B
  def __ge__(self,other):
    if isinstance(other, str):
      other = self.__getattribute__(other)
    return self == self.B or self == other
  def __gt__(self,other):
    if isinstance(other, str):
      other = self.__getattribute__(other)
    return self == self.B and other != self.B

class ItemType(VEnum):
  sword = "sword"
  crossbow = "crossbow"
  hammer = "hammer"
  boot = "boot"
  bag = "bag"
  tea = "tea"
  coin = "coin"
  
class BoardType(VEnum):
  Autumn = "Autumn"
  Winter = "Winter"
  Lake = "Lake"
  Mountain = "Mountain"

class PathType(VEnum):
  PATH = "PATH"
  RIVER = "RIVER"
  CLOSED = "CLOSED"

ClearingIndex = NewType("ClearingIndex", int)

# pathid is x-y where x and y are clearing Indexes
PathID = str
PathDict = Dict[PathID,PathType]
ForestID = List[ClearingIndex]
ForestList = List[ForestID]

WarriorCount = Dict[Faction,int]
  
class DeckType(VEnum):
  Standard = "Standard"
  E_P = "E_P"

class TurnPhase(VEnum):
  Inactive = "Inactive"
  Birdsong = "Birdsong"
  Daylight = "Daylight"
  Evening = "Evening"

# TODO: figure out how to associate current turn (faction) with this?
class GamePhase(VEnum):
  Setup = "Setup"
  Play = "Play"

class Card:
  def __init__(self, suit:Suit):
    self.suit = suit

PlayerName = NewType("PlayerName",str)

class Deserializable:

  @classmethod
  def _deserialize(cls,*args,**kwargs):
    return cls(*args,**kwargs)

### DEFAULTS AND DATA. Put this in JSON?

BOARDS = {
  BoardType.Autumn : {
    "n_clearings": 12,
    "build_slots": [1,2,1,1,2,1.5,2,2,2,1.5,2.5,1.5],
    "suits": [Suit.F,Suit.M,Suit.R,Suit.R,Suit.R,Suit.F,
              Suit.M,Suit.F,Suit.M,Suit.R,Suit.M,Suit.F],
    "paths": {(1,5):PathType.PATH,(1,9):PathType.PATH,(1,10):PathType.PATH,
      (2,5):PathType.PATH,(2,6):PathType.PATH,(2,10):PathType.PATH,(3,6):PathType.PATH,
      (3,7):PathType.PATH,(3,11):PathType.PATH,(4,8):PathType.PATH,(4,9):PathType.PATH,
      (4,12):PathType.PATH,(6,11):PathType.PATH,(7,8):PathType.PATH,(7,12):PathType.PATH,
      (9,12):PathType.PATH,(10,12):PathType.PATH,(11,12):PathType.PATH,(4,7):PathType.RIVER,
      (5,10):PathType.RIVER,(7,11):PathType.RIVER,(10,11):PathType.RIVER},
    "forests": {"1-2-5-10","1-9-10-12","2-6-10-11-12",
      "3-6-11","3-7-11-12","4-7-8-12","4-9-12"},
    "mapping": {"NW":1,"NE":2,"SE":3,"SW":4,"N":5,"E":6,"SCE":7,"SCW":8,"W":9,
      "CN":10, "CE":11, "CW":12},
  },
  BoardType.Winter : {
    "n_clearings": 12,
    "build_slots": [1,1,2,2,2,2,1,1.5,1.5,1,2.5,2.5],
    "suits":None,
    "paths": {(1,5):PathType.PATH,(1,10):PathType.PATH,(1,11):PathType.PATH,
      (2,6):PathType.PATH,(2,7):PathType.PATH,(2,12):PathType.PATH,(3,7):PathType.PATH,
      (3,8):PathType.PATH,(3,12):PathType.PATH,(4,9):PathType.PATH,(4,10):PathType.PATH,
      (4,11):PathType.PATH,(5,6):PathType.PATH,(8,9):PathType.PATH,(8,12):PathType.PATH,
      (9,11):PathType.PATH,(7,12):PathType.RIVER,(10,11):PathType.RIVER,
      (11,12):PathType.RIVER},
    "forests": {"1-2-5-6-11-12","1-4-10-11","2-3-7-12",
      "3-8-12","4-9-11","8-9-11-12"},
    "mapping": {"NW":1,"NE":2,"SE":3,"SW":4,"NCW":5,"NCE":6,"E":7,"SCE":8,
      "SCW":9,"W":10,"CW":11,"CE":12},
  },
  BoardType.Lake : {
    "n_clearings": 12,
    "build_slots": [2,1,1,1,2.5,2,1,1,1,2.5,2.5,2.5],
    "suits":None,
    "paths": {(1,5):PathType.PATH,(1,9):PathType.PATH,(2,7):PathType.PATH,(2,8):PathType.PATH,
      (2,10):PathType.PATH,(3,8):PathType.PATH,(3,9):PathType.PATH,(3,12):PathType.PATH,
      (4,5):PathType.PATH,(4,6):PathType.PATH,(5,11):PathType.PATH,(6,7):PathType.PATH,
      (6,11):PathType.PATH,(7,10):PathType.PATH,(7,11):PathType.PATH,(8,10):PathType.PATH,
      (9,12):PathType.PATH,(1,10):PathType.RIVER,(1,11):PathType.RIVER,(1,12):PathType.RIVER,
      (10,11):PathType.RIVER,(10,12):PathType.RIVER,(11,12):PathType.RIVER},
    "forests": {"0-1-5-11","0-1-9-12","2-7-10","2-8-10",
      "0-3-8-10-12","3-9-12","4-5-6-11","6-7-11","0-7-10-11"},
    "mapping": {"SE":1,"NW":2,"SW":3,"NE":4,"E":5,"NCE":6,"NCW":7,"W":8,"S":9,
      "CNW":10,"CE":11,"CSW":12},
  },
  BoardType.Mountain: {
    "n_clearings": 12,
    "build_slots": [2,2,2,2,1,1,1,1,2.5,1.5,2.5,2.5],
    "suits":None,
    "paths": {(1,8):PathType.PATH,(1,9):PathType.PATH,(2,6):PathType.PATH,(2,11):PathType.PATH,
      (3,6):PathType.PATH,(3,11):PathType.PATH,(4,8):PathType.PATH,(4,12):PathType.PATH,
      (5,10):PathType.PATH,(5,11):PathType.PATH,(7,12):PathType.PATH,(9,10):PathType.PATH,
      (9,12):PathType.PATH,(10,11):PathType.PATH,(10,12):PathType.PATH,(2,10):PathType.RIVER,
      (4,10):PathType.RIVER,(2,5):PathType.CLOSED,(3,7):PathType.CLOSED,(5,9):PathType.CLOSED,
      (6,11):PathType.CLOSED,(8,9):PathType.CLOSED,(11,12):PathType.CLOSED},
    "forests": {"1-8-9","2-5-11","2-6-11","3-6-11","3-7-11-12",
      "4-8-9-12","5-9-10","5-10-11","9-10-12","10-11-12"},
    "mapping":{"NW":1,"NE":2,"SE":3,"SW":4,"N":5,"E":6,"S":7,"W":8,"CNW":9,
      "CNE":10,"CSE":11,"CSW":12},
  }
}

# Just a list? nah
START_ITEMS = {
  ItemType.sword:2,
  ItemType.crossbow:1,
  ItemType.hammer:1,
  ItemType.boot:2,
  ItemType.bag:2,
  ItemType.tea:2,
  ItemType.coin:2
}
