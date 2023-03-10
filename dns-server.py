from scapy.all import *
from scapy.sendrecv import sniff, send
from scapy.layers.inet import UDP, IP
from scapy.layers.dns import DNS, DNSQR, DNSRR

from config import *


def handle_dns_packet(pkt):
    if not pkt.haslayer(DNS):
        return
    
    if not pkt.haslayer(DNSQR):
        return
    
    req_name = pkt[DNSQR].qname.decode().rstrip(".")

    if req_name != APP_DOMAIN:
        return
    
    query = pkt[DNS].qd.qname.decode('utf-8')[:-1]
    print(f"Received DNS query for {query}")

    dnsrr = DNSRR(rrname=APP_DOMAIN, type="A", rclass="IN", ttl=60, rdata=APP_SERVER_IP)
    response = IP(src=DNS_SERVER_IP, dst=pkt[IP].src) / \
               UDP(sport=53, dport=pkt[UDP].sport) / \
               DNS(id=pkt[DNS].id, an=dnsrr, qr=1)
    send(response)


if __name__ == '__main__':
    print("DNS Server is running")
    sniff(filter="udp port 53", prn=handle_dns_packet, iface=NETWORK_INTERFACE)