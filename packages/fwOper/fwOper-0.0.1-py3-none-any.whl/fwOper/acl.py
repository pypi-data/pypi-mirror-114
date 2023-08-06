
# ----------------------------------------------------------------------------------------
from nettoolkit import *
from collections import OrderedDict
from copy import deepcopy

from .common import Plurals, Singulars
from .acg import OBJ
from .control import (
	network_group_member, port_group_member, 
	ANY, HOST, NETWORK, OBJ_GROUP, PORTS,
	)

# ----------------------------------------------------------------------------------------
# Local Functions
# ----------------------------------------------------------------------------------------
def access_list_list(config_list):
	"""extracts access-lists from provided configuration list ie.config_list.
	returns access-lists lines in a list
	"""
	return [line.rstrip() for line in config_list if line.startswith("access-list ")]


# ----------------------------------------------------------------------------------------
# Access Lists Entries
# ----------------------------------------------------------------------------------------
class ACLS(Plurals):
	"""collection of ACL objects

	:: Instance variables ::
	acls_list : access-lists in a list
	_repr_dic: access-lists (ACL)s  in a dictionary

	"""
	def __init__(self, config_list, objs=None):
		super().__init__()
		self.acls_list = access_list_list(config_list)
		self.set_acl_names()
		self.set_objects(objs)

	# ~~~~~~~~~~~~~~~~~~ CALLABLE ~~~~~~~~~~~~~~~~~~

	def add_str(self, n=0, seq=True):
		s = ''
		for acl_name, acl_obj in self._repr_dic.items():
			s += acl_obj.add_str(n, seq)
		return s

	def del_str(self, n=0, seq=True):
		s = ''
		for acl_name, acl_obj in self._repr_dic.items():
			s += acl_obj.del_str(n, seq)
		return s

	def set_acl_names(self):
		"""sets available access-lists names in _repr_dic (key) """
		for acl_line in self.acls_list:
			spl_acl_line = acl_line.split()
			acl_name = spl_acl_line[1]
			if acl_name not in self._repr_dic: self._repr_dic[acl_name] = []
			self._repr_dic[acl_name].append(acl_line)
		return self._repr_dic

	# def set_acl_objects(self, objs):
	def set_objects(self, objs):
		"""sets access-lists (ACL)s in _repr_dic (value) """
		for acl_name, acl_lines_list in self._repr_dic.items():
			acl =  ACL(acl_name, acl_lines_list)
			acl.parse(objs)
			self._repr_dic[acl_name] = acl

