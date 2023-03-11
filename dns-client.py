from scapy.all import *
from scapy.sendrecv import sniff, send
from scapy.layers.inet import UDP, IP
from scapy.layers.dns import DNS, DNSQR, DNSRR
from time import sleep

from config import *


def send_dns_request():
    packet = IP(src=CLIENT_IP, dst=DNS_SERVER_IP) / \
             UDP(sport=RandShort(), dport=DNS_SPORT) / \
             DNS(rd=1, qd=DNSQR(qname=APP_DOMAIN))
    send(packet)

def handle_dns_packet(pkt):
    sleep(1)
    print("hello")
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

    print(app_server_ip)

if __name__ == '__main__':
    send_dns_request() 
    sniff(filter=f"udp port 53 and src {DNS_SERVER_IP}", prn=handle_dns_packet, iface=NETWORK_INTERFACE)