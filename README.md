# contiv_kube_script

## Usage

	$ kubecontiv.py create <DESCRIPTION NAME>.json [debug]
	$ Kubecontiv.py delete <DESCRIPTION NAME>.json [debug]

## Descriptino Json

already sample json in working tree : [sample_desc.json](https://github.com/CiscoKorea/contiv_kube_script/blob/master/sample_desc.json)

### Tenant Object

Tenant mapped to Tenant on APIC

	{
		"name" : <TENANT NAME>,
		"policy" : [ <POLICY OBJECT>, ... ],
		"profile" : [ <PROFILE OBJECT>, ... ]
	}

### Policy Object

Policy mapped to Contract on APIC

	{
		"name": <POLICY NAME>,
		"rule": [ <RULE OBJECT>, ...]
	}

### Rule Object

Rule mapped to Rule on APIC

	{
		# Required
		"direction": <"in" | "out">,
		"action": <"allow" | "deny">
		
		# Optional
		"priority":
		
		"from_network": <NETWORK NAME>, 	# if direction is "in"
		"from_group": <GROUP NAME>, 		# if direction is "in"
		"from_ip": <IP ADDRESS>,			# if direction is "in"
		
		"to_network": <NETWORK NAME>,		# if direction is "out"
		"to_group": <GROUP NAME>,			# if direction is "out"
		"to_ip": <IP ADDRESS>,				# if direction is "out"
		
		"protocol": <"tcp" | "udp" | "icmp" | etc...>,
		"port": <PORT NUMBER>,				# please need string value
	}
	

### Profile Object

Profile mapped to App-Profile on APIC

	{
		"name" : <APP-PROFILE NAME>,
		"net" : [ <NETWORK OBJECT>, ... ],
		"group" : [ <GROUP OBJECT>, ... ]
	}

### Network Object
	
Network mapped to BridgeDomain on APIC

	{
		"name" : <NETWORK NAME>, 
		"type": <"infra" | "data">,
		"encap": <"vlan" | "vxlan">,
		"tag": <TAG OF VLAN OR VXLAN>,
		"subnet": <SUBNET CIDR>,
		"gateway": <GATEWAY IP>,
	}
	
### Group Object

Group mapped to EPG on APIC

	{
		"name" : <GROUP NAME>,
		"net" : <NETWORK NAME>,
		"policy" : [ <POLICY NAME>, ... ],
		"pod": [ <POD OBJECT>, ... ]
	}
	
### Pod Object

Pod mapped to Pod on Kubernetes

	{
		"name": <POD NAME>,
		"cname": <CONTAINER NAME>,
		"image": <CONTAINER IMAGE>,
		"command": [ <COMMAND>, ... ]
	}
