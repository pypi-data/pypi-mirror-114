
# ----------------------------------------------------------------------------------------
from nettoolkit import *

# ----------------------------------------------------------------------------------------
# Static / Universal Variables
# ----------------------------------------------------------------------------------------
ADD = 'add'			# request types
DEL = 'del'
ANY = ('any', 'any4', 'any6')
ICMP = ('echo', 'echo-reply')
DEFAULT_ROUTE = ("0.0.0.0", "0.0.0.0")
any4 = '0.0.0.0 0.0.0.0'
PORT_MAPPINGS = {
	'7': 'echo', 
	'22': 'ssh', 
	'23': 'telnet', 
	'80': 'www', 
	'443': 'https', 
}
VALID_PROTOCOLS = ('tcp', 'udp', 'icmp', 'ip', 'scp')
VALID_MEMBER_TYPES = ('network-object', 'port-object', 'icmp-object', 'group-object', 
	'protocol-object')

# ----------------------------------------------------------------------------------------
# Control Functions
# ----------------------------------------------------------------------------------------
def network_group_member(spl_line, idx, objectGroups=None):
	"""returns Network group member object from given splitted line, 
	provide index to look at, 
	objectGroups will require if splitted line has object-group.
	"""
	if spl_line[idx] == 'host':
		return HOST(spl_line[idx+1])
	elif spl_line[idx] == 'object-group':
		try:
			return OBJ_GROUP(spl_line[idx+1], objectGroups)		## TBD pass objectGroups
		except:
			return None
	elif spl_line[idx] in ANY:
		return NETWORK(*DEFAULT_ROUTE)
	else: 
		ao = addressing(spl_line[idx])
		if type(ao) == IPv6: return NETWORK(spl_line[idx])
		if type(ao) == IPv4: return NETWORK(spl_line[idx], spl_line[idx+1])
	raise Exception(f"UndefinedEndPointTypeDetected: {spl_line}\n{idx}")

def port_group_member(spl_line, idx, objectGroups=None):
	"""returns Port group member object from given splitted line, 
	provide index to look at, 
	objectGroups will require if splitted line has object-group.
	"""
	try: spl_line[idx]
	except: return ''
	if 4 < len(spl_line) <= 8:
		pts = PORTS("", "")
	elif spl_line[idx] == 'eq':
		pts = PORTS(spl_line[idx], spl_line[idx+1])
	elif spl_line[idx] =='range':
		pts = PORTS(spl_line[idx], spl_line[idx+1], spl_line[idx+2])
	elif spl_line[idx] == 'object-group':
		try:
			pts = OBJ_GROUP(spl_line[idx+1], objectGroups)
		except:
			pts = None
			pass													### bypassed temporily
	elif spl_line[idx] in ICMP:
		pts = PORTS("", spl_line[idx])
	elif spl_line[4] == 'icmp':				### Exceptional match for missing icmp ports
		pts = PORTS("", 'echo')				  # define port as echo in this case
	elif spl_line[idx] == 'log':
		return ''
	else:
		raise Exception(f"UndefinedPort/TypeDetected: {spl_line} at index {idx}")
	return pts

def icmp_group_member(spl_line):
	pts = Icmp(spl_line[-1])
	return pts

def protocol_group_member(spl_line):
	pts = PROTOCOL(spl_line[-1])
	return pts

def group_object_member(spl_line, objectGroups=None):
	try:
		pts = OBJ_GROUP(spl_line[-1], objectGroups)
	except:
		pts = None	
	return pts


def network_member(network, objs=None):
	"""returns Network group member object for given network, 
	objs will require if network has object-group.
	"""
	if not isinstance(network, str): return network	
	# ----------------------------------------------------
	network = network.strip()
	# ----------------------------------------------------
	if network in ANY: return NETWORK(*DEFAULT_ROUTE)
	# ----------------------------------------------------
	spl_network = network.split("/")
	net_obj = None
	if len(spl_network) == 2:
		net_obj = addressing(network)
		if net_obj:
			mask = int(spl_network[1]) 
			if mask == 32: return HOST(spl_network[0])
			return NETWORK(spl_network[0], bin_mask(mask))
	# ----------------------------------------------------
	spl_network = network.split(" ")
	if len(spl_network) == 2:
		if spl_network[0] == 'object-group': return OBJ_GROUP(spl_network[1], objs)
		mask = to_dec_mask(spl_network[1])
		net = spl_network[0] +"/"+ str(mask)
		net_obj = addressing(net)
		if net_obj: 
			if mask == 32: return HOST(spl_network[0])
			return NETWORK(spl_network[0], spl_network[1])
	# ----------------------------------------------------
	else:
		subnet = network + "/32"
		net_obj = addressing(network)
		if net_obj: return HOST(network)
	# ----------------------------------------------------
	raise Exception(f"InvalidNetworkOrHost")

