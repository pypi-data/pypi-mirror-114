
# ----------------------------------------------------------------------------------------
from nettoolkit import *
from collections import OrderedDict
from copy import deepcopy

from .common import Plurals, Singulars
from .control import (
	network_group_member, port_group_member, icmp_group_member, group_object_member,
	protocol_group_member,
	network_member, port_member, 
	HOST, NETWORK, OBJ_GROUP, PORTS, update_ports_name, 
	ANY, VALID_MEMBER_TYPES,
	)

# ----------------------------------------------------------------------------------------
# Local Functions
# ----------------------------------------------------------------------------------------

def _object_group_list(config_list):
	"""extracts obect groups from provided configuration list ie.config_list 
	returns object groups (OBJ)s in a list"""
	obj_grp_list = []
	obj_group_started = False
	for line in config_list:
		spaces = STR.indention(line)
		if line.startswith("object-group"): 
			obj_group_started = True
			obj_grp_list.append(line.rstrip())
			continue
		if obj_group_started and spaces > 0:
			obj_grp_list.append(line.rstrip())
			continue
		if obj_group_started:
			break
	return obj_grp_list


def get_member_obj(member_type, member, objs):
	"""convert and provided string member to member object aka: HOST, NETWORK, OBJ_GROUP, PORTS based on its member-type provided.
	objs: requires for recursive lookup for OBJ_GROUP (if any)"""
	member_type_map = {
		'port-object': port_member,
		'network-object': network_member,
		'icmp-object': None,		# TBD
		'group-object': None,		# TBD
		'protocol-object': None,	# TBD
		# ... add more as need
	}
	if member_type not in member_type_map: 
		raise Exception(f"InvalidMemberTypeDefined-{member_type} for member-{member}")
	return member_type_map[member_type](member, objs)



# ----------------------------------------------------------------------------------------
# Collection of Object Group(s) objects
# ----------------------------------------------------------------------------------------
class OBJS(Plurals):
	"""collection of object groups """
	def __init__(self, config_list):
		super().__init__()
		self.obj_grps_list = _object_group_list(config_list)
		self._set_obj_grp_basics()
		self.set_objects()

	# ~~~~~~~~~~~~~~~~~~ CALLABLE ~~~~~~~~~~~~~~~~~~

	def get_matching_obj_grps(self, requests):
		"""matches provided (request members) in all object-groups available on device and 
		returns dictionary of object-group names. 
		where object-group matches same members in it.
		requests: list/set/tuple with members of dict, 
		         containing 'source', 'destination', 'ports' as keys.
		--> dict ( include all three, src, dest, port)
		"""
		candidates = {'source': [], 'destination': [], 'ports': []}
		group_names = {}
		if not isinstance(requests, (tuple, list, set)):
			raise Exception(f"NotValidRequestProvided-{requests}")
		for request in requests:
			for loc, member in candidates.items():
				if request[loc] in ANY: continue
				member.append(request[loc])
		for loc, member in candidates.items():
			obj_grps_list = self.matching_obj_grps(member)
			if obj_grps_list:
				group_names[loc] = obj_grps_list
		return group_names

	def matching_obj_grps(self, member):
		"""matches provided [members] in all object-groups available on device and 
		returns list of object-group names. 
		where object-group matches same members in it.
		member: list/set/tuple with members, 
		--> list ( singular )
		"""
		if isinstance(member, str):
			return [obj for name, obj in self if member in obj]
		elif isinstance(member, (tuple, list, set)):
			g = []
			for name, obj in self:
				match = False
				for m in member:
					match = m in obj
					if not match: break
				if match and len(obj) == len(member): g.append(obj)
			return g

	# ~~~~~~~~~~~~~~~~~~~ INTERNALS ~~~~~~~~~~~~~~~~~~~

	# set basic information of each object-group.
	def _set_obj_grp_basics(self):
		obj_grp_name = None
		for obj_grps_line in self.obj_grps_list:
			spaces = STR.indention(obj_grps_line)
			if spaces == 0:
				spl_obj_grps_line = obj_grps_line.split()
				obj_grp_type = spl_obj_grps_line[1]
				obj_grp_name = spl_obj_grps_line[2]
				if obj_grp_name not in self._repr_dic: self._repr_dic[obj_grp_name] = {}
				self._repr_dic[obj_grp_name]['type'] = obj_grp_type
				self._repr_dic[obj_grp_name]['candiates_list'] = []
				try:
					obj_grp_svc_filter = spl_obj_grps_line[3]
					self._repr_dic[obj_grp_name]['svc_filter'] = obj_grp_svc_filter
				except:
					self._repr_dic[obj_grp_name]['svc_filter'] = ""
			else:
				self._repr_dic[obj_grp_name]['candiates_list'].append(obj_grps_line)
		return self._repr_dic

	# set extended information of each object-group.
	def set_objects(self):
		h = 0
		for obj_grp_name, obj_grp_details in self._repr_dic.items():
			obj_grp = OBJ(obj_grp_name, h)
			obj_grp.set_instance_primary_details(obj_grp_details)
			obj_grp.parent = self
			obj_grp.parse()
			self._repr_dic[obj_grp_name] = obj_grp
			h += 1

