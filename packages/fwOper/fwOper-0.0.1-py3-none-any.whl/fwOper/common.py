
# ----------------------------------------------------------------------------------------
from abc import abstractclassmethod

# ----------------------------------------------------------------------------------------
# SHARED Functions
# ----------------------------------------------------------------------------------------
def get_object(obj, file=None, conf_list=None, **kwargs):
	"""Pre-defined set of steps to get objects. 
	( either input require file/conf_list ;  preferred conf_list )"""
	if file is not None:
		with open(file, 'r') as f:
			conf_list = f.readlines()
	objs = obj(conf_list, **kwargs)
	if conf_list: return objs
	raise Exception("MissingMandatoryInput(AtleastOneRequire {file/conf_list})")


# ----------------------------------------------------------------------------------------
# SHARED Classes
# ----------------------------------------------------------------------------------------
class Common():
	"""Commons methods of object/objects"""		
	def __init__(self): self._repr_dic = {}
	def __iter__(self):
		for k, v in self._repr_dic.items():
			yield (k, v)
	def __getitem__(self, item): 
		return self._repr_dic[item]# if self._repr_dic.get(item) else None
	def __getattr__(self, attr): return self[attr]
	def __repr__(self): return f'{self.__class__.__name__}[{self._name}]'
	def keys(self): return self._repr_dic.keys()
	def values(self): return self._repr_dic.values()

# ----------------------------------------------------------------------------------------
class Plurals(Common):
	"""collection of objects """		
	@abstractclassmethod
	def set_objects(self): pass

# ----------------------------------------------------------------------------------------
class Singulars(Common):
	"""One of object """		
	def __init__(self, name=''):
		super().__init__()
		self._name = name
	def __setitem__(self, key, value):  self._repr_dic[key] = value
	def __len__(self):  return len(self._repr_dic.keys())
	@abstractclassmethod
	def parse(self): pass

# ----------------------------------------------------------------------------------------
