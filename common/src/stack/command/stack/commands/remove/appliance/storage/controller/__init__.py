# @copyright@
import stack.commands


class Command(stack.commands.remove.command):
	"""
	Remove storage controller configuration for an appliance.

	<arg type='string' name='host' optional='1'>
	Hostname of the machine
	</arg>
	
	<param type='string' name='device' optional='1'>
	Device whose controller configuration needs to be removed from
	the database.
	</param>

	<param type='string' name='mountpoint' optional='1'>
	Mountpoint for the controller that needs to be removed from
	the database.
	</param>

	<example cmd='remove host storage controller backend-0-1'>
	Removes the controller information for backend-0-1
	</example>
	"""

	def run(self, params, args):
		self.addText(self.command('remove.storage.controller', self._argv + [ 'scope=appliance' ]))
		return self.rc
