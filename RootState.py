from typing import NewType, List, Set, Dict, Optional, Union
from venum import VEnum, OrderedVEnum, auto
from dataclasses import dataclass

import json

Suit = VEnum('Suit', 'M F R B')
Faction = VEnum('Faction', 'MC ED WA VB V2 LC RC UD CC') # TODO: support other forms? (C, E, A, V, L, O, M/D, ?)
Building = VEnum('Building', 'sawmill workshop recruiter roost base')
Token = VEnum('Token', 'keep wood sympathy')
Leader = VEnum('Leader', 'Builder Charismatic Commander Despot')
ItemType = VEnum('ItemType', 'sword crossbow hammer boot bag tea coin')
@dataclass
class Item:
  t : ItemType
  ex : bool = True
Relation = OrderedVEnum("Relation",'Hostile Indifferent Favorable Cordial Allied')
Board = VEnum('Board', 'Autumn Winter Lake Mountain')
PathType = VEnum('PathType','PATH RIVER CLOSED')
Deck = VEnum("Deck", 'Standard E_P')


class RootException(Exception):
  pass




class Clearing:

  CLEARING_PATHS_LOOKUP = {
    Board.Autumn : [
      [5,9,10], [5,6,10], [6,7,11], [8,9,12], [1,2], [2,3,11], [3,8,12],
      [4,7], [1,4,12], [1,2,12], [3,6,12], [4,7,9,10,11],],
    Board.Winter : [
      [5,10,11], [6,7,12], [7,8,12], [9,10,11], [1,6], [2,5], 
      [2,3], [3,9,12], [4,8,11], [1,4], [1,4,9], [2,3,8],],
    Board.Lake : [
      [5,9], [7,8,10], [8,9,12], [5,6], [1,4,11], [4,7,11],
      [2,6,10,11], [2,3,10], [1,3,12], [2,7,8], [5,6,7], [3,9],],
    Board.Mountain : [
      [8,9], [6,11], [6,11], [8,12], [10,11], [2,3], [12], [1,4],
      [1,10,12], [5,9,11], [2,3,10], [4,7,9,10],]}
  RIVER_PATHS_LOOKUP = {
    Board.Autumn : [
      [],[],[],[7],[10],[],[4,11],[],[],[5,11],[7,10],[],],
    Board.Winter : [
      [],[],[],[],[],[],[12],[],[],[11],[10,12],[11,7],],
    Board.Lake : [
      [10,11,12],[],[],[],[],[],[],[],[],[1,11,12],[1,10,12],[1,10,11],],
    Board.Mountain : [
      [],[10],[],[10],[],[],[],[],[],[2,4],[],[],]}
  HIDDEN_PATHS_MOUNTAIN = [
    [],[5],[7],[],[2,9],[11],[3],[9],[5,8],[],[6,12],[11],]
  BUILDING_SLOTS_LOOKUP = {
    Board.Autumn : [1,2,1,1,2,1.5,2,2,2,1.5,2.5,1.5],
    Board.Winter : [1,1,2,2,2,2,1,1.5,1.5,1,2.5,2.5],
    Board.Lake   : [2,1,1,1,2.5,2,1,1,1,2.5,2.5,2.5],
    Board.Mountain: [2,2,2,2,1,1,1,1,2.5,1.5,2.5,2.5],}

  def __init__(self, n:int, board_type:Board, suit:Suit):
    self.n = n
    self.paths = set(self.CLEARING_PATHS_LOOKUP[board_type][n])
    self.rivers = set(self.RIVER_PATHS_LOOKUP[board_type][n])
    self.building_slots = self.BUILDING_SLOTS_LOOKUP[board_type][n]
    if board_type == Board.Mountain:
      self.hidden = set(self.HIDDEN_PATHS_MOUNTAIN[n])

    self.buildings : List[Building]= []
    self.tokens : List[Token] = []
    self.warriors : List[Faction] = []
    self.pawns : List[Faction] = []

paths = Clearing.CLEARING_PATHS_LOOKUP[Board.Autumn]
d = {}
for i in range(len(paths)):
  c = i + 1
  for j in range(len(paths[i])):
    o = paths[i][j]
    s = {c,o}
    d["%d-%d" % tuple(sorted(s))] = PathType.PATH

rivers = Clearing.RIVER_PATHS_LOOKUP[Board.Autumn]
for i in range(len(rivers)):
  c = i + 1
  for j in range(len(rivers[i])):
    o = rivers[i][j]
    s = {c,o}
    l = sorted(s)
    d["%d-%d" % (l[0],l[1])] = PathType.RIVER

# rivers = Clearing.RIVER_PATHS_LOOKUP[Board.Autumn]
# for i in range(len(rivers)):
#   c = i + 1
#   for j in range(len(rivers[i])):
#     o = rivers[i][j]
#     s = {c,o}
#     d["%d-%d" % sorted(s)] = PathType.RIVER

