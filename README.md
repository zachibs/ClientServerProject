# ClientServerProject


## Introduction
A project to demonstrate knowledge regrading the client-server architecture, implemented DHCP, DNS and TCP servers and clients.

## prerequisites:

* docker

## Setup:
### Commands to run for a docker container:
1. `git clone https://github.com/zachibs/ClientServerProject.git`
2. `cd ClientServerProject`
3. `docker build -t "latestnetworksserver" .`
4. `docker run -it --name latestnetworksserver -p 3300:22 -d latestnetworksserver`
5. `ssh admin@localhost -p 3300`
6. password is 1234
7. `cd ClientServerProject/src`
8. `sudo python3 client_side.py`

### Commands to run in local machine:
1. `git clone https://github.com/zachibs/ClientServerProject.git`
2. `cd ClientServerProject`
* run the python files in different terminals
3. `sudo pip install -r requirements.txt.`
4. `sudo python3 src/servers/dhcp_server.py`
5. `sudo python3 src/servers/dns_server.py`
6. `sudo python3 src/servers/app_server.py`
7. `sudo python3 src/client_side.py`