# ----------------------------------------------------------------------------------------
# Object Group Detail
# ----------------------------------------------------------------------------------------
class OBJ(Singulars):
	"""Individual group object """

	# valid_member_types = VALID_MEMBER_TYPES

	def __init__(self, obj_grp_name, _hash):
		super().__init__(obj_grp_name)
		self.description = ""
		self._hash = _hash

	def __setitem__(self, key, value):  self._add(key, value)
	def __eq__(self, obj):  return not len([x for x in self > obj])
	def __len__(self): return self._len_of_members()
	def __contains__(self, member): return self.contains(member)
	def __add__(self, attribs): 
		newobj = deepcopy(self)
		newobj += attribs
		return newobj
	def __sub__(self, attribs): 
		newobj = deepcopy(self)
		newobj._delete(attribs)
		return newobj
	def __iadd__(self, n):
		if isinstance(n, dict):
			for k, v in n.items(): self[k] = v
		return self
	def __isub__(self, n): 
		self._delete(n)
		return self
	def __gt__(self, obj):
		diffs = self._missing(obj)
		obj_grp = self._blank_copy_of_self()
		obj_grp._repr_dic = diffs
		return obj_grp
	def __lt__(self, obj):
		diffs = obj._missing(self)
		obj_grp = self._blank_copy_of_self()
		obj_grp._repr_dic = diffs
		return obj_grp

	# ~~~~~~~~~~~~~~~~~~~ EXTERNAL CALLABLES ~~~~~~~~~~~~~~~~~~~

	def _len_of_members(self):
		l = 0
		for v in self._repr_dic.values():
			l += len(v)
		return l

	def contains(self, member, member_type=None):
		"""check member in object instance, if available or not;
		return member object if found
		"""
		if member_type is None: member_type = self._get_member_type(member)
		member_obj = get_member_obj(member_type, member, self.parent)
		if not self[member_type]: return None
		for _ in self[member_type]:
			if member_obj == _: 
				return _
			elif isinstance(_, OBJ_GROUP):
				if self.parent[_.group_name].contains(member, member_type):
					return _

	def add_str(self, header=True): 
		"""return String representation of object-group """
		return self._to_str(False, header)

	def del_str(self, header=False): 
		"""return String representation of object-group as if members need to remove """
		return self._to_str(True, header)

	# ~~~~~~~~~~~~~~~~~~~ INTERNALS ~~~~~~~~~~~~~~~~~~~

	# return String representation of object-group ( add/remove )
	def _to_str(self, negate, header):
		s = self._group_head() if header else ""
		for obj_grp_cand_type, candidates in self:
			for candidate in candidates:
				if negate: s += " no"
				s += f" {obj_grp_cand_type} {candidate}\n"
		return s

	# return String representation of object-group header/name line
	def _group_head(self):
		return (f"object-group {self.obj_grp_type} {self._name} {self.obj_grp_svc_filter}\n")
			
	# create and return a copy of original instance
	def _blank_copy_of_self(self):
		obj_grp = OBJ(self._name, self._hash*1)
		obj_grp.set_instance_primary_details(self.grp_details)
		return obj_grp

	# compare and return difference between parent instance,
	# provided obj/instance in dictionary format
	def _missing(self, obj):
		diffs = {}
		t = self.obj_grp_type == obj.obj_grp_type
		s = self.obj_grp_svc_filter == obj.obj_grp_svc_filter
		if not t or not s:
			# print("Mismatched-GroupType-or-ServiceFilter")
			return diffs

		for self_k, self_v in self._repr_dic.items():
			obj_v = obj[self_k]
			if obj_v is None:
				diffs[self_k] = self_v
			else:
				found = self_v == obj_v
				if found: continue
				diffs[self_k] = self_v.difference(obj_v)
		return diffs

	# supporting method for setting key/value for instance
	def _add(self, item_type, item):
			### ERRORS THERE, item mandatory,itemtype shold be optional, reevaluate
		if isinstance(item, (tuple, set, list)):
			for v in item:  self[item_type] = v
		elif isinstance(item, (str, int)):
			updated_item = self._get_item_object(item_type, item)
			self._obj_add(item_type, updated_item)
		elif isinstance(item, (HOST, NETWORK, OBJ_GROUP, PORTS)):
			self._obj_add(item_type, item)
		else:
			raise Exception(f"IncorrectIteminItemType-{item_type}/{item}")

	# supporting method for setting key/value for instance
	def _obj_add(self, item_type, item):
		try:
			self._repr_dic[item_type].add(item)
		except KeyError:
			self._repr_dic[item_type] = {item, }
		except:
			print(f"UnableToAdd- {item_type}:{item}")
			# raise Exception(f"UnableToAdd- {item_type}:{item}")

	# supporting method for removing key/value for instance ( reevaluation need)
	def _delete(self, item_type, item=''): 						### ERRORS THERE, item mandatory,itemtype shold be optional, reevaluate
		if isinstance(item_type, dict): 
			for k, v in item_type.items(): self._delete(k, v)
		elif isinstance(item, (tuple, set, list)):
			for _ in item: self._delete(item_type, _)
		elif isinstance(item, (str, int)):
			updated_item = self._get_item_object(item_type, item)
			self._obj_delete(item_type, updated_item)
		elif isinstance(item, (HOST, NETWORK, OBJ_GROUP, PORTS)):
			self._obj_delete(item_type, item)
		else:
			raise Exception(f"IncorrectIteminItemType-{item_type}/{item}")

	# supporting method for removing key/value for instance
	def _obj_delete(self, item_type, item):
		try:
			self._repr_dic[item_type].remove(item)
			if len(self._repr_dic[item_type]) == 0:
				del(self._repr_dic[item_type])
		except:
			print(f"NoValidCandidateFoundToRemove-{item_type}: {item}")			
			# raise Exception(f"NoValidCandidateFoundToRemove-{item_type}: {item}")

	# supporting method for retriving member-type/member pair for for a member
	def _get_item_object(self, item_type, item):
		spl_line = [item_type]
		spl_line.extend(item.split())
		updated_item = self._get_member(item_type, spl_line)
		return updated_item

	# supporting method for retriving member object for provided object-type 
	# ex: HOST, NETWORK…
	def _get_member(self, obj_type, spl_line):
		if obj_type == 'network-object':
			member = network_group_member(spl_line, 1, self.parent)
		elif obj_type == 'port-object':
			member = port_group_member(spl_line, 1, self.parent)
		elif obj_type == 'icmp-object':
			member = icmp_group_member(spl_line)
		elif obj_type == 'protocol-object':
			member = protocol_group_member(spl_line)
		elif obj_type == 'group-object':
			member = group_object_member(spl_line, self.parent)
		else:
			raise Exception(f"InvalidGroupMemberType-Noticed-[{obj_type}]\n{spl_line}")
		return member

	# dynamic detection of member-type for given member
	def _get_member_type(self, member):
		try:
			network_member(member, self.parent)
			return 'network-object'
		except:
			pass
		try:
			port_member(member, self.parent)
			return 'port-object'
		except:
			pass
		raise Exception(f"InvalidMemberFound:{member}, unable to generate member type for it.")

	# ~~~~~~ CALLABLE ~~~~~~~~~~~~~~~~~~~
	# USED WHILE INITIATLIZING
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	def set_instance_primary_details(self, obj_grp_details):
		"""set primary variable details of instance """
		self.obj_grp_lines_list = obj_grp_details['candiates_list']
		self.obj_grp_type = obj_grp_details['type']
		self.obj_grp_svc_filter = obj_grp_details['svc_filter']

	def parse(self):
		"""parse object-group-config-lines-list and set extended variables of instance """
		for line in self.obj_grp_lines_list:
			spl_line = line.lstrip().split()
			sub_obj_type = spl_line[0]
			if sub_obj_type == 'description':
				self.description = sub_obj_type
				continue
			member = self._get_member(spl_line[0], spl_line)
			if not self._repr_dic.get(spl_line[0]): self._repr_dic[spl_line[0]] = set()
			self._repr_dic[spl_line[0]].add(member)

	# ~~~~~~~~~~~~~~~~~~~ PROPERTIES ~~~~~~~~~~~~~~~~~~~

	@property
	def grp_details(self):
		"""object group details in dictionary (helpful in generating copy) """
		_grp_details = {
			'type': self.obj_grp_type,
			'svc_filter': self.obj_grp_svc_filter,
			'candiates_list': [],
		}
		return _grp_details
	


# ----------------------------------------------------------------------------------------
#   Main
# ----------------------------------------------------------------------------------------
if __name__ == '__main__':
	pass
# ----------------------------------------------------------------------------------------
