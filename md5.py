import struct
from math import floor, sin
from bitarray import bitarray
import hashlib

f = open('test1.txt','rb')
bit_array = bitarray(endian="big")
bit_array.fromfile(f)

file_bitarray = bit_array.copy()

bit_array.append(1)
while len(bit_array) % 512 != 448:
    bit_array.append(0)

padded_bit_array = bitarray(bit_array, endian='little')

length = len(file_bitarray) % pow(2, 64)
length_bit_array = bitarray(endian="little")
length_bit_array.frombytes(struct.pack("<Q", length))

padded_bit_array.extend(length_bit_array)

A = 0x67452301
B = 0xEFCDAB89
C = 0x98BADCFE
D = 0x10325476

with open('test2.mov', 'rb') as f:
    bytes = f.read() # read file as bytes
    readable_hash = hashlib.md5(bytes).hexdigest();
    print(readable_hash)