import socket,struct

# Default packets
# headers
packet_id = 1234             # Packet Identifier (ID) - 16 bits
qr = 1                       # Query/Response Indicator (QR) - 1 bit
opcode = 0                   # Operation Code (OPCODE) - 4 bits
aa = 0                       # Authoritative Answer (AA) - 1 bit
tc = 0                       # Truncation (TC) - 1 bit
rd = 0                       # Recursion Desired (RD) - 1 bit
ra = 0                       # Recursion Available (RA) - 1 bit
z = 0                        # Reserved (Z) - 3 bits
rcode = 0                    # Response Code (RCODE) - 4 bits
# one question for this
qdcount = 1                  # Question Count (QDCOUNT) - 16 bits
# one answer
ancount = 1                 # Answer Record Count (ANCOUNT) - 16 bits
nscount = 0                  # Authority Record Count (NSCOUNT) - 16 bits
arcount = 0                  # Additional Record Count (ARCOUNT) - 16 bits


def get_headers(query:bytes):
    """
        returns -> 12 byte long data
    """
    packet_id = int.from_bytes(query[:2])
    twelve_bytes = "H"*6
    flags = ""
    # adding values to flag based on their individual bits size
    # it will be a long binary string
    flags+=str(qr)
    flags+=str(opcode).zfill(4)
    flags+=str(aa) + str(tc) + str(rd) + str(ra)
    flags+=str(z).zfill(3)
    flags+=str(rcode).zfill(4)
    # turning it into 2 bytes integer
    flags = int(flags,2)
    return struct.pack(f"!{twelve_bytes}", packet_id, flags, qdcount, ancount, nscount, arcount)

def get_question(query:bytes):
    """
        b'\x06google\x03com\x00\x00\x01\x00\x01'
        here \x06google\x03com\ is the domain of the format <length><content>
        '\x00' marks the end
        '\x00\x01' is the type of the dns record
        '\x00\x01' is the class of the record
        
        question type -> 2byte int
        the decoded value is an int and values for various types A -> value is 1, CNAME -> value is 5

        question class -> 2byte int
        the decoded value is an int and values for various types IN -> 1
    """
    # variable size
    question = query[12:]
    print(question)
    for idx,bytes in enumerate(question):
        if bytes == 0:
            break
    qname = question[:idx]
    qtype = question[idx+1:idx+3]
    qclass = question[idx+3:idx+5]
    # adding the extra b"\x00" bytes as we are skipp bytes==0 so we need to add that
    return qname+b"\x00"+qtype+qclass

def get_answer(query: bytes):
    # similar to the question
    after_headers = query[12:]
    idx = 0
    while after_headers[idx] != 0:
        idx += after_headers[idx] + 1
    
    qname = after_headers[:idx+1]
    
    qtype = after_headers[idx+1:idx+3]   # 2 bytes for qtype
    qclass = after_headers[idx+3:idx+5]  # 2 bytes for qclass
    
    # Create the TTL and resource data length fields (assuming A record, 4 bytes for IPv4 address)
    ttl = struct.pack("!I", 60)  # TTL should be 4 bytes
    rlength = struct.pack("!H", 4)  # Data length for an IPv4 address (4 bytes)
    
    # Assuming the answer is an A record with IP 8.8.8.8
    data = b"\x08\x08\x08\x08"  # IP address 8.8.8.8 (in raw bytes)
    
    return qname + qtype + qclass + ttl + rlength + data

def main():
    print("Logs from your program will appear here!")

    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(("127.0.0.1", 2053))
    print("Server is running on 127.0.0.1:2053")
    while True:
        try:
            buf, source = udp_socket.recvfrom(512)
            headers = get_headers(buf)
            question = get_question(buf)
            ans = get_answer(buf)
            response = headers+question+ans
            udp_socket.sendto(response, source)
        except Exception as e:
            print(f"Error receiving data: {e}")
            break


if __name__ == "__main__":
    main()
