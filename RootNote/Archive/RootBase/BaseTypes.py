from typing import NewType, List

# Create abstract class that collects instances of that class?

class Building(type):

  _list = []
  
  def __new__(cls, name, bases, classdict):
    t = super().__new__(cls, name, bases, classdict)
    cls._list.append(t)
    Building._list.append(t)
    return t

  