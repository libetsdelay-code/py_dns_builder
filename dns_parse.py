import socket
import struct
from io import BytesIO
from dataclasses import dataclass
from dns_header import build_query, DNSHeader, DNSQuestion

# --- Part 2: Parsing Logic ---

@dataclass
class DNSRecord:
    name: bytes
    type_: int
    class_: int
    ttl: int
    data: bytes

def parse_header(reader):
    # Read first 12 bytes
    data = reader.read(12)
    # Unpack into 6 integers
    items = struct.unpack("!HHHHHH", data)
    return DNSHeader(*items)
    # get items in the tuple

def decode_name_simple(reader):
    parts = []
    while (length := reader.read(1)[0]) != 0:
        parts.append(reader.read(length))
    return b".".join(parts)

def decode_name(reader):
    parts = []
    while (length := reader.read(1)[0]) != 0:
        if length & 0b1100_0000:
            parts.append(decode_compressed_name(length, reader))
            break
        else:
            parts.append(reader.read(length))
    return b".".join(parts)


def decode_compressed_name(length, reader):
    pointer_bytes = bytes([length & 0b0011_1111]) + reader.read(1)
    pointer = struct.unpack("!H", pointer_bytes)[0]
    current_pos = reader.tell()
    reader.seek(pointer)
    result = decode_name(reader)
    reader.seek(current_pos)
    return result

def parse_question(reader):
    name = decode_name_simple(reader)
    data = reader.read(4)
    type_, class_ = struct.unpack("!HH", data)
    return DNSQuestion(name, type_, class_)

def parse_record(reader):
    name = decode_name(reader)
    data = reader.read(10)
    type_, class_, ttl, data_len = struct.unpack("!HHIH", data)
    data = reader.read(data_len)
    return DNSRecord(name, type_, class_, ttl, data)


# 1. Build and Send Query
query = build_query("www.example.com", 1) # Type 1 = A Record (IP)
print(query)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
sock.sendto(query, ("8.8.8.8", 53))

# 2. Receive Response
# recvfrom returns (data, address). We only need 'data' (response).
response, _ = sock.recvfrom(1024) 
print(f"Response received: {len(response)} bytes")

# 3. Parse the Response Header
reader = BytesIO(response)
print(reader)
header = parse_header(reader)
print(header)

question = reader.read(21)


reader = BytesIO(response)
parse_header(reader)
parse_question(reader)
parse_record(reader)