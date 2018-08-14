import json


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
