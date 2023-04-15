from struct import pack, unpack

RSYN = 0
RACK = 1
DATA = 2
RLST = 3

def encode(id : int, mode : int, length : int = 0, data : str = "") -> bytes:
    """length will take the len of {data} in case its not assigned"""
    if not length: length = len(data)
    if mode != DATA: data = pack(f'!2bQ', id, mode, length)
    else: data = pack(f'!2bH{length}s', id, mode, length, data.encode())
    return data

def decode(data : bytes) -> tuple:
    id, mode = unpack('!2b', data[0:2])
    if mode != DATA:
        length, = unpack('!Q', data[2:])
        data = None
    else: 
        length, = unpack('!H', data[2:4])
        data = data[4:].decode()
    return (id, mode, length, data)

