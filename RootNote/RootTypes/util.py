from enum import Enum, EnumMeta

class VEnumMeta(EnumMeta):
  def __call__(cls, value, names=None, *, module=None, qualname=None, type=None, start=None):
    vnames = None
    if names is None:
      return getattr(cls,value)
    if isinstance(names, str):
      vnames = names.replace(',', ' ').split()
      vnames = [(name,name) for name in vnames]
    if isinstance(names, (tuple,list)) and names and isinstance(names[0],str):
      #iterable of str
      vnames = [(name,name) for name in names]
    if not vnames: # wasn't one of the above types
      for item in names:
        if isinstance(item,str):
          vnames.append((item,item))
        else: # tuple list of name, value
          vnames.append((item[0],item[0]))
    return super().__call__(value,vnames,module=module,qualname=qualname,type=type,start=start)

  def __contains__(cls, item):
    item = cls.__call__(item) # pylint: disable=no-value-for-parameter
    return item.name in cls._member_map_

  def __repr__(cls):
    return "<{}:[{}]>".format(cls.__name__, ",".join(cls._member_map_.keys()))

class VEnum2(Enum, metaclass=VEnumMeta):

  def __init__(self, *args, **kwargs):
    print(args,kwargs)

  def __repr__(self):
    return "<%s.%s>" % (self.__class__.__name__, self.name)
  
  def __eq__(self, other):
    if isinstance(other, str):
      return self.name == other
    if isinstance(other, self.__class__):
      return self.name == other.name
    return False

  def __hash__(self):
    return hash(self.name)

class OrderedVEnum(VEnum2):
  def __lt__(self, other):
    other = self.__class__(other)
    l = list(self.__class__)
    return l.index(self) < l.index(other)

  def __le__(self,other):
    return self == other or self < other

# defined with dynamic getattr to prevent pylint errors

class auto:
  def __getattr__(self, name):
    return self.__getattribute__(name)

class MetaStr(type):
  def __new__(cls, name, bases, classdict):
    return super().__new__(cls, name,bases,classdict)
  
  def __iter__(cls):
    return iter([k for k in cls.__dict__ if not k[0:2] == "__"])

  def __contains__(cls, key):
    return key in cls.__dict__

class VEnum(str, metaclass = MetaStr):
  def __init__(self, value):
    if value in self.__dict__:
      super().__init__(self.__getattribute__(value))
    else:
      raise TypeError(type(self).__name__ + ": " + value)
