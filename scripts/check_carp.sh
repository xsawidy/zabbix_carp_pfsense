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
			*)
				echo 0
		esac
		return 0
	fi
	return 1
}

getStatus $1
