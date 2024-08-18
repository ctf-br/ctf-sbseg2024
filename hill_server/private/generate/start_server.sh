source ./config.sh

python server.py $HTTP_PORT $HOSTNAME $FORWARD_PORT &
server_pid=$!

python rev_proxy.py 127.0.0.1 $HTTP_PORT $REV_PROXY_PORT 1

kill $server_pid 

