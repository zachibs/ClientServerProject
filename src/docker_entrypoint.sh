#!/bin/bash
set -e
exec sudo python3 -u servers/dhcp_server.py &
exec sudo python3 -u servers/dns_server.py &
exec sudo python3 -u servers/app_server.py &
