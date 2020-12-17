import ply.lex as lex

tokens = [
  'CARD','NAME','NUMBER','EXHAUSTED'
]

# Add reserved words!
reserved_words_list = (
  'Pool',
  'Board',
  'Deck',
  'Setup',
  'Place Keep', 'Place Roost', 'Choose Leader', 'Draw Supporters',
  'Choose Character', 'Forest', 'Reveal Quest',
  'Craft', 'Battle', 'X', 'Ambush', 'Remove', 'Hostile',
  'Recruit', 'Move', 'Build', 'Draw', 'Discard',
  'Spend', 'March', 'Overwork',
  'Emergency Orders','New Roost', 'Decree', 'Turmoil', 'Score',
  'Outrage','Revolt','Spread','Mobilize','Train','Organize',
  'Refresh','Slip','Damage','Explore','Aid','Improve Relations',
  'Strike','Repair','Steal','Day Labor','Hideout','Evenings Rest',
  'Wins',
)

reserved_types_list = {
  'BUILDING': ['sawmill','workshop','recruiter','base'],
  'TOKEN': ['wood','keep','sympathy'],
  'SUIT': ['M','F','R','B'],
  'FACTION': ['MC','ED','WA','VB'],
  'BOARD_TYPE': ['Autumn','Winter','Lake','Mountain'],
  'DECK_TYPE': ['Standard', 'E&P'],
  'LEADER_TYPE': ['Builder','Charismatic','Commander','Despot'],
  'VB_CHARACTER': ['Thief','Tinker','Ranger'],
  'ITEM': ['sword','torch','boot','crossbow','hammer','bag','tea','coins'],
}

helper_words_list = (
  'to','for','from','with','in','left',
)

reserved_words = {}
reserved_multiwords = {}
for word in reserved_words_list:
  breakdown = word.split()
  tok_name =word.replace(" ", "_").upper()
  if len(breakdown) == 1:
    reserved_words[word] = tok_name
  else:
    reserved_multiwords[word] = tok_name

helper_words = {}
for word in helper_words_list:
  helper_words[word] = word.upper()

tokens += reserved_words.values() 
tokens += reserved_multiwords.values()
tokens += reserved_types_list.keys()
tokens += helper_words.values()

def t_newline(t):
  r'\n+'
  t.lexer.lineno += len(t.value)

t_ignore = '[ \t,:+'

t_EXHAUSTED = r'\.'

def t_CARD(t):
  r'\{[.]\}'
  # TODO: check card validity, get other details of card
  return t

def t_NAME(t):
  r'"[^"\n]+"'
  t.value = t.value[1:-1]
  return t

def t_NUMBER(t):
  r'\d+'
  t.value = int(t.value)
  return t

def t_WORD(t):
  r'[a-zA-Z&\.]+'
  word = t.value
  for multiword in reserved_multiwords:
    if word == multiword[:len(word)]:
      # Check for multiword
      remaining_word = multiword[len(word):]
      test_word = t.lexer.lexdata[t.lexer.lexpos:t.lexer.lexpos+len(remaining_word)]
      if remaining_word == test_word:
        # Found multiword!
        t.type = reserved_multiwords[multiword]
        t.value = multiword
        t.lexer.skip(len(remaining_word))
        return t
  if word in reserved_words:
    t.type = reserved_words[word]
    return t
  if word.lower() in helper_words:
    t.type = helper_words[word.lower()]
    return t
  for category in reserved_types_list:
    if t.value in reserved_types_list[category]:
      t.type = category
      return t
  raise NotImplementedError("Unknown word: {}".format(word))

def t_error(t):
  print("Illegal character '%s'" % t.value[0])
  t.lexer.skip(1)

lexer = lex.lex(debug=True)

if __name__ == "__main__":
  lex.runmain()