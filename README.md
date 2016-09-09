# contiv_kube_script

## Usage

	$ kubecontiv.py create < Description.json >
	$ Kubecontiv.py delete < Description.json >

## Descriptino Json

already sample json in working tree : [sample_desc.json](https://github.com/CiscoKorea/contiv_kube_script/blob/master/sample_desc.json)

### Tenant Object

Tenant mapped to Tenant on APIC

	{
		"name" : <TENANT NAME>,
		"app" : [ <APP-PROFILE OBJECT> ... ]
	}
	
### App-Profile Object

App-Profile mapped to App-Profile on APIC

	{
		"name" : <APP-PROFILE NAME>,
		"group" : [ <GROUP OBJECT> ... ]
	}
	
### Group Object

Group mapped to EPG & BD on APIC

	{
		"name" : <GROUP NAME>, 
		"type": <"infra" OR "data">,
		"encap": <"vlan" OR "vxlan">,
		"tag": <TAG OF VLAN OR VXLAN>,
		"subnet": <SUBNET CIDR>,
		"gateway": <GATEWAY IP>,
		"pod": [ <POD OBJECT> ... ]
	}
	
### Pod Object

Pod mapped to Pod on Kubernetes

	{
		"name": <POD NAME>,
		"cname": <CONTAINER NAME>,
		"image": <CONTAINER IMAGE>,
		"command": [ <COMMAND 1>, <COMMAND 2> ]
	}
