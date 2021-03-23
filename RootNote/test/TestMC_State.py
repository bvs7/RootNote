from .. import *
from ..Factions.MC_State import MC_State
from unittest import TestCase

class TestMC_State(TestCase):

  def test_play(self):
    pass

  def test_reachable_clearings(self):
    bs = BoardState()

    for c in bs.clearings:
      c.warriors.append(Faction.MC)
      self.assertEqual(c.rule(),Faction.MC)

    for c in [4,6,11,12]:
      bs.clearings[c].warriors.append(Faction.ED)

    mc = MC_State(bs)
    rc = mc.reachable_clearings(1)
    for i in [1,2,5,9,10]:
      self.assertIn(i, rc)
    for i in [3,4,6,7,8,11,12]:
      self.assertNotIn(i,rc)