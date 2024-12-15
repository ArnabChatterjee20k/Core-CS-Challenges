# data = b'\x06google\x03com\x00\x00\x01\x00\x01'
data = b'\x0ccodecrafters\x02io\x00\x00\x01\x00\x01'
domain = ""
qclass = ""
qtype = ""
for idx,d in enumerate(data):
    if d==0 and not domain:
        break

domain = data[:idx]
qtype = data[idx+1:idx+3] # 2bytes
qclass = data[idx+3:idx+5] # 2bytes
print(domain.decode(),+ int.from_bytes(qtype),+ int.from_bytes(qclass))