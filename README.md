# Python DNS Client

A simple, manual implementation of the DNS protocol in Python. This project demonstrates how to construct DNS headers and question sections from scratch using raw bytes.

## Features
- Custom `DNSHeader` and `DNSQuestion` classes.
- `header_to_bytes` conversion using struct packing.
- `question_to_bytes` conversion with domain name encoding.

## Usage
Run the script to see the byte output of a standard DNS query for `google.com`.