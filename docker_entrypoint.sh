#!/bin/bash
set -e
exec sudo python3 dhcp_server.py &
exec sudo python3 dns_server.py &
exec sudo python3 app_server.py &