class Forest:

  FORESTS_LOOKUP = {
    Board.Autumn : [
      [1,2,5,10],[1,9,10,12],[2,6,10,11,12],[3,6,11],[3,7,11,12],[4,7,8,12],[4,9,12],],
    Board.Winter : [
      [1,2,5,6,11,12], [1,4,10,11],[2,3,7,12],[3,8,12],[4,9,11],[8,9,11,12]],
    Board.Lake : [
      [1,5,11],[1,9,12],[2,7,10],[2,8,10],[3,8,10,12],[3,9,12],[4,5,6,11],[6,7,11],[7,10,11]],
    Board.Mountain : [
      [1,8,9],[2,5,11],[2,6,11],[3,6,11],[3,7,11,12],[4,8,9,12],[5,9,10],[5,10,11],
      [9,10,12],[10,11,12],],}

  def __init__(self, verteces:Set[int]):
    self.verteces = verteces
    self.adjacent = set()
    
    self.pawns = []

  @staticmethod
  def init_forests(board_type):
    forests = [Forest(set(f)) for f in Forest.FORESTS_LOOKUP[board_type]]
    for forest in forests:
      for other_forest in forests:
        if len(forest.verteces & other_forest.verteces) >= 2:
          forest.adjacent.add(other_forest)
        if board_type == Board.Lake:
          lake_set = set([1,10,11,12])
          if (
            len(forest.verteces & lake_set) >= 2 and
            len(other_forest.verteces & lake_set) >= 2 and
            len(forest.verteces & other_forest.verteces) >= 1):
            forest.adjacent.add(other_forest)
    return forests

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




# BoardState
class BoardState:
  def __init__(self,
               board_type:Board,
               clearing_spec:List[Suit],
               deck_type:Deck):
    (self.clearings, self.forests) = self.init_locations(board_type, clearing_spec)
    self.board_type = board_type
    
    self.deck = Deck(deck_type)
    self.deck_type = deck_type
    self.items = {} # TODO starting items

  def init_locations(self, board_type:Board, suits:List[Suit]):
    if board_type == Board.Autumn:
      suits = [Suit.F, Suit.M, Suit.R, Suit.R, Suit.R, Suit.F,
               Suit.M, Suit.F, Suit.M, Suit.R, Suit.M, Suit.F]
    clearings = [
      Clearing(i, board_type, suits[i]) for i in range(1,len(suits)+1)]
    forests = Forest.init_forests(board_type)
    return (clearings, forests)

Victory = NewType("Victory", Union[int,Suit,Faction])

# FactionState
class FactionState:
  pass

class Track:
  def __init__(self, limit:int, start:int):
    self.limit = limit
    self.n = start

  def use(self):
    self.n -= 1
    assert self.n >= 0
    if 'points' in self.__dict__:
      return self.__dict__['points'][self.limit-self.n-1]

  def ret(self):
    self.n += 1
    assert self.n <= self.limit

  def get(self, name): # TODO safety?
    return self.__dict__[name][self.limit - self.n]

class MC_Track(Track):
  def __init__(self, building:Building):
    super().__init__(6,6)
    self.building = building
    self.costs = [0,1,2,3,3,4]
    if building == Building.sawmill:
      self.points = [0,1,2,3,3,4]
    elif building == Building.workshop:
      self.points = [0,2,2,3,4,5]
    elif building == Building.recruiter:
      self.points = [0,1,2,3,4,5]
      self.card_draw = [1,1,2,2,3,3]

class MC_State(FactionState):
  def __init__(self, board_state:Board):
    self.board_state = board_state
    self.warrior_supply : int = 25
    self.wood = 8
    self.hand = 0
    self.tracks = {
      Building.sawmill : MC_Track(Building.sawmill),
      Building.workshop: MC_Track(Building.workshop),
      Building.recruiter : MC_Track(Building.recruiter),
    }
    self.crafted_items : List[Item] = []
    self.crafted_improvements : List[Card] = []
    self.vp : Victory = 0

class Decree:
  def __init__(self):
    self.recruit :List[Suit] = []
    self.move : List[Suit] = []
    self.battle : List[Suit] = []
    self.build : List[Suit] = []
    self.cards : List[Card] = []

class RoostTrack(Track):
  def __init__(self):
    super().__init__(7,7)
    self.score = [0,1,2,3,4,4,5]
    self.card_draw = [1,1,2,2,2,3,3]

class ED_State(FactionState):
  def __init__(self, board_state:Board):
    self.board_state = board_state
    self.warrior_supply : int = 20
    self.hand = 0
    self.decree = Decree()
    self.leader : Optional[Leader] = None
    self.roost_track = RoostTrack()
    self.crafted_items : List[Item] = []
    self.crafted_improvements : List[Card] = []
    self.vp : Victory = 0

class SympathyTrack(Track):
  def __init__(self):
    super().__init__(10,10)
    self.points = [0,1,1,1,2,2,3,4,4,4]
    self.cost = [1,1,1,2,2,2,3,3,3,3]

class WA_State(FactionState):
  def __init__(self, board_state:Board):
    self.board_state = board_state
    self.warrior_supply : int = 10
    self.officers : int = 0
    self.bases : Set[Suit] = set(Suit.M, Suit.F, Suit.R)
    self.card_draw = [1,2,3,4]
    self.hand = 0
    self.crafted_items : List[Item] = []
    self.crafted_improvements : List[Card] = []
    self.vp : Victory = 0

class TeaTrack(Track):
  def __init__(self):
    super().__init__(3,0)
    self.refresh = [3,5,7,9]

class CoinTrack(Track):
  def __init__(self):
    super().__init__(3,0)
    self.card_draw = [1,2,3,4]

class BagTrack(Track):
  def __init__(self):
    super().__init__(3,0)
    self.storage = [6,8,10,12]

class Satchel:
  def __init__(self):
    self.items : List[Item]
    self.broken : List[Item]

class VB_State(FactionState):
  def __init__(self, board_state:Board):
    self.board_state = board_state
    self.hand = 0
    self.tea_track = TeaTrack()
    self.coin_track = CoinTrack()
    self.bag_track = BagTrack()
    self.satchel = Satchel()
    self.relationships : Dict[Faction,Relation] = {}
    self.crafted_improvements : List[Card] = []
    self.vp : Victory = 0

# RootState
class RootState:
  def __init__(self):
    self.board = None
    self.factions = {} # maps faction name to faction
