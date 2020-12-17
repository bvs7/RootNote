import fileinput

class Action:

  def to_log(self):
    raise NotImplementedError

class ReshuffleDiscardPile(Action):
  pass # TODO

class FactionWin(Action):
  pass # TODO

class RemoveBuilding(Action):
  pass # TODO

class Craft(Action):
  def __init__(self, card, faction):
    self.line = line
    self.faction = faction

class RootNoteAcceptor:

  def __init__(self):
    pass

  def accept(line):

if __name__ == "__main__":
