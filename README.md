# ClientServerProject


## Introduction
A project to demonstrate knowledge regrading the client-server architecture, implemented DHCP, DNS and TCP servers and clients.

## prerequisites:

* docker

## Setup:
### Commands to run for a docker container:
1. `docker build -t "latestnetworksserver" .`
2. `docker run -it --name latestnetworksserver -p 3300:22 -d latestnetworksserver`
3. `ssh admin@localhost -p 3300`
4. `cd ComputerNetworksFinal`
5. `sudo python3 client_side.py`

### Commands to run in local machine:
1. `sudo pip install -r requirements.txt.`
2. `sudo python3 dhcp_server.py `
3. `sudo python3 dns_server.py `
4. `sudo python3 app_server.py `
5. `sudo python3 client_side.py`
6. run the python files in different terminals
