from typing import NewType, List, Set, Dict, Optional, Union, Any
import dataclasses
import math

from .RootTypes import *

class RootException(Exception):
  pass

@dataclasses.dataclass
class Clearing:
  board_state : "Board"
  n : int
  suit : Suit
  build_slots : int
  ruin : bool
  warriors : Dict[Faction, int] = {}
  buildings : List[Building] = []
  tokens : List[Token] = []
  pawns : List[Faction] = []


  def rule(self) -> Optional[Faction]:
    # check for gardens? (later)
    f_totals = {}
    for faction in self.warriors:
      if not faction in f_totals:
        f_totals[faction] = 0
      f_totals[faction] += self.warriors[faction]
    for building in self.buildings:
      faction = building.faction
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

# BoardState
class Board:
  def __init__(self, board_type:Optional[BoardType]=None,
               clearing_suits:Optional[List[Suit]] = None):
    if not board_type:
      board_type = BoardType.Autumn
    board_setup = BOARDS[board_type]
    if clearing_suits:
      board_setup["suits"] = clearing_suits

    if not "suits" in board_setup:
      raise RootException("Did not declare board suits!")

    n_clearings = board_setup["n_clearings"]
    suits = board_setup["suits"]
    build_slots = board_setup["build_slots"]

    self.clearings = [Clearing(self, i+1, suits[i], math.floor(build_slots[i]),
      build_slots[i] % 1 == .5) for i in range(n_clearings)]

    self.mapping = board_setup["mapping"]

    # These shouldn't change, they are for reference (PathTypes should be json!)
    # TODO: after implementing json storage, change this
    paths = board_setup["paths"]
    self.paths = dict([(cs,Path(paths[cs])) for cs in paths])
    self.forests : Set[str] = board_setup["forests"]
  
  def __getitem__(self, key):
    # TODO: parse key better
    if key in self.mapping:
      idx = self.mapping[key]
    idx = key - 1
    if idx < 0 or idx >= len(self):
      raise IndexError("Index %d out of range, clearings use 1-indexing" % idx)
    return self.clearings[idx]
    
# TODO: lizard redirect?
class Deck:
  def __init__(self, deck_type:DeckType):
    self.deck_type = deck_type
    self.deck_count = 54
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

# TODO: intuit board type or deck type?!
# Or, maybe that info isn't necessary?
# What about clearing suits? Later
# RootState
class RootState:
  def __init__(self, board_type:Optional[BoardType] = None,
      clearing_suits:Optional[List[Suit]] = None,
      deck_type:Optional[DeckType] = None):
    self.board = Board(board_type, clearing_suits)
    self.deck = Deck(deck_type)
    self.item_cache = ITEMS.copy()
    self.factions = {} # maps faction name to faction Board?
