#!/ bin/sh
mkdir -p ${VSD_HOME} ${DATA_RGOS_DIR} ${DATA_RGOS_DIR_COMMON} ${RGOS_DIR} ${RGOS_DIR_COMMON}

rm  -rf /etc/rgmomd/ /etc/rg_mom/ /etc/redis/ /etc/zlog/ /tmp/redis/ /data/protos/ /sbin/redis_cli_plugin
mkdir -p /tmp/run/
mkdir -p /var/run/
mkdir -p /data/protos/
mkdir -p /sbin/redis_cli_plugin



cp -af ${IMAGES}/etc/* /etc/
cp -af ${IMAGES}/sbin/redis_cli_plugin/* /sbin/redis_cli_plugin/
cp -af ${PWD}/mom/data/protos/* /data/protos/

chmod 777 ${IMAGES}/sbin/* -R
chmod 777 * -R
case "${1}" in
	start)
		echo "Starting rgmomd rgmoms.ham.."
		ham&
		sleep 1s		
		./S02mom start
		sleep 1s
		;;
	restart)
		echo "restart rgmomd rgmoms.ham.."
		pkill -9 ham
		ham&
		./S02mom restart
		sleep 1s
		;;

	stop)
		echo "stop rgmomd rgmoms.ham.."
		pkill -9 ham
		./S02mom stop
		sleep 1s

		;;	
	*)
		echo "Usage: ${0} {start|stop|restart}"
		exit 1
		;;
esac
