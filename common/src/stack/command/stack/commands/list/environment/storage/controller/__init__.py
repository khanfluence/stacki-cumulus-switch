# @copyright@
import stack.commands


class Command(stack.commands.list.command):
	"""
	List storage controller configuration for an environments.

	<arg type='string' name='host' optional='1'>
	OS Name
	</arg>

	<param type='string' name='device' optional='1'>
	Device whose controller configuration needs to be added to
	the database.
	</param>

	<param type='string' name='mountpoint' optional='1'>
	Mountpoint for the controller that needs to be added to
	the database.
	</param>

	<example cmd='list environment storage controller '>
	Adds the controller information for environment
	</example>
	"""

	def run(self, params, args):
		self.addText(self.command('list.storage.controller', self._argv + [ 'scope=environment' ]))
		return self.rc
