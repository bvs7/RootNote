

from typing import NewType, List, Tuple

from enum import Enum,auto

Name = NewType('Name', str)
Suit = NewType('Suit',str)
Clearing = NewType('Clearing', int)
Forest = NewType('Forest', List[Clearing])
Item = NewType('Item', str)
ClearingSpec = NewType('ClearingSpec', List[Tuple[Suit,Clearing]])
Building = NewType('Building', str)
LeaderType = NewType('LeaderType',str)
VB_Character = NewType('VB_Character',str)

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


DraftPool = NewType('DraftPool', List[Faction])
TurnOrder = NewType('TurnOrder',List[Tuple[Faction, Name]])

class RootObj:
  def __repr__(self):
    return f"\n{type(self).__name__}:{self.__dict__}\n/{type(self).__name__}"

class Win(RootObj):
  def __init__(self,winner, results):
    self.winner = winner
    self.results = results

class Build(RootObj):
  pass

class Setup(RootObj):
  pass

class MC_Build(Build):
  def __init__(self, building:Building, clearing:Clearing, wood_sources=[]):
    self.building = building
    self.clearing = clearing
    self.wood_sources = wood_sources

class MC_Setup(Setup):
  def __init__(self, keep_clearing:Clearing, builds:MC_Build):
    self.keep_clearing = keep_clearing
    self.builds = builds

class ED_Setup(Setup):
  def __init__(self, roost_clearing:Clearing, leader:LeaderType):
    self.roost_clearing = roost_clearing
    self.leader = leader

class WA_Setup(Setup):
  def __init__(self):
    pass

class VB_Setup(Setup):
  def __init__(self, vb_character:VB_Character, forest:Forest, start_quests):
    self.vb_character = vb_character
    self.forest = forest
    self.start_quests = start_quests

class Quest(RootObj):
  def __init__(self, suit, items):
    self.suit = suit
    self.items = items
  @staticmethod
  def questFromName(name): # TODO
    return Quest(None, [None,None])


class Board(RootObj):
  def __init__(self,board_type : BoardType, 
                    clearing_spec:ClearingSpec = []):
    self.board_type = board_type
    if self.board_type == BoardType.Autumn:
      self.clearing_spec = ClearingSpec([
      ('f',1),('m',2),('r',3),('r',4),('r',5),('f',6),
      ('m',7),('f',8),('m',9),('r',10),('m',11),('f',12) ])
    else:
      self.clearing_spec = clearing_spec

class Deck(RootObj):
  def __init__(self, deck_type:DeckType):
    self.deck_type = deck_type

class Draft(RootObj):
  def __init__(self, draft_pool:DraftPool, 
                     board:Board, deck:DeckType, 
                     turn_order:TurnOrder):
    self.draft_pool = draft_pool
    self.board = board
    self.deck = deck
    self.turn_order = turn_order

class RootNote(RootObj):
  def __init__(self, draft:Draft,setups:List[Setup]):
    self.draft = draft
    self.setups = setups
    # self.play = play
