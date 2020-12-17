

import sys
import ply.yacc as yacc

from RootNoteLexer import tokens
from RootNote import *

"""
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
"""

def p_root_note(p):
  'root_note : draft setup play'
  p[0] = RootNote(p[1], p[2], p[3])

def p_draft(p):
  'draft : draft_pool_s board deck faction_choices_turn_order'
  p[0] = Draft(p[1], p[2], p[3], p[4])

def p_draft_pool_s(p):
  'draft_pool_s' : faction_list

def p_win(p):
  '''win : FACTION WINS faction_results
  '''
  p[0] = Win(p[1], p[3])

def p_faction_results(p):
  'faction_results : faction_results FACTION NUMBER'
  p[0] = p[1] + [(p[2],p[3])]

def p_faction_results_last(p):
  'faction_results : FACTION NUMBER'
  p[0] = [(p[1],p[2])]

parser = yacc.yacc(debug=True)

if __name__ == "__main__":
  filename = sys.argv[1]
  with open(filename) as f:
    data = f.read()
  print(parser.parse(data))
