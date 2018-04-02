# check_hs3
Icinga / Nagios check plugin for HS3

Arguments:
```
  -h, --help            	show this help message and exit
  -H HOST, --host 	  	HS3 host
  -d DEVREF, --devref 		DEVREF HS3 comma-separated device ref (ex: -d 70,181)
  -j JSONSTR, --jsonstr 	HS3 JSON string (ex: -j /JSON?request=getstatus&ref=)
  -w WARN, --warn 	  	Warning value
  -c CRIT, --crit 	  	Critical value
  -dt DEVTYPE, --devtype	Device type (ex: -dt °C)
  -s, --ssl             	Use ssl (HTTPS://)
  -u USERNAME, --username 	Username
  -p PASSWORD, --password	Password
```
Icinga command:
```
object CheckCommand "hs3" {
	command = [ PluginContribDir + "/check_hs3.py" ]

	arguments = {
		"-H" = {
			value = "$hs3_address$"
			description = "Name or IP address of HS3 to check."
		}
		"-d" = {
			value = "$hs3_devref$"
			description = "Comma-separated list of devices."
		}
		"-j" = {
			value = "$hs3_djsonstr$"
			description = "HS3 JSON string (ex: /JSON?request=getstatus&ref=)"	
		}
		"-w" = {
			value = "$hs3_warn$"
			description = "Warning value"
		}
		"-c" = {
			value = "$hs3_crit$"
			description = "Critical Value"
		}
		"-dt" = {
			value = "$hs3_devicetype$"
			description = "Device type (ex: -dt °C)"
		}				
		"-s" = {
			value = "$hs3_ssl$"
			description = "Use ssl"
		}
		"-u" = {
			value = "$hs3_username$"
			description = "Username"
		}
		"-p" = {
			value = "$hs3_password$"
			description = "Password"
		}				
	}
}
```

Service example:
```
apply Service "temperature_outdoor" {
  import "generic-service"
  check_command = "hs3"
  
  vars.hs3_address = host.address
  vars.hs3_devref = "36,70"
  vars.hs3_devicetype = "°C"  
  assign where host.name == "hs3.example.com"
}
```
