from .BaseTypes import Faction, Factions, Building, Buildings, Token, Tokens

MC = Faction("MC")
Factions.append(MC)
  
Sawmill = Building("Sawmill", MC)
Workshop = Building("Workshop", MC)
Recruiter = Building("Recruiter", MC)
Buildings += [Sawmill, Workshop, Recruiter]

Keep = Token("Keep", MC)
Wood = Token("Wood", MC)
Tokens += [Keep, Wood]