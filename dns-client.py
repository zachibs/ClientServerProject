from scapy.all import *
from scapy.sendrecv import sniff, send
from scapy.layers.inet import UDP, IP
from scapy.layers.dns import DNS, DNSQR, DNSRR

from config import *


def dns_request():
    packet = IP(src=CLIENT_IP, dst=DNS_SERVER_IP) / \
             UDP(sport=RandShort(), dport=DNS_SPORT) / \
             DNS(rd=1, qd=DNSQR(qname=APP_DOMAIN))
    response = sr1(packet, verbose=0)
    # Check if a response was received
    if response is not None:
        # Check if the response contains a DNS resource record
        if response.haslayer(DNSRR):
            # Print the IP address returned by the DNS server
            print(f"The IP address of {APP_DOMAIN} is {response[DNSRR].rdata}")
        else:
            print(f"No IP address found for {APP_DOMAIN}")
    else:
        print("No response received")


if __name__ == '__main__':
    dns_request() 