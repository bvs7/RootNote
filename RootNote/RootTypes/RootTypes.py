from .BaseTypes import Faction, Factions, Building, Buildings, Token, Tokens

from .util import VEnum, auto

from .MC_Types import * # pylint: disable=unused-wildcard-import
from .ED_Types import * # pylint: disable=unused-wildcard-import
from .WA_Types import * # pylint: disable=unused-wildcard-import
from .VB_Types import * # pylint: disable=unused-wildcard-import

Faction = VEnum("Faction", Factions)

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

class ItemType(VEnum):
  sword = auto()
  crossbow = auto()
  hammer = auto()
  boot = auto()
  bag = auto()
  tea = auto()
  coin = auto()
  
class BoardType(VEnum):
  Autumn = auto()
  Winter = auto()
  Lake = auto()
  Mountain = auto()

class PathType(VEnum):
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
  def __init__(self, suit:Suit):
    self.suit = suit

