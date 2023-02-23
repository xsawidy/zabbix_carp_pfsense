# Monitoring CARP on PFSense using zabbix

### Installation

- You have to upload check_carp.sh and zabbix_carp.py on pfsense filesystem. (/usr/local/bin/ in this example)
- Create the following user parameters on zabbix-agent config page on pfsense (Service -> Zabbix-agent -> Advanced Options)
```
UserParameter=carp.discovery,/usr/local/bin/python3.8 /usr/local/bin/zabbix_carp.py
UserParameter=carp.status[*],/usr/local/bin/check_carp.sh $1
```
- Set execution permissions
```
chmod +x /usr/local/bin/zabbix_carp.py
chmod +x /usr/local/bin/check_carp.sh
``` 
- Import the template carp_template.xml on zabbix and attach to pfsense hosts
