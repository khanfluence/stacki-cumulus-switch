# @copyright@
# Copyright (c) 2006 - 2018 Teradata
# All rights reserved. Stacki(r) v5.x stacki.com
# https://github.com/Teradata/stacki/blob/master/LICENSE.txt
# @copyright@
#
# @rocks@

import stack.commands
from stack.exception import ArgRequired, ArgValue, ParamType, ParamValue, ParamError


class Command(stack.commands.remove.command,
		stack.commands.OSArgumentProcessor,
		stack.commands.HostArgumentProcessor,
		stack.commands.ApplianceArgumentProcessor):
	"""
	Remove a storage controller configuration from the database.

	<param type='string' name='scope'  optional='0'>
	Zero or one parameter. The parameter is the scope for the provided name
	(e.g., 'os', 'host', 'environment', 'appliance').
	No scope means the scope is 'global', and no name will be accepted.
	</param>

	<arg type='string' name='name' optional='0'>
	This argument can be nothing, a valid 'os' (e.g., 'redhat'), a valid
	appliance (e.g., 'backend'), a valid environment (e.g., 'master_node'
	or a host.
	If nothing is supplied, then the configuration will be global.
	</arg>

	<param type='int' name='adapter' optional='1'>
	Adapter address. If adapter is '*', enclosure/slot address applies to
	all adapters.
	</param>

	<param type='int' name='enclosure' optional='1'>
	Enclosure address. If enclosure is '*', adapter/slot address applies
	to all enclosures.
	</param>

	<param type='int' name='slot'>
	Slot address(es). This can be a comma-separated list. If slot is '*',
	adapter/enclosure address applies to all slots.
	</param>

	<example cmd='remove storage controller backend-0-0 slot=1 scope=host'>
	Remove the disk array configuration for slot 1 on the host 'backend-0-0'.
	</example>

	<example cmd='remove storage controller backend slot=1,2,3,4 scope=appliance'>
	Remove the disk array configuration for slots 1-4 for the appliance 'backend'.
	</example>
	"""

	def run(self, params, args):
		scope = None
		oses = []
		appliances = []
		hosts = []

		if len(args) == 0:
			scope = 'global'
		elif len(args) == 1:
			try:
				oses = self.getOSNames(args)
			except:
				oses = []

			try:
				appliances = self.getApplianceNames(args)
			except:
				appliances = []

			try:
				hosts = self.getHostnames(args)
			except:
				hosts = []
		else:
			raise ArgRequired(self, 'scope')

		if not scope:
			if args[0] in oses:
				scope = 'os'
			elif args[0] in appliances:
				scope = 'appliance'
			elif args[0] in hosts:
				scope = 'host'

		if not scope:
			raise ArgValue(self, 'scope', 'a valid os, appliance name or host name')

		if scope == 'global':
			name = None
		else:
			name = args[0]

		adapter, enclosure, slot = self.fillParams([
			('adapter', None), 
			('enclosure', None),
			('slot', None, True)
			])

		if adapter and adapter != '*':
			try:
				adapter = int(adapter)
			except:
				raise ParamType(self, 'adapter', 'integer')
			if adapter < 0:
				raise ParamValue(self, 'adapter', '>= 0')
		else:
			adapter = -1

		if enclosure and enclosure != '*':
			try:
				enclosure = int(enclosure)
			except:
				raise ParamType(self, 'enclosure', 'integer')
			if enclosure < 0:
				raise ParamValue(self, 'enclosure', '>= 0')
		else:
			enclosure = -1

		slots = []
		if slot and slot != '*':
			for s in slot.split(','):
				try:
					s = int(s)
				except:
					raise ParamType(self, 'slot', 'integer')
				if s < 0:
					raise ParamValue(self, 'slot', '>= 0')
				if s in slots:
					raise ParamError(self, 'slot', '"%s" is listed twice' % s)
				slots.append(s)

		#
		# look up the id in the appropriate 'scope' table
		#
		tableid = None
		if scope == 'global':
			tableid = -1
		elif scope == 'appliance':
			self.db.execute("""select id from appliances where
				name = '%s' """ % name)
			tableid, = self.db.fetchone()
		elif scope == 'host':
			self.db.execute("""select id from nodes where name = %s """, name)
			tableid, = self.db.fetchone()

		deletesql = """delete from storage_controller where scope = %s and tableid = %s """, (scope, tableid)

		if adapter != -1:
			deletesql += ' and adapter = %s', adapter

		if enclosure != -1:
			deletesql += ' and enclosure = %s', enclosure

		if slot != '*':
			for slot in slots:
				dsql = '%s and slot = %s', (deletesql, slot)
				self.db.execute(dsql)
		else:
			self.db.execute(deletesql)

