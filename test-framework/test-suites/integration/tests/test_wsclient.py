import json

import wsclient


class TestWSClient:
	def test_wsclient_list_host(self, host):
		"Test the output of wsclient list host"

		if host.system_info.distribution == "centos":
			os = "redhat"
		else:
			os = "sles"
		
		result = host.run("wsclient list host")
		assert result.rc == 0
		assert json.loads(result.stdout) == [
			{
				"host": "frontend-0-0",
				"rack": "0",
				"rank": "0",
				"appliance": "frontend",
				"os": os,
				"box": "default",
				"environment": None,
				"osaction": "default",
				"installaction": "default",
				"status": "deprecated",
				"comment": None
			}
		]

	def test_wsclient_pylib_against_django(self, host, run_django_server):
		"Test the wsclient pylib code against our own Django instance"
		
		# Pull in the credentials
		with open('/root/stacki-ws.cred', 'r') as f:
			credentials = json.load(f)
		
		# Create our client
		client = wsclient.StackWSClient(
			'127.0.0.1',
			'admin',
			credentials[0]['key']
		)

		# Point our client at our own Django instance
		client.url = 'http://127.0.0.1:8000'

		# Login and run a simple command
		client.login()
		data = client.run('list network')

		# Get the expected output directly from the CLI
		result = host.run("stack list network output-format=json")
		assert result.rc == 0
		
		# Make sure we got the data we were expecting
		assert json.loads(data) == json.loads(result.stdout)
