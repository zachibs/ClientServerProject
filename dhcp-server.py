# Import necessary modules from Scapy
from scapy.all import *
from scapy.layers.dhcp import DHCP, BOOTP
from scapy.layers.inet import IP, UDP
from scapy.layers.l2 import Ether

# Constants
from config import *

# Function to handle incoming DHCP packets
def handle_dhcp_packet(pkt):
    # Get MAC address of the network interface
    server_mac_address = get_if_hwaddr(NETWORK_INTERFACE)
    # Get MAC address of the client requesting DHCP
    client_mac_address = pkt[Ether].src

    if pkt[DHCP]:
        # Check if it's a DHCP Discover message
        if pkt[DHCP].options[0][1] == 1:
            # Print message indicating that DHCP Discover message has been received
            print(f"DHCP Discover received from client: {client_mac_address}")
            # Create DHCP offer packet
            dhcp_offer = Ether(src=server_mac_address, dst=client_mac_address)/ \
                         IP(src=SERVER_IP, dst=CLIENT_IP)/ \
                         UDP(sport=DHCP_SPORT, dport=DHCP_DPORT)/ \
                         BOOTP(op=2, yiaddr=CLIENT_IP, siaddr=SERVER_IP, xid=pkt[BOOTP].xid)/ \
                         DHCP(options=[('message-type', 'offer'), ('subnet_mask', MASK_SUBNET),
                                       ('router', SERVER_IP), ('name_server', SERVER_IP),
                                       ('lease_time', ONE_HOUR_IN_SECONDS)])
            # Print message indicating that DHCP Offer message is being sent
            print(f"Sending DHCP Offer to client: {client_mac_address}")
            # Send DHCP Offer packet to the client
            sendp(dhcp_offer, iface=NETWORK_INTERFACE)
            
        # Check if it's a DHCP Request message
        elif pkt[DHCP].options[0][1] == 3:
            # Print message indicating that DHCP Request message has been received
            print(f"DHCP Request received from client: {client_mac_address}") 
            # Create DHCP ACK packet
            dhcp_ack = Ether(src=server_mac_address, dst=client_mac_address)/ \
                       IP(src=SERVER_IP, dst=BROADCAST)/ \
                       UDP(sport=DHCP_SPORT, dport=DHCP_DPORT)/ \
                       BOOTP(op=2, yiaddr=CLIENT_IP, siaddr=SERVER_IP, xid=pkt[BOOTP].xid)/ \
                       DHCP(options=[('message-type', 'ack'), ('subnet_mask', MASK_SUBNET),
                                     ('router', SERVER_IP), ('name_server', SERVER_IP),
                                     ('lease_time', ONE_HOUR_IN_SECONDS)])
            # Print message indicating that DHCP ACK message is being sent
            print(f"Sending DHCP ACK to client: {client_mac_address}")
            # Send DHCP ACK packet to the client
            sendp(dhcp_ack, iface=NETWORK_INTERFACE)

# Main function
if __name__ == '__main__':
    # Print message indicating that the DHCP server is starting
    print("Starting DHCP server...")
    # Sniff for DHCP packets on the specified network interface
    sniff(filter='udp and (port 67 or 68)', prn=handle_dhcp_packet ,iface=NETWORK_INTERFACE)
