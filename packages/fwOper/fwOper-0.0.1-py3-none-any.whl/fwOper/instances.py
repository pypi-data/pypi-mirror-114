
# ----------------------------------------------------------------------------------------
from .common import Plurals, Singulars, get_object
from .route import ROUTES
from .acl import ACLS
from .acg import OBJS

# ----------------------------------------------------------------------------------------
def _get_instances_lists_dict(config_list):
	"""creates and returns dictionary with list of configurations of sub-instances
	--> dict
	"""
	_instances_dict	= {}
	instance_name = None
	for line in config_list:
		if line.rstrip().endswith(" !!") and line.startswith("!! START"):
			instance_name = " ".join(line[3:-3].split()[1:])
			_instances_dict[instance_name] = []
			_instance_list = _instances_dict[instance_name]
		elif instance_name and line.rstrip().endswith(" !!") and line.startswith("!! END"):
			instance_name = None
		elif instance_name:
			_instance_list.append(line.rstrip())
	return _instances_dict

# ----------------------------------------------------------------------------------------
class INSTANCES(Plurals):
	"""firewall object with instances"""

	def __init__(self, config_list):
		self._repr_dic = _get_instances_lists_dict(config_list)
		if not self._repr_dic:
			self._repr_dic['system'] = config_list
		self.set_objects()

	# ~~~~~~~~~~~~~~~~~~~ EXTERNAL CALLABLES ~~~~~~~~~~~~~~~~~~~
	def set_objects(self):
		"""sets instances details"""
		for _name, lines_list in self._repr_dic.items():
			_instance =  INSTANCE(_name, lines_list)
			_instance.parse()
			self._repr_dic[_name] = _instance

# ----------------------------------------------------------------------------------------
class INSTANCE(Singulars):
	"""a single instance object on a firewall config"""

	def __init__(self, instance_name, instance_config_list):
		super().__init__(instance_name)
		self._repr_dic['conf_list'] = instance_config_list
		
	# ~~~~~~~~~~~~~~~~~~~ EXTERNAL CALLABLES ~~~~~~~~~~~~~~~~~~~
	def parse(self):
		"""parsing through config"""
		conf_list = self._repr_dic['conf_list']
		self['routes'] = get_object(ROUTES, conf_list=conf_list)
		self['obj_grps'] = get_object(OBJS, conf_list=conf_list)
		self['acls'] = get_object(ACLS, conf_list=conf_list, objs=self['obj_grps'])

# ----------------------------------------------------------------------------------------
