source ./config.sh

tcpdump -s 0 -i wlan0 port $REV_PROXY_PORT -w capture.pcap &
tcpdump_pid=$!

python rev_proxy.py $SERVER_IP $REV_PROXY_PORT $FORWARD_PORT 0 &
proxy_pid=$!
sleep 2

curl "http://$HOSTNAME/"
curl "http://$HOSTNAME/flag"

sleep 5

kill $proxy_pid
kill $tcpdump_pid 

