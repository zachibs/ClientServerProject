# Constants for the project:

SERVER_IP = "192.168.1.1"
CLIENT_IP = "192.168.13.127"
APP_SERVER_IP = "192.168.13.128"
DNS_SERVER_IP = "8.8.8.8"
BROADCAST = "255.255.255.255"
MASK_SUBNET = "255.255.255.0"
APP_DOMAIN = "ZachiAndDanielSqlServer.com"
NETWORK_INTERFACE = "ens33"
DHCP_DPORT = 68
DHCP_SPORT = 67
DNS_SPORT = 53
APP_SERVER_SRC_PORT = 20890
APP_SERVER_DST_PORT = 30501
ONE_HOUR_IN_SECONDS = 600

if __name__ == "__main__":
    import netifaces
    # Get a list of network interfaces
    interfaces = netifaces.interfaces()

    # Iterate through each interface
    for iface in interfaces:
        # Get the IP addresses for the interface
        addrs = netifaces.ifaddresses(iface)
        ipaddrs = addrs.get(netifaces.AF_INET, [])

        # Print the IP addresses for the interface
        print("IP addresses for", iface)
        for addr in ipaddrs:
            print("- ", addr['addr'])
