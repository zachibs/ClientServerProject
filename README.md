# ClientServerProject


## Introduction
A project to demonstrate knowledge regrading the client-server architecture, implemented DHCP, DNS and TCP servers and clients.

## prerequisites:

* docker

## Setup:

1. `docker build -t "latestnetworksserver" .`
2. `docker run -it --name latestnetworkserver -p 3300:22 -d latestnetworksserver`
3. `ssh admin@localhost -p 3300`
4. `cd ComputerNetworksFinal`
5. `sudo python3 client_side.py`
