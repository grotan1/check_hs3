# check_hs3
Icinga / Nagios check plugin for HS3

Copy plugin to your PluginDir. 
```
/usr/lib64/nagios/plugins (Default PluginDir on Centos)
/usr/lib/nagios/plugins (Default PluginDir on Debian/Ubuntu)
```

Arguments:
```
  -h, --help            	show this help message and exit
  -H HOST, --host 	  	HS3 host
  -d DEVREF, --devref 		Comma-separated device ref (i.e: -d 70,181)
  -j JSONSTR, --jsonstr 	HS3 JSON string (default: -j /JSON?request=getstatus&ref=)
  -w WARN, --warn 	  	Comma-separated Warning value (i.e: -w 22,23)
  -c CRIT, --crit 	  	Comma-separated Critical value (i.e: -c 25,26)
  -mx MAX, --max		Comma-separated Max value (i.e: -mx 40,45)
  -mn MIN, --min		Comma-separated Minimum value (i.e: -c 25,26)
  -sym DEVTYPE, --symbos	Device symbol (i.e: -dt °C)
  -s, --ssl             	Use ssl
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
			description = "Commaseparated list of devices."
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
		"-mx" = {
			value = "$hs3_max$"
			description = "Maximum Value"
		}		
		"-mn" = {
			value = "$hs3_min$"
			description = "Minimum Value"
		}
		"-sym" = {
			value = "$hs3_symbol$"
			description = "Symbol (ex: -sym °C)"
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
  check_interval = 1m
  vars.hs3_address = host.address
  vars.hs3_devref = "36,70"
  vars.hs3_warn = "20,21"
  vars.hs3_crit = "25,26"
  vars.hs3_max = "40,45"
  vars.ms3_min = "0,0"
  vars.hs3_symbol = "°C"  
  assign where host.name == "hs3.example.com"
}
```
