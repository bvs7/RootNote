# A file to create load and dump functions for all Root Types?

from .RootTypes import *
from .RootState import *

import sys
import inspect
import json



def RootObjectHook(d):
  if "__VEnum__" in d:
    return getattr(sys.modules[__name__],d["__VEnum__"])(d["value"])
  elif "__class__" in d:
    cls = getattr(sys.modules[__name__], d["__class__"])
    if cls == Board:
      d['paths'] = dict([(tuple([int(i) for i in k.split("-")]),v) for k,v in d['paths'].items()])
    if hasattr(cls, "_deserialize"):
      return cls._deserialize(**d)
    else:
      return cls(**d)
  return d

def RootDefault(obj):
  if isinstance(obj, VEnum):
    return {"__VEnum__":obj.__class__.__name__, "value":obj.name}
  if isinstance(obj, Deserializable):
    d = obj.__dict__.copy()
    if type(obj).__name__=="Board":
      # Deal with Paths!
      d['paths'] = dict([("-".join([str(i) for i in k]),v) for k,v in obj.paths.items()])
    return dict( d, __class__= obj.__class__.__name__)
  else:
    print(obj)
    raise TypeError("Object of type {} is not JSON serializable".format(obj.__class__.__name__))


dumps = json.dumps
dumps.__kwdefaults__['default'] = RootDefault
dump = json.dump
dump.__kwdefaults__['default'] = RootDefault
loads = json.loads
loads.__kwdefaults__["object_hook"] = RootObjectHook
load = json.load
load.__kwdefaults__["object_hook"] = RootObjectHook