# ----------------------------------------------------------------------------------------
# Access List detail
# ----------------------------------------------------------------------------------------
class ACL(Singulars):
	"""Individual access-list object

	:: Instance variables ::
	acl_name:  access-list name
	acl_lines_list: access-list in list format
	_repr_dic: access-list details in a dictionary format key as acl line number, value as acl line attributes dictionary.

	:: Class variables ::
	end_point_identifiers_pos:  index of src, dst and port on acl line number
	mandatory_item_values_for_str: keys of acl lines

	:: Properties ::
	max: maximum line number on acl
	min: minimum line number on acl

	"""
	end_point_identifiers_pos = {	# static index points 
		0: 5,						# src
		1: 7,						# dst
		2: 9,						# port
	}
	mandatory_item_values_for_str = ('acl_type', 'action', 'protocol',
		'source', 'destination', 'ports', 'log_warning' )

	def __init__(self, acl_name, acl_lines_list):
		super().__init__(acl_name)
		self.acl_lines_list = acl_lines_list
		self._repr_dic = OrderedDict()
	def __iter__(self):
		for k, v in sorted(self._repr_dic.items()):
			yield (k, v)
	def __getitem__(self, item):
		try:
			return self._to_str(item)
		except KeyError:
			return None
	@property
	def max(self): return max(self._repr_dic.keys())
	@property
	def min(self): return min(self._repr_dic.keys())
	def __add__(self, attribs):  return self.copy_and_append(attribs)
	def __sub__(self, n):  return self.copy_and_delete(n)
	def __iadd__(self, n):
		if isinstance(n, ACL):
			if n._name == self._name:
				for k, v in n:
					if k in self._repr_dic: self.insert(k, v)
					else: self.append(v)
			else:
				raise Exception(f"ACLNAME-MISMATCHES-{n._name} v/s {self._name}")
		elif isinstance(n, dict):
			for k, v in n.items():
				if k in self._repr_dic: self.insert(k, v)
				else: self.append(v)
		else:
			raise Exception(f"Not-an-addablevalue {n}")
		return self
	def __isub__(self, n):
		if isinstance(n, int): 
			self.delete(n)
		elif isinstance(n, dict):
			mismatches = self.contains(n, True)
			for m in reversed(mismatches):
				self -= m
		else:
			raise Exception(f"Not-a-deletablevalue {n}")
		return self
	def __eq__(self, obj):
		for k, v in obj:
			if k in self._repr_dic and self._repr_dic[k] == v: continue
			else: return False
		return True
	def __gt__(self, obj):
		diffacl = ACL(self._name, None)
		for self_k, self_v in self._repr_dic.items():
			found = False
			for obj_k, obj_v in obj._repr_dic.items():
				found = self_v == obj_v
				if found: break
			if not found: diffacl[self_k] = self_v
		return diffacl
	def __lt__(self, obj):
		diffacl = ACL(self._name, None)
		for obj_k, obj_v in obj._repr_dic.items():
			found = False
			for self_k, self_v in self._repr_dic.items():
				found = self_v == obj_v
				if found: break
			if not found: diffacl[obj_k] = obj_v
		return diffacl
	def __contains__(self, item): return self.contains(item)
		
	# ~~~~~~~~~~~~~~~~~~~ EXTERNAL CALLABLES ~~~~~~~~~~~~~~~~~~~

	def has(self, item):
		for line_no, acl_details in  self:
			if not isinstance(acl_details, dict): continue
			acl_src = acl_details['source']
			acl_dst = acl_details['destination']
			acl_prt = acl_details['ports']
			if ((isinstance(acl_src, OBJ_GROUP) and acl_src.grp == item) 
				or (isinstance(acl_dst, OBJ_GROUP) and acl_dst.grp == item) 
				or (isinstance(acl_prt, OBJ_GROUP) and acl_prt.grp == item)
				):
				return line_no
		return False

	def contains(self, item, all=False):
		"""check matching attributes in acl object, 
		return matching acl line numbers list
		"""
		matching_lines = []
		for line_no, acl_details in  self:
			if isinstance(acl_details, dict):
				for k, v in item.items():
					if k == 'log_warning': continue
					if isinstance(acl_details[k], OBJ_GROUP) and isinstance(v, OBJ):
						if len(acl_details[k].grp > v): break
					elif acl_details[k] != v:
						break
				else:
					if not all: return line_no
					matching_lines.append(line_no)
		return matching_lines

	# do not return anything, instead alter actual acl
	def append(self, attribs):
		"""append a new acl line in acl object with provided attributes """
		mv = self._matching_value(attribs)
		if not mv:
			self[self.max+1] = attribs
		else:
			print(f"MatchingEntryAlreadyexistAtLine-{mv}")

	def copy_and_append(self, attribs):
		"""create duplicate of self, append a new acl line in new object with provided attributes """
		newobj = deepcopy(self)
		newobj.append(attribs)
		return newobj

	def delete(self, line_no): 
		"""delete a line in acl for given line number"""
		self._key_delete(line_no)
		self._key_deflate(line_no)

	def copy_and_delete(self, attribs):
		"""create duplicate of self, delete a line in new acl for given line number/attributes"""
		newobj = deepcopy(self)
		newobj -= attribs
		return newobj

	def insert(self, line_no, attribs):
		"""insert a new acl line in acl object with provided attributes 
		at given line number
		"""
		mv = self._matching_value(attribs)
		if not mv:
			self._key_extend(line_no)
			self[line_no] = attribs
		else:
			print(f"MatchingEntryAlreadyexistAtLine-{mv}")

	def copy_and_insert(self, line_no, attribs):
		"""create duplicate of self, insert a new acl line in new acl object,
		with provided attributes at given line number and return new updated object.
		existing object remains untouched
		"""
		newacl = deepcopy(self)
		newacl.insert(line_no, attribs)
		return newacl

	# returns string, do not alter actual acl
	def add_str(self, n=0, seq=True): 
		"""String representation of access-list line(n), (omit 'n' for full acl) """
		s = ''
		if n and isinstance(n, int): 
			return self._to_str(n, seq)
		elif n and isinstance(n, (list, tuple, set)):
			for i in n: s += self.add_str(i, seq)
		elif not n:
			for n, v in self: s += self.add_str(n, seq)
		return s

	# returns string, do not alter actual acl
	def del_str(self, n=0, seq=False): 
		"""negated string representation of access-list line(n), (omit 'n' for full acl) """
		s = ''
		if n and isinstance(n, int): 
			return "no " + self._to_str(n, seq)
		elif n and isinstance(n, (list, tuple, set)):
			for i in n: s += self.del_str(i, seq)
		elif not n:
			for n, v in self: s += self.del_str(n, seq)
		return s 

	# ~~~~~~~~~~~~~~~~~~~ INTERNALS ~~~~~~~~~~~~~~~~~~~

	def _matching_value(self, attribs):
		"""line number of acl for matching attributes """
		for line_no, acl_details in self:
			match = False
			for k_attr, v_attr in attribs.items():
				if isinstance(acl_details, ACL_REMARK): break
				match = acl_details[k_attr] == v_attr
				if not match: break
			if match: return line_no

	def _key_extend(self, n):
		"""supportive to insert a new line """
		rvs_keys = list(reversed(self._repr_dic.keys()))
		for key in rvs_keys:
			if key >= n: self[key+1] = self._repr_dic[key]
			else: break

	def _key_deflate(self, n): # Not in use currently
		"""supportive to delete a line (not in use), rearrange next lines """
		last_used_key = self.max
		# print(n, last_used_key)
		for key in range(n, last_used_key):
			self[key] = self[key+1]
		del(self._repr_dic[last_used_key])
		# print(self.max)

	def _key_delete(self, n):
		"""supportive to delete a line """
		try:
			del(self._repr_dic[n])
		except:
			print(f"NoDeletableEntryFoundForLine-{n}-orAlreadyRemoved")
			# raise Exception(f"NoDeletableEntryFoundForLine-{n}")

	def _to_str(self, n, seq=False):
		"""return String representation of access-list line(n) ( add/remove )
		seq=line number require or not in output (Boolean)
		"""
		item = self._repr_dic[n]
		if isinstance(item, dict):
			for v in self.mandatory_item_values_for_str:
				if v not in item:
					item[v] = self._normalize(v)
			log_warning = " log warning" if item['log_warning'] else ""
			seq_no = f"line {n} " if seq else ""
			# print(seq, seq_no)
			s = (f"access-list {self._name} {seq_no}"
				 f"{item['acl_type']} {item['action']} {item['protocol']} "
				 f"{item['source']} {item['destination']} {item['ports']}{log_warning}\n")
		else:
			s = item
		return s

	def _normalize(self, item):
		"""add default attribute and return to given item/attribute
		"""
		normalize_item_values = {
			'acl_type': 'extended', 
			# 'action': 'permit', 
			# 'protocol': 'tcp', 
			# 'source': , 
			# 'destination': , 
			# 'ports': , 
			'log_warning': True,
			}
		if normalize_item_values.get(item):
			return normalize_item_values[item]
		else:
			raise Exception(f"MissingMandatoryParameter-{item}, NormalizationNotAvailableForMandatoryField")

	# ~~~~~~ CALLABLE ~~~~~~~~~~~~~~~~~~~
	# USED WHILE INITIATLIZING
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	def parse(self, objs):
		"""parse access-list-lines-list and set _repr_dic.  
		objs requires for acl lines having object-group-names
		"""
		remark = None
		for line_no, line in enumerate(self.acl_lines_list):
			test = line.startswith("access-list al_from_blue extended deny tcp any4 any4 object-group INET-TCP-DROP")
			spl_line = line.split()
			# remarks line
			if spl_line[2] == 'remark':
				remark = " ".join(spl_line[3:])
				self._repr_dic[line_no] = ACL_REMARK(remark)
				continue
			# src /dst / ports
			idx_variance = 0
			protocol_variance = 1 if spl_line[4] == "object-group" else 0
			for k, v in self.end_point_identifiers_pos.items():
				pv = v+protocol_variance+idx_variance
				if k == 0: source      = network_group_member(spl_line, idx=pv, objectGroups=objs)
				if k == 1: destination = network_group_member(spl_line, idx=pv, objectGroups=objs)
				if k == 2: ports       = port_group_member(spl_line, idx=pv, objectGroups=objs)
				try:
					if spl_line[pv] in ANY: idx_variance -= 1
				except:
					pass
			# add rest statics and create ACL entry dict
			self._repr_dic[line_no] = {
				'remark': remark,
				'acl_type': spl_line[2],
				'action': spl_line[3],
				'protocol': spl_line[4+protocol_variance],
				'source': source,
				'destination': destination,
				'ports': ports,
				'log_warning': STR.found(line, 'log warnings'),
			}

# ----------------------------------------------------------------------------------------
# Access List Entry Candidates
# ----------------------------------------------------------------------------------------

class ACL_REMARK():
	"""ACL remark object
	:: Instance variables ::
	remark: acl remark ( returns as str of obj )
	"""
	def __init__(self, remark): self.remark = remark
	def __str__(self): return self.remark
	def __repr__(self): return self.remark
	def __eq__(self, obj): return str(obj) == str(self)


# ----------------------------------------------------------------------------------------
#   Main
# ----------------------------------------------------------------------------------------
if __name__ == '__main__':
	pass
# ----------------------------------------------------------------------------------------
