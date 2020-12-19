from typing import NewType, List, Set, Dict, Optional, Union
from dataclasses import dataclass

from .util import VEnum, OrderedVEnum, auto


class Suit(VEnum):
  M=auto()
  F=auto()
  R=auto()
  B=auto()
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

class Faction(OrderedVEnum):
  MC = auto()
  ED = auto()
  WA = auto()
  VB = auto()

class Building(VEnum): 
  sawmill = auto()
  workshop = auto()
  recruiter = auto()
  roost = auto()
  Mbase = auto()
  Fbase = auto()
  Rbase = auto()
  def __getattr__(self, name):
    if name == "faction":
      if self in [self.sawmill, self.workshop, self.recruiter]:
        return Faction.MC
      if self in [self.roost]:
        return Faction.ED
      if self in [self.Mbase, self.Fbase, self.Rbase]:
        return Faction.WA
    else:
      return super().__getattr__(name)

class Token(VEnum):
  keep = auto()
  wood = auto()
  sympathy = auto()
  def __getattr__(self, name):
    if name == "faction":
      if self in [self.keep, self.wood]:
        return Faction.MC
      if self in [self.sympathy]:
        return Faction.WA
    else:
      return super().__getattr__(name)

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
  
Leader = VEnum('Leader', 'Builder Charismatic Commander Despot')
Relation = OrderedVEnum("Relation",'Hostile Indifferent Favorable Cordial Allied')
Board = VEnum('Board', 'Autumn Winter Lake Mountain')
Path = VEnum('Path','PATH RIVER CLOSED')
Deck = VEnum("Deck", 'Standard E_P')


class RootException(Exception):
  pass

class Clearing:
  def __init__(self, board_state, n:int, suit:Suit, build_slots:int):
    self.board_state = board_state
    self.n = n
    self.suit = suit
    self.build_slots = build_slots
    self.warriors : List[Faction] = []
    self.buildings : List[Building] = []
    self.tokens : List[Token] = []
    self.pawns : List[Faction] = []

  def rule(self) -> Optional[Faction]:
    # check for lizards (later)
    f_totals = {}
    for faction in (self.warriors + [b.faction for b in self.buildings]):
      if not faction in f_totals:
        f_totals[faction] = 0
      f_totals[faction] += 1
    if len(f_totals) == 0:
      return None
    f_list = sorted(f_totals.items(), key=(lambda f: f[1] + (.5 if f[0]==Faction.ED else 0)))
    if len(f_list) == 1:
      return f_list[-1][0]
    else:
      if f_list[-1][1] == f_list[-2][1] and not f_list[-1][0] == Faction.ED:
        return None
      else:
        return f_list[-1][0]

class Clearings(list):
  def __init__(self, bs, n, suits:List[Suit], build_slots:List[int]):
    super().__init__(
      [Clearing(bs,i+1,suits[i],build_slots[i]) for i in range(n)])

  def __getitem__(self,i):
    i -= 1
    if i < 0 or i > len(self):
      raise IndexError("Index %d out of range, clearings use 1-indexing" % i)
    return super().__getitem__(i)

class Card:
  def __init__(self):
    pass

# TODO: lizard redirect?
class Deck_:
  def __init__(self, deck_type:Deck):
    self.deck_type = deck_type
    self.deck_count = 54
    self.discard : List[Card] = []

  def draw(self, n):
    for _ in range(n):
      if self.deck_count < 1:
        self.reshuffle()
      self.deck_count -= 1

  def reshuffle(self):
    n = len(self.discard)
    self.discard = []
    self.deck_count += n

