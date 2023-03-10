from scapy.all import *
from scapy.layers.dhcp import DHCP, BOOTP
from scapy.layers.inet import IP, UDP
from scapy.layers.l2 import Ether

# Constants
SERVER_IP = "192.168.1.1"
CLIENT_IP = "192.168.1.255"
BROADCAST = "255.255.255.255"
MASK_SUBNET = "255.255.255.0"
NETWORK_INTERFACE = "eth0"
DPORT = 68
SPORT = 67
ONE_HOUR_IN_SECONDS = 600

def dhcp_server(pkt):
    server_mac_address = get_if_hwaddr(NETWORK_INTERFACE)
    client_mac_address = pkt[Ether].src

    if pkt[DHCP]:

        # check if it's a DHCP Discover message
        if pkt[DHCP].options[0][1] == 1:
            print("DHCP Discover received from client: {}".format(client_mac_address))
            # create DHCP offer packet
            dhcp_offer = Ether(src=server_mac_address, dst=client_mac_address)/ \
                         IP(src=SERVER_IP, dst=CLIENT_IP)/ \
                         UDP(sport=SPORT, dport=DPORT)/ \
                         BOOTP(op=2, yiaddr=CLIENT_IP, siaddr=SERVER_IP, xid=pkt[BOOTP].xid)/ \
                         DHCP(options=[('message-type', 'offer'), ('subnet_mask', MASK_SUBNET),
                                       ('router', SERVER_IP), ('name_server', SERVER_IP),
                                       ('lease_time', ONE_HOUR_IN_SECONDS)])

            print("Sending DHCP Offer to client: {}".format(client_mac_address))
            sendp(dhcp_offer, iface=NETWORK_INTERFACE)
            
        # check if it's a DHCP Request message
        elif pkt[DHCP].options[0][1] == 3:
            print("DHCP Request received from client: {}".format(client_mac_address)) 
            # create DHCP ACK packet
            dhcp_ack = Ether(src=server_mac_address, dst=client_mac_address)/ \
                       IP(src=SERVER_IP, dst=BROADCAST)/ \
                       UDP(sport=SPORT, dport=DPORT)/ \
                       BOOTP(op=2, yiaddr=CLIENT_IP, siaddr=SERVER_IP, xid=pkt[BOOTP].xid)/ \
                       DHCP(options=[('message-type', 'ack'), ('subnet_mask', MASK_SUBNET),
                                     ('router', SERVER_IP), ('name_server', SERVER_IP),
                                     ('lease_time', ONE_HOUR_IN_SECONDS)])

            print("Sending DHCP ACK to client: {}".format(client_mac_address))
            sendp(dhcp_ack, iface=NETWORK_INTERFACE)
        

if __name__ == '__main__':
    print("Starting DHCP server...")
    sniff(filter='udp and (port 67 or 68)', prn=dhcp_server ,iface=NETWORK_INTERFACE)
