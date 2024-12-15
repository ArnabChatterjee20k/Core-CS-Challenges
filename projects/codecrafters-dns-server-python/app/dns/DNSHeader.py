import struct
from .utils import get_encoded
# DNS Packet Fields with Expected Values
# Header size 12 bytes

# Default packets
packet_id = 1234             # Packet Identifier (ID) - 16 bits
qr = 1                       # Query/Response Indicator (QR) - 1 bit
opcode = 0                   # Operation Code (OPCODE) - 4 bits
aa = 0                       # Authoritative Answer (AA) - 1 bit
tc = 0                       # Truncation (TC) - 1 bit
rd = 0                       # Recursion Desired (RD) - 1 bit
ra = 0                       # Recursion Available (RA) - 1 bit
z = 0                        # Reserved (Z) - 3 bits
rcode = 0                    # Response Code (RCODE) - 4 bits
qdcount = 0                  # Question Count (QDCOUNT) - 16 bits
ancount = 0                  # Answer Record Count (ANCOUNT) - 16 bits
nscount = 0                  # Authority Record Count (NSCOUNT) - 16 bits
arcount = 0                  # Additional Record Count (ARCOUNT) - 16 bits


def get_headers(query:bytes):
    """
        returns -> 12 byte long data
    """
    packet_id = int.from_bytes(query[:2])
    twelve_bytes = "H"*6
    flags = struct.pack("!HH",qr , opcode , aa , tc , rd , ra , z , rcode)
    return struct.pack(f"!{twelve_bytes}", packet_id, flags, qdcount, ancount, nscount, arcount)
