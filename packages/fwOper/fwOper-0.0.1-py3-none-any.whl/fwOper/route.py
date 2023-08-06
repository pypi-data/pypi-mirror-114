
# ----------------------------------------------------------------------------------------
from collections import OrderedDict
from nettoolkit import *

from .common import Singulars
# ----------------------------------------------------------------------------------------
def routes_list(config_list):
	"""list of lines with static routes from given config-list """
	return [line.rstrip() for line in config_list if line.startswith("route ")]

# ----------------------------------------------------------------------------------------
# Static Route Entries
# ----------------------------------------------------------------------------------------
class ROUTES():
	"""collection of object of Routes """
	def __init__(self, config_list):
		############ To be moved over to custom deployment #############
		# self.cfg_interface_group_list = interface_group_list(config_list)
		################################################################
		self.cfg_routes_list = routes_list(config_list)
		self.routes_list = []
		self.get_route_objects()
	def __iter__(self):
		for item in self.routes_list: yield item
	def __getitem__(self, item):
		try:
			return self.routes_list[item]
		except:
			return None
	def __getattr__(self, attr): return self[attr]
	def __len__(self): return len(self.routes_list)
	def __contains__(self, network): return self.prefix(network)

	# ~~~~~~~~~~~~~~~~~~ CALLABLE ~~~~~~~~~~~~~~~~~~

	def prefix(self, network):
		"""check matching network in ROUTES object, return matching route """
		route_match = None
		for sn in reversed(self):
			if network in sn:
				route_match = sn
				break
		if route_match: return route_match

	def get_route_objects(self):
		"""set ROUTE objects in self instance """
		for route_line in self.cfg_routes_list:
			route =  ROUTE(route_line)
			route.parse()
			############ To be moved over to custom deployment #############
			# route.parse_group(self.cfg_interface_group_list)
			################################################################
			self.routes_list.append(route)


# ----------------------------------------------------------------------------------------
# Static Route Details
# ----------------------------------------------------------------------------------------
class ROUTE(Singulars):
	"""Individual static-route object"""
	def __init__(self, route_line):
		super().__init__()
		self.route_line = route_line
		self._repr_dic = OrderedDict()
	def __contains__(self, network): return isSubset(network, self.network)

	# ~~~~~~~~~~~~~~~~~~ CALLABLE ~~~~~~~~~~~~~~~~~~

	def parse(self):
		"""parse static route line and set route_dict """
		spl_route_line = self.route_line.split()
		self._repr_dic['ifdesc'] = spl_route_line[1]
		self._repr_dic['nexthop'] = spl_route_line[4]
		try: self._repr_dic['distance'] = int(spl_route_line[5])
		except: self._repr_dic['distance'] = 1
		mask = to_dec_mask(spl_route_line[3])
		self._repr_dic['network'] = addressing(spl_route_line[2]+"/"+str(mask))


'''  ############ To be moved over to custom deployment #############
	def parse_group(self, cfg_interface_group_list):
		"""parse interface group list to get interface name-remark
		custom ---> to be moved to custom project
		"""
		self.remark = ""
		for grp_line in cfg_interface_group_list:
			spl_grp_line = grp_line.strip().split()
			if spl_grp_line[-1] == self.interface_desc:
				self.remark = spl_grp_line[1]
				break
		if not self.remark and cfg_interface_group_list:
			print(f"ACLNameundetected: {cfg_interface_group_list}")
'''

# ------------------------------------------------------------------------------ #
if __name__=="__main__":
	pass
# ------------------------------------------------------------------------------ #
