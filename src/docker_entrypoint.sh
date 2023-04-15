#!/bin/bash
set -e
exec sudo python3 src/servers/dhcp_server.py &
exec sudo python3 src/servers/dns_server.py &
exec sudo python3 src/servers/app_server.py &
