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
    return struct.pack("!HHHHHH", *fields)


def questions_to_bytes(question):
    return question.name + struct.pack("!HH", question.type_, question.class_) #proper format byte

def encode_dns_name(domain_name):
    encoded = b"" # empty binary string 
    for part in domain_name.encode("ascii").split(b"."):
        print(part)
        encoded+=  bytes([len(part)]) + part 
    return encoded + b"\x00"

#print(encode_dns_name("google.com"))

1.4 #build the query 

import random
random.seed(2)

TYPE_A = 1
CLASS_IN = 1

def build_query(domain_name, record_type):
    name = encode_dns_name(domain_name)
    id = random.randint(0, 65535)
    #1 << 8 means shift the bit to the left by 8 positions which is the RD position that we set to 1 in the flags fields of the header
    RECURSION = 1 << 8
    header = DNSHeader(id=id, num_questions=1, flags=RECURSION) 
    question = DNSQuestion(name=name,type_=record_type,class_=CLASS_IN)
    return header_to_bytes(header) + questions_to_bytes(question)

#need to finish the build query function




'''
print(header_to_bytes(DNSHeader(id=0x1314, flags=0, num_questions=1, num_additionals=0, num_authorities=0, num_answers=0)))

print(build_query("example.com", TYPE_A))
 ---> will return b'\x1c\xf4\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x07example\x03com\x00\x00\x01\x00\x01'
given that  '\x1c\xf4\' =  unique id in base64 hex
01 00 is the recursion desired at the 8 place tks to RECURSION variable 
00 01 is the nm questions 
and other explain before 

'''

1.5

import socket


query = build_query("www.example.com", 1)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
'''
socket to communicate 
af_inet connecting trough internet
dgram means protocol is UDP so no connection just send and receive.

'''
print(sock.sendto(query,("8.8.8.8",53)))

response, _ = sock.recvfrom(1024)
print(response,)