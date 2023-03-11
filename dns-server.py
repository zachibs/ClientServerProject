from config import *
import socket
import json
from scapy.layers.dns import DNS, DNSQR, DNSRR



def handle_dns_request(sock, data, address):
    DNS_DATABASE = {APP_DOMAIN:APP_SERVER_IP}

    # request_json = json.loads(data.decode())
    # print(f"Received DNS query from {address}: requested domain name: {request_json['domain']}")
    
    # # Extract the domain name from the query
    # domain_name = request_json["domain"]

    dns_data = (DNS(data))
    domain_name = dns_data.qd.qname.decode('utf-8')[:-1]
    
    # Check if the domain name is in our DNS table
    if domain_name in DNS_DATABASE:
        # If so, construct the DNS response with the IP address
        ip_address = DNS_DATABASE[domain_name]
        dnsrr = DNSRR(rrname=APP_DOMAIN, type="A", rclass="IN", ttl=60, rdata=ip_address)
        response = DNS(id=dns_data.id, an=dnsrr, qr=1)
        print(f"Sending DNS response to {address}: {response}")
        
        # Encode the response and send it back to the client
        sock.sendto(bytes(response), address)
    else:
        # If not, respond with an error message
        dnsrr = DNSRR(rrname=APP_DOMAIN, type="A", rclass="IN", ttl=60, rdata="0.0.0.0")
        response = DNS(id=dns_data.id, an=dnsrr, qr=1)
        print(f"Sending DNS response to {address}: {response}")
        
        # Encode the response and send it back to the client
        sock.sendto(bytes(response), address)

def start_dns_server(dns_server_ip):
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind the socket to the DNS port
    sock.bind((dns_server_ip, DNS_SPORT))
    print(f"DNS server listening on port {DNS_SPORT}...")

    # Wait for DNS queries and handle them
    while True:
        data, addr = sock.recvfrom(1024)
        handle_dns_request(sock, data, addr)

if __name__ == "__main__":
    start_dns_server(DNS_SERVER_IP)