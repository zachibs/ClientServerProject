# Import necessary modules from Scapy
from scapy.all import *
from scapy.layers.dhcp import DHCP, BOOTP
from scapy.layers.inet import IP, UDP
from scapy.layers.l2 import Ether
from time import sleep

# Constants
from config import *

# Function to handle incoming DHCP packets
def handle_dhcp_packet(pkt):
    sleep(1)
    # Check if it's a DHCP Offer message
    if pkt[DHCP] and pkt[DHCP].options[0][1] == 2:
        # Get MAC address of the network interface
        mac_str = uuid.getnode()
        client_mac_address = ':'.join(['{:02x}'.format((mac_str >> i) & 0xff) for i in range(0, 48, 8)])
        # Get MAC address of the server sending DHCP Offer
        # Get IP address offered by the server
        client_ip_address = pkt[BOOTP].yiaddr

        # Create DHCP Request packet
        dhcp_request = Ether(src=client_mac_address, dst='ff:ff:ff:ff:ff:ff')/ \
                       IP(src=client_ip_address, dst=BROADCAST)/ \
                       UDP(sport=DHCP_DPORT, dport=DHCP_SPORT)/ \
                       BOOTP(op=1, chaddr=client_mac_address, xid=RandShort())/ \
                       DHCP(options=[('message-type', 'request'), ('requested_addr', client_ip_address),
                                     ('server_id', BROADCAST), "end"])

        # Print message indicating that DHCP Request message is being sent
        print(f"Sending DHCP Request to server: {SERVER_IP}")
        # Send DHCP Request packet to the server
        sendp(dhcp_request, iface=NETWORK_INTERFACE)
    
    if pkt[DHCP] and pkt[DHCP].options[0][1] == 5:
        print("DHCP ACK Received")
        print(f"IP Received: {pkt[BOOTP].yiaddr}")
        print(f"DNS Server ip Received: {pkt[DHCP].options[3][1]}")

def send_dhcp_discover():
    mac_str = uuid.getnode()
    client_mac_address = ':'.join(['{:02x}'.format((mac_str >> i) & 0xff) for i in range(0, 48, 8)])
    
    dhcp_discover = Ether(src=client_mac_address, dst='ff:ff:ff:ff:ff:ff')/ \
                    IP(src='0.0.0.0', dst=BROADCAST)/ \
                    UDP(sport=DHCP_DPORT, dport=DHCP_SPORT)/ \
                    BOOTP(chaddr=client_mac_address, op=1)/ \
                    DHCP(options=[('message-type', 'discover'), ('client_id', client_mac_address),
                                  ('requested_addr', '0.0.0.0'), 'end'])

    # Print message indicating that DHCP Discover message is being sent
    print(f"Sending DHCP Discover to server: {BROADCAST}")
    # Send DHCP Discover packet to the server
    sendp(dhcp_discover, iface=NETWORK_INTERFACE)

# Main function
if __name__ == '__main__':
    # Print message indicating that the DHCP client is starting
    print("Starting DHCP client...")

    # Create DHCP Discover packet
    send_dhcp_discover()

    # Sniff for DHCP packets on the specified network interface
    sniff(filter='udp and (port 67 or 68)', prn=handle_dhcp_packet, iface=NETWORK_INTERFACE)