def port_member(port, objs):
	"""returns Port group member object for given port, 
	objs will require if port has object-group.
	"""
	port = str(port).strip()
	if port.startswith('eq '): port = port[3:].lstrip()
	if port.startswith('range '): port = port[6:].lstrip()
	if port in ICMP: return PORTS("", port)
	# ----------------------------------------------------
	spl_port = port.split(" ")
	if len(spl_port) == 2: 
		if spl_port[0] == 'object-group': return OBJ_GROUP(spl_port[1], objs)
		return PORTS('range', spl_port[0], spl_port[1])
	dspl_port = port.split("-")
	if len(dspl_port) == 2: return PORTS('range', dspl_port[0], dspl_port[1])
	elif len(dspl_port) == 1 and len(spl_port) == 1: return PORTS('eq', port)
	# ----------------------------------------------------
	raise Exception(f"InvalidPort")

# ----------------------------------------------------------------------------------------

def get_match_dict(request_parameters, objs):
	"""search for request parameters and return matching parameters dictionary.
	(dictionary with attributes require to match in ACL)
	"""
	matching_parameters = ('remark', 'acl_type', 'action', 'protocol', 'source',
		'destination', 'ports',)
	network_member_parameters = ('source', 'destination')
	port_member_parameters = ('ports',)
	matching_dict = {}
	for item in matching_parameters:
		if item in network_member_parameters and item in request_parameters:
			matching_dict[item] = network_member(request_parameters[item], objs)
		elif item in port_member_parameters and item in request_parameters:
			matching_dict[item] = port_member(request_parameters[item], objs)
		elif item in request_parameters:
			matching_dict[item] = request_parameters[item]
	return matching_dict


# ----------------------------------------------------------------------------------------
# Other Functions
# ----------------------------------------------------------------------------------------
def get_port_name(n):
	"""update and return well known port number for port name """
	return PORT_MAPPINGS[n] if PORT_MAPPINGS.get(n) else n

def update_ports_name(requests):
	"""update and return well known port number for port name in given request port"""
	for request in requests: 
		request['ports'] = get_port_name(str(request['ports']))
	return requests

# ----------------------------------------------------------------------------------------
# Control Classes
# ----------------------------------------------------------------------------------------
class HOST():
	"""a single ip host object 

	:: Instance variables ::
	host: host-ip ( returns as str of obj )

	"""
	def __init__(self, host): self.host = host
	def __str__(self): return f"host {self.host}"
	def __repr__(self): return f"host {self.host}"
	def __eq__(self, obj): return str(obj) == str(self)
	def __hash__(self): return hash(IPv4(self.host+"/32"))

class NETWORK():
	"""a network/subnet object 

	:: Instance variables ::
	subnet : network/mask formatted string of subnet
	network:  IP Object

	"""
	def __init__(self, network, dotted_mask=None): 
		if dotted_mask:
			mask = to_dec_mask(dotted_mask)
			self.subnet = network + "/" + str(mask)
		else:
			self.subnet = network
		self.network = addressing(self.subnet)
	def _str(self):
		net = self.network.ipbinmask()
		return 'any4' if net == any4 else net
	def __str__(self): return self._str()
	def __repr__(self): return self._str()
	def __eq__(self, obj): return str(obj) == str(self)
	def __hash__(self): return hash(self.network)

class OBJ_GROUP():
	"""networks/ports grouped object 

	:: Instance variables ::
	group_name : name of object-group
	grp : OBJ object for the given object-group
	
	"""
	def __init__(self, group_name, objectGroups): 
		self.group_name = group_name
		try:
			self.grp = objectGroups[group_name]
		except:
			raise Exception("ObjectGroupNotPresent")
	def __str__(self): return f"object-group {self.group_name}"
	def __repr__(self): return f"object-group {self.group_name}"
	def __eq__(self, obj): return str(obj) == str(self)
	def __hash__(self): return self.grp._hash

class PORTS():
	"""a port/range-of-ports object 

	:: Instance variables ::
	port_type: port-type (ex: eq, range.. )
	port: port-number (beginning in case of range)
	port_range_end : port-number (ending in case of range)
	
	"""
	def __init__(self, port_type, port, port_range_end=''): 
		self.port_type = port_type
		self.port = port
		self.port_range_end = port_range_end
	def __str__(self): return f'{self.port_type} {self.port} {self.port_range_end}'.strip()
	def __repr__(self): return f'{self.port_type} {self.port} {self.port_range_end}'.strip()
	def __eq__(self, obj): return str(obj) == str(self)
	def __hash__(self): return hash(self.port)

class Singular():
	def __init__(self, _type):
		self._type = _type
	def __str__(self): return f'icmp-object {self._type}'.strip()
	def __repr__(self): return f'icmp-object {self._type}'.strip()
	def __eq__(self, obj): return str(obj) == str(self)
	def __hash__(self): return hash(self._type)

Icmp = Singular
PROTOCOL = Singular

# ----------------------------------------------------------------------------------------
#   Main
# ----------------------------------------------------------------------------------------
if __name__ == '__main__':
	pass
# ----------------------------------------------------------------------------------------
