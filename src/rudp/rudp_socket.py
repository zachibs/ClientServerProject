import socket
import rudp_packet
import time
import random

TIMEOUT = 0.0001
MAX_WINDOW_SIZE = 16384
INFINITY = 10000000

LOSE_RANDOM_PACKETS = False

sock : socket.socket = None
server : tuple[str, int] = None

def bind(client_ip, port):
    global sock
    #create a UDP socket for sending/recieving data
    sock = socket.socket(family= socket.AF_INET, type= socket.SOCK_DGRAM)
    if client_ip != None:
        sock.bind((client_ip, port))
    sock.settimeout(TIMEOUT)
    sock.setblocking(0)

def connect(server_ip, port):
    global server
    #set send end point
    server = (server_ip, port)

def _timed_recv(buffer_size, duration):
    start = time.time()
    while time.time() - start < duration:
        try: 
            data, c = sock.recvfrom(buffer_size)
            return data, c
        except: continue
    return None, None

def send(data):
    length = len(data)

    #start conversation by sending sync
    sock.sendto(
        rudp_packet.encode(0, rudp_packet.RSYN, length),
        server
    )

    #wait to ack
    res, _ = _timed_recv(256, TIMEOUT)
    if not res: 
        print('no response recived')
        return False

    #check if packet was recieved correctly
    pack = rudp_packet.decode(res)
    print(pack)
    if pack[1] != rudp_packet.RACK or pack[2] != length:
        print('no ack recieved')
        return False

    #start sending data with growing windows
    #window will grow after n sends
    #where n = log(window_size) - 7
    #if messege is lost the window caps at last size
    window_size = 2
    next_increase = 1
    is_capped = False
    packet_id = 1
    data_sent = 0
    while data_sent != length:
        #send packet to server
        packet_size = min(window_size, length - data_sent)
        pack = rudp_packet.encode(
            id = packet_id,
            mode = rudp_packet.DATA,
            length = packet_size,
            data = data[data_sent : data_sent + packet_size + 1]
        )
        print(f"sending pack {packet_id} :", rudp_packet.decode(pack))
        sock.sendto(pack, server)

        #see if packet was lost and resend
        res, _ = _timed_recv(256, TIMEOUT / 10)
        if res:
            res = rudp_packet.decode(res)
            if res[1] == rudp_packet.RLST:
                if not is_capped:   
                    window_size = 2 if window_size == 2 else window_size // 2
                    is_capped = True

                packet_id = res[0]
                data_sent = res[2]
                print(f"packet {packet_id} was lost")
                continue

        #increase window
        if not is_capped and packet_id == next_increase:
            next_increase += next_increase + 1
            window_size *= 2
            if window_size >= MAX_WINDOW_SIZE: is_capped = True

        packet_id += 1
        data_sent += packet_size

def recv():
    def resend_packet():
        pack = rudp_packet.encode(packet_id + 1, rudp_packet.RLST, data_recv, "")
        sock.sendto(pack, client)
        print("sending :", rudp_packet.decode(pack))

    length = 0
    client : tuple[str, int] = None
    total_data = ""

    #wait for sync request
    while not client:
        data, c = _timed_recv(256, INFINITY)
        pack = rudp_packet.decode(data)
        if pack[1] == rudp_packet.RSYN:
            client = c
            length = pack[2]

    #send ACK back
    sock.sendto(
        rudp_packet.encode(0, rudp_packet.RACK, length),
        client
    )
    print('sent :', rudp_packet.decode(rudp_packet.encode(0, rudp_packet.RACK, length)))
    print("Got connetion from :", client)

    packet_id = 0
    data_recv = 0
    while length != data_recv:
        data, c = _timed_recv(MAX_WINDOW_SIZE, 1)
        #check for timeout to reset
        if data:
            #simulate packet loss
            if LOSE_RANDOM_PACKETS:
                r = random.randint(1,2)
                if r == 1:
                    print("lost due to timeout")
                    resend_packet()
                    continue

            pack = rudp_packet.decode(data)
            if pack[1] == rudp_packet.DATA:
                print("recieved :", pack)
                #check if packet was lost
                if pack[0] != packet_id + 1:
                    print("lost due to error")
                    resend_packet()
                else:
                    data_recv += pack[2]
                    total_data += pack[3]
                    packet_id += 1
        else:
            print("lost due to timeout")
            resend_packet()
    
    print('final data :', total_data)



def close():
    sock.close()

selection = input("send recv? 1/2 : ")
src_port = 50000 if selection == "1" else 50001
dst_port = 50001 if selection == "1" else 50000

addr = "localhost"
if selection != '1':
    bind(addr, src_port)
else :
    bind(None, src_port)
connect(addr, dst_port)
if selection == "1":
    while True:
        inp = input()
        send(inp)
else:
    while True:
        recv()