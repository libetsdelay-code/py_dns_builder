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

# --- Main Exec---

# 1. Build and Send Query
query = build_query("www.example.com", 1) # Type 1 = A Record (IP)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(query, ("8.8.8.8", 53))

# 2. Receive Response
# recvfrom returns (data, address). We only need 'data' (response).
response, _ = sock.recvfrom(1024) 
print(f"Response received: {len(response)} bytes")

# 3. Parse the Response Header
reader = BytesIO(response)
header = parse_header(reader)
print(header)
