#!/bin/bash
set -e
exec sudo python3 -u src/servers/dhcp_server.py &
exec sudo python3 -u src/servers/dns_server.py &
exec sudo python3 -u src/servers/app_server.py &
