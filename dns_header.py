# build a dns query 2 parts ->  header and a question
# 1 - things is to create a python classes for the header and the question
# 2 - Write header_to_bytes  and question_to_byte
# 3 - Write a build_query(domain_name, record_type)

1.1 # write dnsheader and dnsquestions classes

from dataclasses import dataclass
import dataclasses
import struct

@dataclass
class DNSHeader:
    id: int 
    flags: int
    num_questions: int = 0
    num_answers: int = 0
    num_authorities: int = 0
    num_additionals: int = 0

#dns questions has 3 fields (name like example.com) a type A and a class 

@dataclass
class DNSQuestion:
    name: bytes
    type_: int
    class_: int

1.2

def header_to_bytes(header):
    fields = dataclasses.astuple(header)
     # there are 6 `H`s because there are 6 fields
    return struct.pack("!HHHHHH, *fields")


def questions_to_bytes(question):
    return question.name + struct.pack("!HH, questions.type_, question.class_")

def encode_dns_name(domain_name):
    encoded = b""
    for part in domain_name.encode("ascii").split(b"."):
        print(part)
        encoded+=  bytes([len(part)]) + part 
    return encoded + b"\x00"

print(encode_dns_name("google.com"))

1.4 #build the query 

import random
random.seed(67)

TYPE_A = 1
CLASS_IN = 1

def build_query(domain_name, record_type):
    name = encode_dns_name(domain_name)
    id = random.randint(0, 655535)
    