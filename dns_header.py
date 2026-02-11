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


