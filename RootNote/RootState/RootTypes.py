
from dataclasses import dataclass
from typing import List

from ..util import VEnum, OrderedVEnum, auto

class Suit(VEnum):
  M = auto()
  F = auto()
  R = auto()
  B = auto()

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

class Faction:
  pass

class Building: 
  pass

class Token:
  pass

class ItemType(VEnum):
  sword = auto()
  crossbow = auto()
  hammer = auto()
  boot = auto()
  bag = auto()
  tea = auto()
  coin = auto()

@dataclass
class Item:
  t : ItemType
  ex : bool = False
  def refresh(self):
    self.ex = True
  def exhaust(self):
    self.ex = False
  
class BoardType(VEnum):
  Autumn = auto()
  Winter = auto()
  Lake = auto()
  Mountain = auto()

class Path(VEnum):
  PATH = auto()
  RIVER = auto()
  CLOSED = auto()
  
class DeckType(VEnum):
  Standard = auto()
  E_P = auto()

class TurnPhase(VEnum):
  Inactive = auto()
  Birdsong = auto()
  Daylight = auto()
  Evening = auto()

class Card:
  pass


BOARDS = {
  BoardType.Autumn : {
    "n_clearings": 12,
    "build_slots": [1,2,1,1,2,1.5,2,2,2,1.5,2.5,1.5],
    "suits": [Suit.F,Suit.M,Suit.R,Suit.R,Suit.R,Suit.F,
              Suit.M,Suit.F,Suit.M,Suit.R,Suit.M,Suit.F],
    "paths": {(1,5):Path.PATH,(1,9):Path.PATH,(1,10):Path.PATH,
      (2,5):Path.PATH,(2,6):Path.PATH,(2,10):Path.PATH,(3,6):Path.PATH,
      (3,7):Path.PATH,(3,11):Path.PATH,(4,8):Path.PATH,(4,9):Path.PATH,
      (4,12):Path.PATH,(6,11):Path.PATH,(7,8):Path.PATH,(7,12):Path.PATH,
      (9,12):Path.PATH,(10,12):Path.PATH,(11,12):Path.PATH,(4,7):Path.RIVER,
      (5,10):Path.RIVER,(7,11):Path.RIVER,(10,11):Path.RIVER},
    "forests": {"1-2-5-10","1-9-10-12","2-6-10-11-12",
      "3-6-11","3-7-11-12","4-7-8-12","4-9-12"},
    "mapping": {"NW":1,"NE":2,"SE":3,"SW":4,"N":5,"E":6,"SCE":7,"SCW":8,"W":9,
      "CN":10, "CE":11, "CW":12},
  },
  BoardType.Winter : {
    "n_clearings": 12,
    "build_slots": [1,1,2,2,2,2,1,1.5,1.5,1,2.5,2.5],
    "paths": {(1,5):Path.PATH,(1,10):Path.PATH,(1,11):Path.PATH,
      (2,6):Path.PATH,(2,7):Path.PATH,(2,12):Path.PATH,(3,7):Path.PATH,
      (3,8):Path.PATH,(3,12):Path.PATH,(4,9):Path.PATH,(4,10):Path.PATH,
      (4,11):Path.PATH,(5,6):Path.PATH,(8,9):Path.PATH,(8,12):Path.PATH,
      (9,11):Path.PATH,(7,12):Path.RIVER,(10,11):Path.RIVER,
      (11,12):Path.RIVER},
    "forests": {"1-2-5-6-11-12","1-4-10-11","2-3-7-12",
      "3-8-12","4-9-11","8-9-11-12"},
    "mapping": {"NW":1,"NE":2,"SE":3,"SW":4,"NCW":5,"NCE":6,"E":7,"SCE":8,
      "SCW":9,"W":10,"CW":11,"CE":12},
  },
  BoardType.Lake : {
    "n_clearings": 12,
    "build_slots": [2,1,1,1,2.5,2,1,1,1,2.5,2.5,2.5],
    "paths": {(1,5):Path.PATH,(1,9):Path.PATH,(2,7):Path.PATH,(2,8):Path.PATH,
      (2,10):Path.PATH,(3,8):Path.PATH,(3,9):Path.PATH,(3,12):Path.PATH,
      (4,5):Path.PATH,(4,6):Path.PATH,(5,11):Path.PATH,(6,7):Path.PATH,
      (6,11):Path.PATH,(7,10):Path.PATH,(7,11):Path.PATH,(8,10):Path.PATH,
      (9,12):Path.PATH,(1,10):Path.RIVER,(1,11):Path.RIVER,(1,12):Path.RIVER,
      (10,11):Path.RIVER,(10,12):Path.RIVER,(11,12):Path.RIVER},
    "forests": {"0-1-5-11","0-1-9-12","2-7-10","2-8-10",
      "0-3-8-10-12","3-9-12","4-5-6-11","6-7-11","0-7-10-11"},
    "mapping": {"SE":1,"NW":2,"SW":3,"NE":4,"E":5,"NCE":6,"NCW":7,"W":8,"S":9,
      "CNW":10,"CE":11,"CSW":12},
  },
  BoardType.Mountain: {
    "n_clearings": 12,
    "build_slots": [2,2,2,2,1,1,1,1,2.5,1.5,2.5,2.5],
    "paths": {(1,8):Path.PATH,(1,9):Path.PATH,(2,6):Path.PATH,(2,11):Path.PATH,
      (3,6):Path.PATH,(3,11):Path.PATH,(4,8):Path.PATH,(4,12):Path.PATH,
      (5,10):Path.PATH,(5,11):Path.PATH,(7,12):Path.PATH,(9,10):Path.PATH,
      (9,12):Path.PATH,(10,11):Path.PATH,(10,12):Path.PATH,(2,10):Path.RIVER,
      (4,10):Path.RIVER,(2,5):Path.CLOSED,(3,7):Path.CLOSED,(5,9):Path.CLOSED,
      (6,11):Path.CLOSED,(8,9):Path.CLOSED,(11,12):Path.CLOSED},
    "forests": {"1-8-9","2-5-11","2-6-11","3-6-11","3-7-11-12",
      "4-8-9-12","5-9-10","5-10-11","9-10-12","10-11-12"},
    "mapping":{"NW":1,"NE":2,"SE":3,"SW":4,"N":5,"E":6,"S":7,"W":8,"CNW":9,
      "CNE":10,"CSE":11,"CSW":12},
  }
}

ITEMS = {
  ItemType.sword:2,
  ItemType.crossbow:1,
  ItemType.hammer:1,
  ItemType.boot:2,
  ItemType.bag:2,
  ItemType.tea:2,
  ItemType.coin:2
}

