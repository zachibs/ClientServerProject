from scapy.all import *
from scapy.sendrecv import sniff, send
from scapy.layers.inet import UDP, IP
from scapy.layers.dns import DNS, DNSQR, DNSRR
from scapy.layers.l2 import Ether
from time import sleep

# Importing the variables from the configuration file
from config import *


def handle_dns_packet(pkt: Ether) -> None:
    sleep(1)
    # Check if the packet contains a DNS layer
    if not pkt.haslayer(DNS):
        return
    
    # Check if the packet contains a DNS query
    if not pkt.haslayer(DNSQR):
        return
    
    # Get the requested domain name from the DNS query
    req_name = pkt[DNSQR].qname.decode().rstrip(".")
    
    # Check if the requested domain name matches the application domain name
    if req_name != APP_DOMAIN:
        return
    
    # Extract the query from the packet and print it to the console
    query = pkt[DNS].qd.qname.decode('utf-8')[:-1]
    print(f"Received DNS query for {query}")
    
    # Create a DNS resource record for the application server IP
    dnsrr = DNSRR(rrname=APP_DOMAIN, type="A", rclass="IN", ttl=60, rdata=APP_SERVER_IP)
    
    # Create a DNS response packet with the appropriate source and destination IP addresses,
    # source and destination ports, and with the DNS resource record created earlier
    response = IP(src=DNS_SERVER_IP, dst=pkt[IP].src) / \
               UDP(sport=DNS_SPORT, dport=pkt[UDP].sport) / \
               DNS(id=pkt[DNS].id, an=dnsrr, qr=1)   
                
    # Send the DNS response packet
    # print(f"Response - {response}")
    print(f"Sent Response to IP={pkt[IP].src}")
    send(response)


if __name__ == '__main__':
    print("Starting DNS server...")
    # Sniff for incoming DNS packets on the specified network interface, and call the
    # handle_dns_packet function for each packet that matches the filter
    sniff(filter="udp port 53", prn=handle_dns_packet, iface=NETWORK_INTERFACE)