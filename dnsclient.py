from scapy.all import *
from scapy.sendrecv import sniff, send
from scapy.layers.inet import UDP, IP
from scapy.layers.dns import DNS, DNSQR, DNSRR
from time import sleep

from config import *

app_server_ip = 0

def send_dns_request(app_domain_to_find, new_client_ip_address, dns_server_ip_address):
    packet = IP(src=new_client_ip_address, dst=dns_server_ip_address) / \
             UDP(sport=RandShort(), dport=DNS_SPORT) / \
             DNS(rd=1, qd=DNSQR(qname=app_domain_to_find))
    send(packet)

def handle_dns_packet(pkt):
    sleep(1)
    print(type(pkt))
    global app_server_ip
    if not pkt[IP]:
        return

    ip_source = pkt[IP].src
    ip_dest = pkt[IP].dst
    
    if not pkt.haslayer(DNS):
        return
    if not pkt.haslayer(DNSRR):
        return

    app_server_URL = pkt[DNSRR].rrname.decode().rstrip(".")

    if app_server_URL != APP_DOMAIN:
        return

    app_server_ip = pkt[DNSRR].rdata


def query_dns_server_for_ip(app_domain_to_find, new_client_ip_address, dns_server_ip_address):
    send_dns_request(app_domain_to_find, new_client_ip_address, dns_server_ip_address) 
    sniff(filter=f"udp port 53 and src {dns_server_ip_address}", count=2, timeout=10, prn=handle_dns_packet, iface=NETWORK_INTERFACE)
    print(app_server_ip)
    return app_server_ip
