from ..RootState import RootState, RootTypes
from ..RootState.Factions.MC_State import MC_State
from unittest import TestCase

class TestMC_State(TestCase):

  def test_play(self):
    pass

  def test_reachable_clearings(self):
    board = RootState.Board()

    for c in board.clearings:
      c.warriors[RootTypes.Faction.MC] = 1
      self.assertEqual(c.rule(),RootTypes.Faction.MC)

    for c in [4,6,11,12]:
      board[c].warriors[RootTypes.Faction.ED] = 1

    mc = MC_State(board)
    rc = mc.reachable_clearings(1)
    for i in [1,2,5,9,10]:
      self.assertIn(i, rc)
    for i in [3,4,6,7,8,11,12]:
      self.assertNotIn(i,rc)