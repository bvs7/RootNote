from typing import NewType

# Create abstract class that collects instances of that class?


class Building(type):

  _list = None

  def __new__(cls, *args):
    print(cls, args)
    t = type.__new__(cls, *args)
    if not cls._list:
      cls._list = []
    cls._list.append(t)
    print(t, cls, cls._list)
    return t

  def A(self):
    print(self)

  @classmethod
  def C(cls):
    print(cls)

  @staticmethod
  def S():
    print("s")
  

class Token(type):
  pass

class Faction(type):
  pass
