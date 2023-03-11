# Import necessary modules from Scapy
from scapy.all import *
from scapy.layers.dhcp import DHCP, BOOTP
from scapy.layers.inet import IP, UDP
from scapy.layers.l2 import Ether

# Constants
from config import *

# Function to handle incoming DHCP packets
def handle_dhcp_packet(pkt):
    # Check if it's a DHCP Offer message
    if pkt[DHCP] and pkt[DHCP].options[0][1] == 2:
        # Get MAC address of the network interface
        client_mac_address = get_if_hwaddr(NETWORK_INTERFACE)
        # Get MAC address of the server sending DHCP Offer
        server_mac_address = pkt[Ether].src
        # Get IP address offered by the server
        client_ip_address = pkt[BOOTP].yiaddr

        # Create DHCP Request packet
        dhcp_request = Ether(src=client_mac_address, dst=server_mac_address)/ \
                       IP(src=CLIENT_IP, dst=SERVER_IP)/ \
                       UDP(sport=DHCP_DPORT, dport=DHCP_SPORT)/ \
                       BOOTP(op=1, chaddr=client_mac_address)/ \
                       DHCP(options=[('message-type', 'request'), ('requested_addr', client_ip_address),
                                     ('server_id', SERVER_IP)])

        # Print message indicating that DHCP Request message is being sent
        print(f"Sending DHCP Request to server: {SERVER_IP}")
        # Send DHCP Request packet to the server
        sendp(dhcp_request, iface=NETWORK_INTERFACE)

        # Print message indicating that DHCP Request message has been sent
        print(f"DHCP Request sent to server: {SERVER_IP}")
    
    if pkt[DHCP] and pkt[DHCP].options[0][1] == 5:
        print("DHCP ACK Received")
        print(f"IP Received: {packet[BOOTP].yiaddr}")

# Main function
if __name__ == '__main__':
    # Print message indicating that the DHCP client is starting
    print("Starting DHCP client...")
    # Create DHCP Discover packet
    dhcp_discover = Ether(dst=BROADCAST)/ \
                    IP(src='0.0.0.0', dst='255.255.255.255')/ \
                    UDP(sport=DHCP_DPORT, dport=DHCP_SPORT)/ \
                    BOOTP(chaddr=get_if_hwaddr(NETWORK_INTERFACE), xid=random.randint(1, 1000000))/ \
                    DHCP(options=[('message-type', 'discover'), ('client_id', get_if_hwaddr(NETWORK_INTERFACE)),
                                  ('requested_addr', CLIENT_IP), 'end'])

    # Print message indicating that DHCP Discover message is being sent
    print(f"Sending DHCP Discover to server: {BROADCAST}")
    # Send DHCP Discover packet to the server
    sendp(dhcp_discover, iface=NETWORK_INTERFACE)

    # Print message indicating that DHCP Discover message has been sent
    print(f"DHCP Discover sent to server: {BROADCAST}")

    # Sniff for DHCP packets on the specified network interface
    sniff(filter='udp and (port 67 or 68)', prn=handle_dhcp_packet, iface=NETWORK_INTERFACE)
