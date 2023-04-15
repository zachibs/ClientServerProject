#!/bin/bash
set -e
exec sudo python3 servers/dhcp_server.py &
exec sudo python3 servers/dns_server.py &
exec sudo python3 servers/app_server.py &
