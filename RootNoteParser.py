

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
  'root_note : draft game_setup'# play'
  p[0] = RootNote(p[1], p[2])#, p[3])

def p_faction(p):
  '''faction : FACTION'''
  p[0] = Faction(p[1])

def p_faction_list(p):
  '''faction_list : faction_list faction
                  | empty'''
  if len(p) == 3:
    p[0] = p[1] + [p[2]]
  else:
    p[0] = []

def p_building(p):
  '''building : BUILDING'''
  p[0] = Building(p[1])

def p_name(p):
  '''name : NAME'''
  p[0] = Name(p[1])

def p_clearing(p):
  'clearing : NUMBER'
  p[0] = Clearing(p[1])

def p_forest(p):
  'forest : FOREST clearing_list'
  p[0] = Forest(p[1])

def p_clearing_list(p):
  '''clearing_list : clearing_list clearing 
                   | empty'''
  if len(p) == 3:
    p[0] = p[1] + [p[2]]
  else:
    p[0] = []

def p_item(p):
  ''' item : ITEM'''
  p[0] = Item(p[1])

def p_draft(p):
  'draft : draft_pool_s board deck turn_order'
  p[0] = Draft(p[1], p[2], p[3], p[4])

def p_draft_pool_s(p):
  '''draft_pool_s : draft_pool 
                  | empty'''
  if len(p) == 2:
    p[0] = p[1]
  else:
    p[0] = None

def p_board(p):
  '''board : BOARD board_type clearing_spec'''
  p[0] = Board(p[2], p[3])

def p_board_type(p):
  '''board_type : BOARD_TYPE'''
  p[0] = BoardType(p[1])

def p_clearing_spec(p):
  '''clearing_spec : suit_clearing_list'''
  p[0] = ClearingSpec(p[1])

def p_suit_clearing_list(p):
  '''suit_clearing_list : suit_clearing_list suit clearing
                        | empty'''
  if len(p) >= 4:
    p[0] = p[1] + [(p[2],p[3])]
  else:
    p[0] = []

def p_suit(p):
  '''suit : SUIT'''
  p[0] = Suit(p[1])

def p_deck(p):
  ''' deck : DECK DECK_TYPE '''
  p[0] = DeckType(p[2])

def p_turn_order(p):
  '''turn_order : turn_order faction name 
                | empty '''
  if len(p) > 3:
    p[0] = TurnOrder(p[1] + [(p[2],p[3])])
  else: # Last faction/name
    p[0] = []

def p_draft_pool(p):
  'draft_pool : POOL faction_list'
  p[0] = DraftPool(p[2])

def p_win(p):
  '''win : faction WINS faction_results
  '''
  p[0] = Win(p[1], p[3])

def p_faction_results(p):
  '''faction_results : faction_results faction NUMBER
                     | empty'''
  if len(p) == 4:
    p[0] = p[1] + [(p[2],p[3])]
  else:
    p[0] = []

def p_game_setup(p):
  '''game_setup : SETUP setup_list'''
  p[0] = p[2]

def p_setup_list(p):
  '''setup_list : setup_list setup
                | empty'''
  if len(p) >= 3:
    p[0] = p[1] + [p[2]]
  else:
    p[0] = []

def p_setup(p):
  '''setup : mc_setup
           | ed_setup
           | wa_setup
           | vb_setup'''
  p[0] = p[1]

def p_mc_setup(p):
  '''mc_setup : faction PLACE_KEEP IN clearing \
       mc_build mc_build mc_build'''
  assert(p[1] == 'MC')
  p[0] = MC_Setup(p[4], p[5:8])

def p_mc_build(p):
  '''mc_build : BUILD building IN clearing clearing_list'''
  p[0] = MC_Build(p[2], p[4], p[5])

def p_ed_setup(p):
  '''ed_setup : faction PLACE_ROOST IN clearing \
                ed_leader'''
  assert(p[1] == 'ED')
  p[0] = ED_Setup(p[4], p[5])

def p_ed_leader(p):
  '''ed_leader : CHOOSE_LEADER LEADER_TYPE'''
  p[0] = LeaderType(p[2])

def p_wa_setup(p):
  '''wa_setup : faction DRAW_SUPPORTERS'''
  p[0] = WA_Setup()

def p_vb_setup(p):
  '''vb_setup : faction vb_character forest reveal_quest_list'''
  p[0] = VB_Setup(p[2],p[3],p[4])

def p_vb_character(p):
  '''vb_character : CHOOSE_CHARACTER VB_CHARACTER'''
  p[0] = VB_Character(p[2])

def p_reveal_quest_list(p):
  '''reveal_quest_list : reveal_quest reveal_quest reveal_quest'''
  p[0] = p[1:4]

def p_reveal_quest(p):
  '''reveal_quest : REVEAL_QUEST quest'''
  p[0] = p[2]
  
def p_quest(p):
  '''quest : suit item item
           | name'''
  if len(p) == 2:
    p[0] = Quest.questFromName(p[1])
  else:
    p[0] = Quest(p[1],[p[2],p[3]])

def p_empty(p):
  'empty :'
  pass

parser = yacc.yacc(debug=True)

if __name__ == "__main__":
  filename = sys.argv[1]
  with open(filename) as f:
    data = f.read()
  print(parser.parse(data))
