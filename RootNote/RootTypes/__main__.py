from .RootTypes import * # pylint: disable=unused-wildcard-import
import traceback


while True:
  i = input("-> ")
  if i in "quit":
    break

  if i == "*":
    print(locals())
    continue
  
  try:
    print(locals()[i])
  except Exception as e:
    traceback.print_exc()