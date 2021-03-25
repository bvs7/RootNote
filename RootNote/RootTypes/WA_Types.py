from .BaseTypes import Faction, Factions, Building, Buildings, Token, Tokens

WA = Faction("WA")
Factions.append(WA)

FBase = Building("FBase", WA)
MBase = Building("MBase", WA)
RBase = Building("RBase", WA)

Buildings += [FBase, MBase, RBase]

Sympathy = Token("Sympathy", WA)
Tokens += [Sympathy]