BOARDS = {
  Board.Autumn : {
    "n_clearings": 12,
    "build_slots": [1,2,1,1,2,1.5,2,2,2,1.5,2.5,1.5],
    "suits": [Suit.F,Suit.M,Suit.R,Suit.R,Suit.R,Suit.F,
              Suit.M,Suit.F,Suit.M,Suit.R,Suit.M,Suit.F],
    "paths": {"1-5":Path.PATH,"1-9":Path.PATH,"1-10":Path.PATH,
      "2-5":Path.PATH,"2-6":Path.PATH,"2-10":Path.PATH,"3-6":Path.PATH,
      "3-7":Path.PATH,"3-11":Path.PATH,"4-8":Path.PATH,"4-9":Path.PATH,
      "4-12":Path.PATH,"6-11":Path.PATH,"7-8":Path.PATH,"7-12":Path.PATH,
      "9-12":Path.PATH,"10-12":Path.PATH,"11-12":Path.PATH,"4-7":Path.RIVER,
      "5-10":Path.RIVER,"7-11":Path.RIVER,"10-11":Path.RIVER},
    "forests": {"1-2-5-10","1-9-10-12","2-6-10-11-12",
      "3-6-11","3-7-11-12","4-7-8-12","4-9-12"},
  },
  Board.Winter : {
    "n_clearings": 12,
    "build_slots": [1,1,2,2,2,2,1,1.5,1.5,1,2.5,2.5],
    "paths": {"1-5":Path.PATH,"1-10":Path.PATH,"1-11":Path.PATH,
      "2-6":Path.PATH,"2-7":Path.PATH,"2-12":Path.PATH,"3-7":Path.PATH,
      "3-8":Path.PATH,"3-12":Path.PATH,"4-9":Path.PATH,"4-10":Path.PATH,
      "4-11":Path.PATH,"5-6":Path.PATH,"8-9":Path.PATH,"8-12":Path.PATH,
      "9-11":Path.PATH,"7-12":Path.RIVER,"10-11":Path.RIVER,
      "11-12":Path.RIVER},
    "forests": {"1-2-5-6-11-12","1-4-10-11","2-3-7-12",
      "3-8-12","4-9-11","8-9-11-12"},
  },
  Board.Lake : {
    "n_clearings": 12,
    "build_slots": [2,1,1,1,2.5,2,1,1,1,2.5,2.5,2.5],
    "paths": {"1-5":Path.PATH,"1-9":Path.PATH,"2-7":Path.PATH,"2-8":Path.PATH,
      "2-10":Path.PATH,"3-8":Path.PATH,"3-9":Path.PATH,"3-12":Path.PATH,
      "4-5":Path.PATH,"4-6":Path.PATH,"5-11":Path.PATH,"6-7":Path.PATH,
      "6-11":Path.PATH,"7-10":Path.PATH,"7-11":Path.PATH,"8-10":Path.PATH,
      "9-12":Path.PATH,"1-10":Path.RIVER,"1-11":Path.RIVER,"1-12":Path.RIVER,
      "10-11":Path.RIVER,"10-12":Path.RIVER,"11-12":Path.RIVER},
    "forests": {"0-1-5-11","0-1-9-12","2-7-10","2-8-10",
      "0-3-8-10-12","3-9-12","4-5-6-11","6-7-11","0-7-10-11"},
  },
  Board.Mountain: {
    "n_clearings": 12,
    "build_slots": [2,2,2,2,1,1,1,1,2.5,1.5,2.5,2.5],
    "paths": {"1-8":Path.PATH,"1-9":Path.PATH,"2-6":Path.PATH,"2-11":Path.PATH,
      "3-6":Path.PATH,"3-11":Path.PATH,"4-8":Path.PATH,"4-12":Path.PATH,
      "5-10":Path.PATH,"5-11":Path.PATH,"7-12":Path.PATH,"9-10":Path.PATH,
      "9-12":Path.PATH,"10-11":Path.PATH,"10-12":Path.PATH,"2-10":Path.RIVER,
      "4-10":Path.RIVER,"2-5":Path.CLOSED,"3-7":Path.CLOSED,"5-9":Path.CLOSED,
      "6-11":Path.CLOSED,"8-9":Path.CLOSED,"11-12":Path.CLOSED},
    "forests": {"1-8-9","2-5-11","2-6-11","3-6-11","3-7-11-12",
      "4-8-9-12","5-9-10","5-10-11","9-10-12","10-11-12"},
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


# BoardState
class BoardState:
  def __init__(self, board:Board=Board.Autumn, deck:Deck=Deck.Standard, clearing_suits:List[Suit] = []):
    b = BOARDS[board]
    if len(clearing_suits) > 0:
      b["suits"] = clearing_suits

    n_clearings = b["n_clearings"]
    suits = b["suits"]
    build_slots = b["build_slots"]

    self.clearings = Clearings(self, n_clearings, suits, build_slots)

    # These shouldn't change, they are for reference
    self.paths = b["paths"]
    self.forests = b["forests"]
    # This is mutable
    self.items = ITEMS.copy()
    

# RootState
class RootState:
  def __init__(self):
    self.board = None
    self.factions = {} # maps faction name to faction
