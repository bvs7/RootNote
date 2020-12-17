# Parsing using a Lexer?...

tokens = [
  'CARD', 'NAME', 'NUMBER', 'EXHAUSTED', 'DOUBLE_WORD', 
  'POOL', 'BOARD', 'DECK', 'SETUP', 'FOREST', 'CRAFT', 
  'BATTLE', 'X', 'AMBUSH', 'REMOVE', 'HOSTILE', 'RECRUIT', 
  'MOVE', 'BUILD', 'DRAW', 'DISCARD', 'SPEND', 'MARCH', 'OVERWORK', 
  'DECREE', 'TURMOIL', 'SCORE', 'OUTRAGE', 'REVOLT', 'SPREAD', 
  'MOBILIZE', 'TRAIN', 'ORGANIZE', 'REFRESH', 'SLIP', 'DAMAGE', 
  'EXPLORE', 'AID', 'STRIKE', 'REPAIR', 'STEAL', 'HIDEOUT', 'WINS', 
  'PLACE_KEEP', 'PLACE_ROOST', 'CHOOSE_LEADER', 'DRAW_SUPPORTERS', 
  'CHOOSE_CHARACTER', 'REVEAL_QUEST', 'EMERGENCY_ORDERS', 'NEW_ROOST', 
  'IMPROVE_RELATIONS', 'DAY_LABOR', 'EVENINGS_REST', 'BUILDING', 
  'TOKEN', 'SUIT', 'FACTION', 'BOARD_TYPE', 'DECK_TYPE', 
  'LEADER_TYPE', 'VB_CHARACTER', 'ITEM', 'TO', 'FOR', 'FROM', 
  'WITH', 'IN', 'LEFT']


class Pattern:
  def __init__(self, tok_list):
    self.tok_list = tok_list

  def match(self, l):
    i = iter(l)
    for tok in self.tok_list:
      if not tok == next(i):
        return False