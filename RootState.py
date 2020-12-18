from typing import List, Set, Dict
from enum import Enum, auto





class RootException(Exception):
  pass

class Suit(Enum):
  M=auto()
  F=auto()
  R=auto()
  B=auto()

class Faction(Enum):
  MC=auto()
  ED=auto()
  WA=auto()
  VB=auto()

class BoardType(Enum):
  Autumn=auto()
  Winter=auto()
  Lake=auto()
  Moutain=auto()

class DeckType(Enum):
  Standard=auto()
  E_P=auto()

class ItemType(Enum):
  sword = auto()
  crossbow = auto()
  hammer = auto()
  boot = auto()
  bag = auto()
  tea = auto()
  coins = auto()

class ItemNotAvailableException(RootException):
  pass

class Items:
  def __init__(self):
    self.items = {
      ItemType.sword : 2,
      ItemType.crossbow : 1,
      ItemType.hammer : 1,
      ItemType.boot : 2,
      ItemType.bag : 2,
      ItemType.tea : 2,
      ItemType.coins : 2, }

  def check(self, item_type : ItemType):
    return self.items[item_type] > 0

  def take(self, item_type):
    if not self.check(item_type):
      raise ItemNotAvailableException()
    self.items[item_type] -= 1
    return True

class Clearing:

  CLEARING_PATHS_LOOKUP = {
    BoardType.Autumn : [
      [5,9,10], [5,6,10], [6,7,11], [8,9,12], [1,2], [2,3,11], [3,8,12],
      [4,7], [1,4,12], [1,2,12], [3,6,12], [4,7,9,10,11],],
    BoardType.Winter : [
      [5,10,11], [6,7,12], [7,8,12], [9,10,11], [1,6], [2,5], 
      [2,3], [3,9,12], [4,8,11], [1,4], [1,4,9], [2,3,8],],
    BoardType.Lake : [
      [5,9], [7,8,10], [8,9,12], [5,6], [1,4,11], [4,7,11],
      [2,6,10,11], [2,3,10], [1,3,12], [2,7,8], [5,6,7], [3,9],],
    BoardType.Mountain : [
      [8,9], [6,11], [6,11], [8,12], [10,11], [2,3], [12], [1,4],
      [1,10,12], [5,9,11], [2,3,10], [4,7,9,10],]}
  RIVER_PATHS_LOOKUP = {
    BoardType.Autumn : [
      [],[],[],[7],[10],[],[4,11],[],[],[5,11],[7,10],[],],
    BoardType.Winter : [
      [],[],[],[],[],[],[12],[],[],[11],[10,12],[11,7],],
    BoardType.Lake : [
      [10,11,12],[],[],[],[],[],[],[],[],[1,11,12],[1,10,12],[1,10,11],],
    BoardType.Moutain : [
      [],[10],[],[10],[],[],[],[],[],[2,4],[],[],]}
  HIDDEN_PATHS_MOUNTAIN = [
    [],[5],[7],[],[2,9],[11],[3],[9],[5,8],[],[6,12],[11],]
  BUILDING_SLOTS_LOOKUP = {
    BoardType.Autumn : [1,2,1,1,2,1.5,2,2,2,1.5,2.5,1.5],
    BoardType.Winter : [1,1,2,2,2,2,1,1.5,1.5,1,2.5,2.5],
    BoardType.Lake   : [2,1,1,1,2.5,2,1,1,1,2.5,2.5,2.5],
    BoardType.Moutain: [2,2,2,2,1,1,1,1,2.5,1.5,2.5,2.5],}

  def __init__(self, n:int, board_type:BoardType, suit:Suit):
    self.n = n
    self.paths = set(self.CLEARING_PATHS_LOOKUP[board_type][n])
    self.rivers = set(self.RIVER_PATHS_LOOKUP[board_type][n])
    self.building_slots = self.BUILDING_SLOTS_LOOKUP[board_type][n]
    if board_type == BoardType.Mountain:
      self.hidden = set(self.HIDDEN_PATHS_MOUNTAIN[n])

    self.buildings = []
    self.tokens = []
    self.warriors = []
    self.pawns = []

class Forest:

  FORESTS_LOOKUP = {
    BoardType.Autumn : [
      [1,2,5,10],[1,9,10,12],[2,6,10,11,12],[3,6,11],[3,7,11,12],[4,7,8,12],[4,9,12],],
    BoardType.Winter : [
      [1,2,5,6,11,12], [1,4,10,11],[2,3,7,12],[3,8,12],[4,9,11],[8,9,11,12]],
    BoardType.Lake : [
      [1,5,11],[1,9,12],[2,7,10],[2,8,10],[3,8,10,12],[3,9,12],[4,5,6,11],[6,7,11],[7,10,11]],
    BoardType.Mountain : [
      [1,8,9],[2,5,11],[2,6,11],[3,6,11],[3,7,11,12],[4,8,9,12],[5,9,10],[5,10,11],
      [9,10,12],[10,11,12],],}

  def __init__(self, verteces:Set[int], adjacent : Set[Forest]):
    self.verteces = verteces
    self.adjacent = adjacent
    
    self.pawns = []

  def init_forests(self, board_type):
    forests = [Forest(set(f)) for f in self.FORESTS_LOOKUP[board_type]]
    for forest in forests:
      for other_forest in forests:
        if len(forest.verteces & other_forest.verteces) >= 2:
          forest.adjacent.add(other_forest)
        if board_type == BoardType.Lake:
          lake_set = set([1,10,11,12])
          if (
            len(forest.verteces & lake_set) >= 2 and
            len(other_forest.verteces & lake_set) >= 2 and
            len(forest.verteces & other_forest.verteces) >= 1):
            forest.adjacent.add(other_forest)
    return forests

class Card:
  def __init__(self,

# BoardState
class BoardState:
  def __init__(self,
               board_type:BoardType,
               clearing_spec:List[Suit],
               deck_type:DeckType):
    (self.clearings, self.forests) = self.init_locations(board_type, clearing_spec)
    self.board_type = board_type
    
    self.deck_type = deck_type
    self.items = Items()

  def init_locations(self, board_type:BoardType, suits:List[Suit]):
    if board_type == BoardType.Autumn:
      suits = [Suit.F, Suit.M, Suit.R, Suit.R, Suit.R, Suit.F
               Suit.M, Suit.F, Suit.M, Suit.R, Suit.M, Suit.F]
    clearings = [
      Clearing(i, board_type, suits[i]) for i in range(1,len(suits)+1)
    ]





# FactionState
class FactionState:
    def __init__(self):
      self.hand : Dict[str, Card]

class MC_State(FactionState):
  def __init__(self, board_state:BoardType):
    self.board_state = board_state
    self.warrior_supply : int = 25

class ED_State(FactionState):
  pass

class WA_State(FactionState):
  pass

class VB_State(FactionState):
  pass

# RootState
class RootState:
  def __init__(self):
    self.board = BoardState()
    self.factions = {} # maps faction name to faction
