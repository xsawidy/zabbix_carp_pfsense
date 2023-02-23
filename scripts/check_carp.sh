chmod +x /usr/local/bin/zabbix_carp.py
chmod +x /usr/local/bin/check_carp.sh


UserParameter=carp.discovery,/usr/local/bin/python3.8 /usr/local/bin/zabbix_carp.py
UserParameter=carp.status[*],/usr/local/bin/check_carp.sh $1


if [ $# -eq 0 ]; then
	echo "Missing arguments"
	exit $STATE_UNKNOWN
fi

getStatus() {
	VHID='vhid '"$1"
	STATUS=$(ifconfig -a | grep carp | grep "$VHID" | awk -F " " '{print $2}')
	if [ $? -eq 0 ]; then
		case $STATUS in
			MASTER)
				echo 1
				;;
			BACKUP)
				echo 0
				;;
			*)
				return 1
		esac
		return 0
	fi
	return 1
}

getStatus $1
