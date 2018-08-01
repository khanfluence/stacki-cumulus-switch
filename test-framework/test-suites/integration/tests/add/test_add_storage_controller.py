import pytest


class TestAddStorageControllerBase:

	"""
	Test that we can successfully add an os level storage controller
	"""

	def test_add_storage_controller(self, host):
		#this should work and have no errors
		results = host.run('stack add storage controller redhat adapter=1 arrayid=2 enclosure=3 raidlevel=4 slot=5')
		assert results.rc == 0

		#make sure that we are able to list the entry we just added
		results = host.run('stack list storage controller redhat')
		assert 'redhat' in str(results.stdout)

		#this should not work because 'blah' is not a valid scope
		results = host.run('stack add storage controller blah adapter=1 arrayid=2 enclosure=3 raidlevel=4 slot=5')
		assert results.rc != 0


class TestAddStorageControllerScopes():
	"""
	storage controller {name} {scope=string} [adapter=int] [arrayid=string] [enclosure=int] [hotspare=int] [raidlevel=int] [slot=int]
	"""

	@pytest.mark.usefixtures("revert_database")
	@pytest.mark.usefixtures("add_host")
	def test_add_storage_controller_scope_param(self, host):
		"""This should work and have no errors. """
		result = host.run('stack add storage controller scope=global adapter=1 arrayid=test enclosure=1 hotspare=0 '
		                  'raidlevel=1 slot=1,2')
		assert result.rc == 0
		assert '' == result.stdout
		result = host.run('stack add storage controller backend scope=appliance adapter=1 arrayid=test enclosure=1 '
		                  'hotspare=0 raidlevel=1 slot=1,2')
		assert result.rc == 0
		assert '' == result.stdout
		result = host.run('stack add storage controller backend-0-0 scope=host adapter=1 arrayid=test enclosure=1 '
		                  'hotspare=0 raidlevel=1 slot=1,2')
		assert result.rc == 0
		assert '' == result.stdout
		result = host.run('stack add storage controller sles scope=os adapter=1 arrayid=test enclosure=1 hotspare=0 '
		                  'raidlevel=1 slot=1,2')
		assert result.rc == 0
		assert '' == result.stdout
		host.run('stack add environment test')
		result = host.run('stack add storage controller test scope=environment adapter=1 arrayid=test enclosure=1 '
		                  'hotspare=0 raidlevel=1 slot=1,2')
		assert result.rc == 0
		assert '' == result.stdout

	@pytest.mark.usefixtures("revert_database")
	def test_add_storage_controller_multi(self, host):
		host.run('stack add host backend-0-0')
		host.run('stack add host backend-0-1')
		host.run('stack add host backend-0-2')
		result = host.run('stack add storage controller a:backend scope=host adapter=1 arrayid=test enclosure=1 '
		                  'hotspare=0 raidlevel=1 slot=1,2')
		assert result.rc == 0
		assert '' == result.stdout

	@pytest.mark.usefixtures("revert_database")
	@pytest.mark.usefixtures("add_host")
	def test_add_storage_controller_scope_verb(self, host):
		"""This should work and have no errors. """
		result = host.run('stack add storage controller adapter=1 arrayid=test enclosure=1 hotspare=0 raidlevel=1 '
		                  'slot=1,2')
		assert result.rc == 0
		assert '' == result.stdout
		result = host.run('stack add appliance storage controller backend adapter=1 arrayid=test enclosure=1 '
		                  'hotspare=0 raidlevel=1 slot=1,2')
		assert result.rc == 0
		assert '' == result.stdout
		result = host.run('stack add host storage controller backend-0-0 adapter=1 arrayid=test enclosure=1 '
		                  'hotspare=0 raidlevel=1 slot=1,2')
		assert result.rc == 0
		assert '' == result.stdout
		result = host.run('stack add os storage controller sles adapter=1 arrayid=test enclosure=1 hotspare=0 '
		                  'raidlevel=1 slot=1,2')
		assert result.rc == 0
		assert '' == result.stdout
		host.run('stack add environment test')
		result = host.run('stack add environment storage controller test adapter=1 arrayid=test enclosure=1 '
		                  'hotspare=0 raidlevel=1 slot=1,2')
		assert result.rc == 0
		assert '' == result.stdout


	@pytest.mark.usefixtures("revert_database")
	@pytest.mark.usefixtures("add_host")
	def test_add_storage_controller_double_add_partid_negative(self, host):
		"""the first ones should work fine, then error out on the 2nd add."""
		result = host.run('stack add storage controller scope=global adapter=1 arrayid=test enclosure=1 hotspare=0 '
		                  'raidlevel=1 slot=1,2')
		assert result.rc == 0
		assert '' == result.stdout
		result = host.run('stack add appliance storage controller backend adapter=1 arrayid=test enclosure=1 '
		                  'hotspare=0 raidlevel=1 slot=1,2')
		assert result.rc == 0
		assert '' == result.stdout
		result = host.run('stack add host storage controller backend-0-0 adapter=1 arrayid=test enclosure=1 '
		                  'hotspare=0 raidlevel=1 slot=1,2')
		assert result.rc == 0
		assert '' == result.stdout
		result = host.run('stack add os storage controller sles adapter=1 arrayid=test enclosure=1 hotspare=0 '
		                  'raidlevel=1 slot=1,2')
		assert result.rc == 0
		assert '' == result.stdout

		# 2nd add:
		result = host.run('stack add storage controller scope=global adapter=1 arrayid=test enclosure=1 hotspare=0 '
		                  'raidlevel=1 slot=1,2')
		assert result.rc != 0
		assert '' == result.stdout
		result = host.run('stack add appliance storage controller backend adapter=1 arrayid=test enclosure=1 '
		                  'hotspare=0 raidlevel=1 slot=1,2')
		assert result.rc != 0
		assert '' == result.stdout
		result = host.run('stack add host storage controller backend-0-0 adapter=1 arrayid=test enclosure=1 '
		                  'hotspare=0 raidlevel=1 slot=1,2')
		assert result.rc != 0
		assert '' == result.stdout
		result = host.run('stack add os storage controller sles adapter=1 arrayid=test enclosure=1 hotspare=0 '
		                  'raidlevel=1 slot=1,2')
		assert result.rc != 0
		assert '' == result.stdout

	@pytest.mark.usefixtures("revert_database")
	@pytest.mark.usefixtures("add_host")
	def test_add_storage_controller_double_add_mount_negative(self, host):
		"""The first ones should work fine, then error out on the 2nd add."""

		result = host.run('stack add storage controller scope=global adapter=1 arrayid=test enclosure=1 hotspare=0 '
		                  'raidlevel=1 slot=1,2')
		assert result.rc == 0
		assert '' == result.stdout
		result = host.run('stack add appliance storage controller backend adapter=1 arrayid=test enclosure=1 '
		                  'hotspare=0 raidlevel=1 slot=1,2')
		assert result.rc == 0
		assert '' == result.stdout
		result = host.run('stack add host storage controller backend-0-0 adapter=1 arrayid=test enclosure=1 '
		                  'hotspare=0 raidlevel=1 slot=1,2')
		assert result.rc == 0
		assert '' == result.stdout
		result = host.run('stack add os storage controller sles adapter=1 arrayid=test enclosure=1 hotspare=0 '
		                  'raidlevel=1 slot=1,2')
		assert result.rc == 0
		assert '' == result.stdout
		host.run('stack add environment test')
		result = host.run('stack add environment storage controller test adapter=1 arrayid=test enclosure=1 '
		                  'hotspare=0 raidlevel=1 slot=1,2')
		assert result.rc == 0
		assert '' == result.stdout

		# 2nd add:
		result = host.run('stack add storage controller scope=global adapter=1 arrayid=test enclosure=1 hotspare=0 '
		                  'raidlevel=1 slot=1,2')
		assert result.rc != 0
		assert '' == result.stdout
		result = host.run('stack add appliance storage controller backend adapter=1 arrayid=test enclosure=1 '
		                  'hotspare=0 raidlevel=1 slot=1,2')
		assert result.rc != 0
		assert '' == result.stdout
		result = host.run('stack add host storage controller backend-0-0 adapter=1 arrayid=test enclosure=1 '
		                  'hotspare=0 raidlevel=1 slot=1,2')
		assert result.rc != 0
		assert '' == result.stdout
		result = host.run('stack add os storage controller sles adapter=1 arrayid=test enclosure=1 hotspare=0 '
		                  'raidlevel=1 slot=1,2')
		assert result.rc != 0
		assert '' == result.stdout
		result = host.run('stack add environment storage controller test adapter=1 arrayid=test enclosure=1 '
		                  'hotspare=0 raidlevel=1 slot=1,2')
		assert result.rc != 0
		assert '' == result.stdout

	@pytest.mark.usefixtures("revert_database")
	def test_add_storage_controller_scopes_negative(self, host):
		"""these shouldn't work"""
		accepted_scopes = ['global', 'os', 'appliance', 'host']
		for scope in accepted_scopes:
			if scope != 'global':
				result = host.run('stack add storage controller scope=%s' % scope)
				assert result.rc == 255
				assert 'error - "device" parameter is required' in result.stderr
				result = host.run('stack add storage controller scope=%s device=vda' % scope)
				assert result.rc == 255
				assert 'error - "size" parameter is required' in result.stderr
				result = host.run('stack add storage controller scope=%s device=vda size=0' % scope)
				assert result.rc == 255
				assert '"%s name" argument is required' % scope in result.stderr
				result = host.run('stack add storage controller scope=%s device=vda size=0 test' % scope)
				assert result.rc == 255
				if scope == 'host':
					assert 'error - cannot resolve host "test"' in str(result.stderr).lower()
				else:
					assert '"test" argument is not a valid %s' % scope in str(result.stderr).lower()
			else:
				result = host.run('stack add storage controller scope=%s' % scope)
				assert result.rc == 255
				assert 'error - "device" parameter is required' in result.stderr
				result = host.run('stack add storage controller scope=%s device=vda' % scope)
				assert result.rc == 255
				assert 'error - "size" parameter is required' in result.stderr
