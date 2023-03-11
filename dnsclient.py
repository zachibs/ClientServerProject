import socket
import json
from config import *

def query_dns_server_for_ip(domain_name):
    print("Started DNS client")
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Encode the DNS query
    request_json = json.dumps({"domain":domain_name})
    query = request_json.encode()
    sock.sendto(query, (DNS_SERVER_IP, DNS_SPORT))

    # Receive the DNS response
    data, addr = sock.recvfrom(1024)

    # Decode and print the DNS response
    response = data.decode()
    response_json = json.loads(response)
    print(f"Received DNS response from {addr}: Domain: '{domain_name}' , ip-address: {response_json['ip']}")
    if response_json['ip'] == "not found":
        return None
    return response_json['ip']
