from .BaseTypes import Faction, Factions, Building, Buildings, Token, Tokens

ED = Faction("ED")
Factions.append(ED)
  
Roost = Building("Roost", ED)

Buildings += [Roost]