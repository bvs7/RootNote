from ..RootState import *
from unittest import TestCase

class TestBoardState(TestCase):

  def test_init(self):
    bs = BoardState()
    bs.items[ItemType.sword] -= 1
    self.assertEqual(bs.items[ItemType.sword], 1)

    bs2 = BoardState()
    self.assertEqual(bs2.items['sword'],2)

    self.assertEqual(bs.paths['1-5'],Path.PATH)
    self.assertIn("4-9-12", bs.forests)

    self.assertIsNone(bs.clearings[12].rule())

    bs.clearings[1].warriors.append(Faction.MC)
    bs.clearings[2].warriors.append(Faction.MC)
    bs.clearings[2].warriors.append(Faction.ED)
    bs.clearings[3].warriors.append(Faction.MC)
    bs.clearings[3].warriors.append(Faction.MC)
    bs.clearings[3].warriors.append(Faction.ED)

    self.assertEqual(bs.clearings[1].rule(),Faction.MC)
    self.assertEqual(bs.clearings[2].rule(),Faction.ED)
    self.assertEqual(bs.clearings[3].rule(),Faction.MC)

    bs.clearings[3].warriors.extend([Faction.WA]*2)
    
    self.assertEqual(bs.clearings[3].rule(),None)

    bs.clearings[3].buildings.append(Building.roost)
    self.assertEqual(bs.clearings[3].rule(),Faction.ED)

    bs.clearings[2].buildings.append(Building.sawmill)
    self.assertEqual(bs.clearings[2].rule(),Faction.MC)
    
    bs.clearings[2].buildings.append(Building.sawmill)
    bs.clearings[2].warriors.append(Faction.ED)
    self.assertEqual(bs.clearings[2].rule(),Faction.MC)


  def test_suits(self):
    self.assertTrue(Suit.M <= Suit.B)
    self.assertTrue(Suit.B <= Suit.B)
    self.assertTrue(Suit.F <= Suit.F)
    self.assertFalse(Suit.B <= Suit.F)
    self.assertTrue(Suit.B >= Suit.M)
    self.assertFalse(Suit.M >= Suit.F)
    self.assertTrue(Suit.M == "M")
    self.assertFalse(Suit.F == "B")
    self.assertTrue(Suit.F <= "B")
    self.assertTrue(Suit.B >= "F")
    self.assertTrue(Suit.B > Suit.F)
    self.assertFalse(Suit.F < Suit.M)
  
  def test_pieces(self):
    sm = Building.sawmill
    self.assertTrue(sm.faction == Faction.MC)

  def test_item(self):
    i = Item(ItemType.sword)
