import socket
import json
from config import *
from scapy.layers.inet import UDP, IP
from scapy.layers.dns import DNS, DNSQR, DNSRR
from scapy.all import RandShort


def query_dns_server_for_ip(domain_name, new_client_ip_address, dns_server_ip_address):
    print("Started DNS client")
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Encode the DNS query
    # request_json = json.dumps({"domain":domain_name})
    # query = request_json.encode()

    packet = DNS(rd=1, qd=DNSQR(qname=domain_name))

    # query = (str(packet)).encode()
    query = bytes(packet)
    sock.sendto(query, (DNS_SERVER_IP, DNS_SPORT))

    # Receive the DNS response
    data, addr = sock.recvfrom(1024)

    # Decode and print the DNS response
    dns_data = (DNS(data))
    app_ip_address = dns_data.an.rdata
    print(f"Received DNS response from {addr}: Domain: '{domain_name}' , ip-address: {app_ip_address}")
    if app_ip_address == "0.0.0.0":
        return None
    return app_ip_address
