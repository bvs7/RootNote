from .Factions import *

def _is_Building(obj):
  return issubclass(type(obj), Building)

print(dir(MC_Building))
print(MC_Building.__dict__)
print(MC_Building.A(MC_Building))
print(MC_Building.C())

print("\n\n")
print(Sawmill)
print(dir(Sawmill))
print(Sawmill.__mro__)