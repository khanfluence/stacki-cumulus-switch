import os
import subprocess
import pytest

STORAGE_SPREADSHEETS = ['backend', 'global']

@pytest.mark.usefixtures("revert_database")
@pytest.mark.usefixtures("add_host")
@pytest.mark.parametrize("csvfile", STORAGE_SPREADSHEETS)
def test_remove_storage_controller(host, csvfile):
	# get filename

	dirn = '/export/test-files/load/storage_controller_'
	input_file = dirn + csvfile + '_input' + '.csv'

	if 'global' in input_file:
		hostname = ''
	else:
		hostname = 'scope=host backend-0-0'
	# check that it has no controller info by default
	result = host.run('stack list storage controller %s' % hostname)
	assert result.rc == 0
	if hostname == ''
		assert len(result.stdout.splitlines()) == 2
	else:
		assert result.stdout == ''

	# load the controller file
	result = host.run('stack load storage controller file=%s' % input_file)
	assert result.rc == 0

	# check that it has controller info
	result = host.run('stack list storage controller %s' % hostname)
	assert result.rc == 0
	assert 'sda' in result.stdout
	assert 'sdb' in result.stdout
	assert '/var/opt/teradata' in result.stdout
	assert result.stderr == ''

	# remove the controller info for a single device
	result = host.run('stack remove storage controller %s device=sdb' % hostname)
	assert result.rc == 0
	assert result.stdout == ''
	assert result.stderr == ''
	# Check that it is indeed removed
	result = host.run('stack list storage controller %s' % hostname)
	assert result.rc == 0
	assert 'sda' in result.stdout
	assert 'sdb' not in result.stdout

	# remove the controller info for a single mountpoint
	result = host.run('stack remove storage controller %s mountpoint="/var/opt/teradata"' % hostname)
	assert result.rc == 0
	assert result.stdout == ''
	assert result.stderr == ''
	# Check that it is indeed removed
	result = host.run('stack list storage controller %s' % hostname)
	assert result.rc == 0
	assert '/var/opt/teradata' not in result.stdout

	# remove all the controller info
	result = host.run('stack remove storage controller %s device="*"' % hostname)
	assert result.rc == 0
	assert result.stdout == ''
	assert result.stderr == ''

	# check that it has no controller info again
	result = host.run('stack list storage controller %s' % hostname)
	assert result.rc == 0
	assert result.stdout == ''
	assert result.stderr == ''

@pytest.mark.usefixtures("revert_database")
@pytest.mark.usefixtures("add_host")
def test_negative_remove_storage_controller(host):
	"""
	Trying to hit the below exceptions. The order is important as it is contextual to the attempted input.

		if scope not in accepted_scopes:
			raise ParamValue(self, '%s' % params, 'one of the following: %s' % accepted_scopes )
		elif scope == 'global' and len(args) >= 1:
			raise ArgError(self, '%s' % args, 'unexpected, please provide a scope: %s' % accepted_scopes)
		elif scope == 'global' and (device is None and mountpoint is None):
			raise ParamRequired(self, 'device OR mountpoint')
		elif scope != 'global' and len(args) < 1:
			raise ArgRequired(self, '%s name' % scope)
	"""
	accepted_scopes = ['global', 'os', 'appliance', 'host', 'environment']

	# Provide extra data on global scope
	result = host.run('stack remove storage controller scope=global backend-0-0 slot=1')
	assert result.rc == 255
	assert 'argument unexpected' in result.stderr

	result = host.run('stack remove storage controller scope=garbage backend-0-0 slot=1')
	assert result.rc == 255
	assert '"scope" parameter must be one of the following:' in result.stderr

	for scope in accepted_scopes:
		if scope != 'global':
			result = host.run('stack remove storage controller scope=%s slot=1' % scope)
			assert result.rc == 255
			assert '"%s name" argument is required' % scope in result.stderr
		else:
			result = host.run('stack remove storage controller scope=%s' % scope)
			assert result.rc == 255
			assert '"slot" parameter is required' in result.stderr
