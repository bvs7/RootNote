from ...util import VEnum, auto

from ..BaseTypes import *

# What behavior do we want?

# Strict "Building" Typing.
# Building is a type.
# Strict types of Buildings. (sm, ws, rec, roost, m_base, r_base, f_base, etc)
# Global access to types of buildings?
# Sawmill is a reference to the Sawmill type
# no instances? Sawmill == Sawmill no matter what. 
# Multiple sm in one clearing will be listed twice. in a list or multiset

# So, issubtype(Sawmill, Building)?
# Not, isisnstance(Sawmill, Building)?
# Or, Building is a subclass of type?

# Desired operations:

# x is a Building (type) -> bool

# x is a MC Building (type) -> bool

# x is a Sawmill (type) -> bool

# find every clearing with an x (type of Building)

# Require an input param to be a building
# Require an input param to be a MC building?

# So, Building is a type. MC_Building is a type that is a subtype of Building
# Sawmill is an instance of MC_Building
# isinstance(Sawmill, Building) -> True
# isinstance(Sawmill, MC_Building) -> True

# or, initialize buildings and move them around? interesting... no

class MC_Building(Building):
  pass

Sawmill = MC_Building("Sawmill", (), {})
Workshop = MC_Building("Workshop", (), {})
Recruiter = MC_Building("Recruiter", (), {})

class ED_Building(Building):
  pass
Roost = ED_Building("Roost", (), {})