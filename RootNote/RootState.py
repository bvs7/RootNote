from typing import Optional, List, Dict, Set, OrderedDict, Tuple, Any
import math

from .RootTypes import *

import RootNote.RootJSON as RootJSON

class RootException(Exception):
  pass

class Clearing(Deserializable):

  # No suit!
  def __init__(self, idx : ClearingIndex = 0, suit : Optional[Suit] = None, 
              slots : int = 1, ruin : bool = False, **kwargs):
    self.idx       : ClearingIndex  = idx
    self.suit      : Optional[Suit] = suit
    self.slots     : int            = slots
    self.ruin      : bool           = ruin

    self.init()

    self.__dict__.update(kwargs) #pylint: disable=no-member

  def init(self):
    self.warriors  : WarriorCount   = {}
    self.buildings : List[Building] = []
    self.tokens    : List[Token]    = []

  def __repr__(self):
    return "Clearing{}:{}".format(self.idx,self.suit if self.suit else "-")
    

class ClearingList(list, Deserializable):

  @staticmethod
  def to_idx(key) -> ClearingIndex:
    if isinstance(key, int):
      idx = ClearingIndex(key-1)
    else:
      raise NotImplementedError("Haven't done clearing mapping stuff yet")
    return idx

  def __getitem__(self, key):
    return super().__getitem__(self.to_idx(key))

  def __setitem__(self, key, value):
    super().__setitem__(self.to_idx(key), value)

def clearing_setup(board_type:BoardType) -> ClearingList:
  board_setup = BOARDS[board_type]
  clearing_setup : List[Tuple[ClearingIndex, Optional[Suit], int, bool]] = ClearingList()
  for i in range(board_setup["n_clearings"]):
    clearing_setup.append(
      Clearing(ClearingIndex(i+1), board_setup["suits"][i] if board_setup["suits"] else None , board_setup["build_slots"][i] // 1, board_setup["build_slots"][i] % 1 == .5)
    )
  return clearing_setup

def paths_setup(board_type:BoardType) -> PathDict:
  board_setup = BOARDS[board_type]
  paths = board_setup['paths']
  pathdict : PathDict = {}
  for p, pt in paths.items():
    path_id = tuple(sorted(p))
    pathdict[path_id] = pt
  return pathdict

def forests_setup(board_type:BoardType) -> ForestList:
  board_setup = BOARDS[board_type]
  forestset = []
  for f in board_setup["forests"]:
    cs = [ClearingIndex(int(c)) for c in f.split("-")]
    fs = sorted(cs)
    forestset.append(fs)

  return forestset



# BoardState
class Board(Deserializable):
  def __init__(self, board_type:BoardType):
    
    # Create board_setup from board_type
    self.board_type : BoardType           = board_type
    self.clearings  : List[Clearing]      = []
    self.paths      : Optional[PathDict]  = None
    self.forests    : Optional[ForestList] = None

  @classmethod
  def load_default(cls,board_type:BoardType):
    with open("RootNote/data/board_defaults/{}_board_default.json".format(board_type), 'r') as fp:
      return RootJSON.load(fp)

  @classmethod
  def _deserialize(cls, **kwargs):
    b = cls(kwargs.pop("board_type"))
    b.clearings = ClearingList(kwargs.pop("clearings"))
    b.__dict__.update(kwargs)
    return b

  def __repr__(self):
    return "{}({}): {}".format(self.__class__.__name__, self.board_type, self.clearings)
    
# TODO: lizard redirect?
class Deck:
  def __init__(self, deck_type:DeckType):
    self.deck_type = deck_type
    self.deck_count = 54 # Remove dominance for 2p
    self.discard_pile : List[Card] = []

  def draw(self, n):
    for _ in range(n):
      if self.deck_count < 1:
        self.reshuffle()
      self.deck_count -= 1

  def discard(self, card:Card):
    self.discard_pile.append(card)

  def reshuffle(self):
    n = len(self.discard_pile)
    self.discard_pile = []
    self.deck_count += n

  def __repr__(self):
    return "{}({}): {}|{}".format(self.__class__.__name__, self.deck_type, self.deck_count, len(self.discard_pile))

class RootState(Deserializable):
  def __init__(self):

    self.board : Optional[Board] = None
    self.deck  : Optional[Deck]  = None
    self.item_cache : Dict[ItemType, int] = START_ITEMS.copy()
    self.draft_pool : Optional[List[Faction]] = None 
    self.turn_order : Optional[List[PlayerName]] = None
    self.factions : Dict[Faction,Any] = {} # Also, factions will be in turn order?

  ## Setup Operations:
  def chooseBoardType(self, board_type : BoardType):
    self.board = Board.load_default(board_type)

  def chooseDeckType(self, deck_type : DeckType):
    self.deck = Deck(deck_type)

  # TODO: Update function. Calls sub updates on factions with args?
  # Could eventually take a slightly worked RootMove and call appropriate things.
  def update(self, name, *args, faction = None):
    pass

  @classmethod
  def _deserialize(cls, **kwargs):
    r = RootState()
    del kwargs["__class__"]
    r.__dict__.update(kwargs)
    return r

  def __repr__(self):
    msg =("{}:\n".format(self.__class__.__name__) + \
          "{}\n".format(self.board) + \
          "Deck: {}\n".format(self.deck) + \
          "Items: {}\n".format(self.item_cache) )
    return msg

if __name__ == "__main__":
  for board_type in BoardType:
    r = RootState()
    r.chooseBoardType(board_type)
    r.chooseDeckType(DeckType.Standard)
    print(r)