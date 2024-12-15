import struct
def get_encoded(value,format="!i"):
    return struct.pack(format,value)