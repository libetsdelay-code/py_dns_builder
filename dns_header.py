from dataclasses import dataclass
import dataclasses
import struct
import random

# --- Part 1: Classes & Building Logic ---

@dataclass
class DNSHeader:
    id: int 
    flags: int
    num_questions: int = 0
    num_answers: int = 0
    num_authorities: int = 0
    num_additionals: int = 0

@dataclass
class DNSQuestion:
    name: bytes
    type_: int
    class_: int

def header_to_bytes(header):
    fields = dataclasses.astuple(header)
    # ! = Network (Big Endian), H = Unsigned Short (2 bytes)
    return struct.pack("!HHHHHH", *fields)

def question_to_bytes(question):
    # Pack Type and Class as 2 unsigned shorts (!HH)
    return question.name + struct.pack("!HH", question.type_, question.class_)

def encode_dns_name(domain_name):
    encoded = b""
    for part in domain_name.encode("ascii").split(b"."):
        encoded += bytes([len(part)]) + part 
    return encoded + b"\x00"

def build_query(domain_name, record_type):
    name = encode_dns_name(domain_name)
    id = random.randint(0, 65535)
    # Recursion Desired (RD) bit at position 8
    RECURSION = 1 << 8 
    header = DNSHeader(id=id, num_questions=1, flags=RECURSION) 
    question = DNSQuestion(name=name, type_=record_type, class_=1)
    return header_to_bytes(header) + question_to_bytes(question)


print(encode_dns_name("google.com"))