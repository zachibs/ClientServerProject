#!/bin/bash
set -e
exec sudo python3 dhcp-server.py &
exec sudo python3 dns-server.py &
exec sudo python3 app-server.py &
