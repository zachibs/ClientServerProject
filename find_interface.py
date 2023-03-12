import netifaces
# Get a list of network interfaces
interfaces = netifaces.interfaces()

# Iterate through each interface
for iface in interfaces:
    # Get the IP addresses for the interface
    addrs = netifaces.ifaddresses(iface)
    ipaddrs = addrs.get(netifaces.AF_INET, [])

    if iface == "eth0":
        NETWORK_INTERFACE = "eth0"
        APP_SERVER_IP = ipaddrs[0]['addr']

print(f"{NETWORK_INTERFACE}, {APP_SERVER_IP}")

with open("config.py", "a") as file:
    file.write(f"NETWORK_INTERFACE='{NETWORK_INTERFACE}'\n")
    file.write(f"APP_SERVER_IP='{APP_SERVER_IP}'\n")
