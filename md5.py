import struct
from math import floor, sin
from bitarray import bitarray
import hashlib

f = open('test.txt','rb')
bit_array = bitarray(endian="big")
bit_array.fromfile(f)
file_bitarray = bit_array.copy()
# print(file_bitarray)
# print(bit_array)
# print('\n')
bit_array.append(1)
# print(len(bit_array))
while len(bit_array) % 512 != 448:
    bit_array.append(0)

bit_array = bitarray(bit_array, endian='little')
# print(bit_array, len(bit_array), '\n')

length = len(file_bitarray) % pow(2, 64)
# print(length)
length_bit_array = bitarray(endian="little")
length_bit_array.frombytes(struct.pack("<Q", length))

temp = bit_array.copy()
temp.extend(length_bit_array)
# print(temp)

A = 0x67452301
B = 0xEFCDAB89
C = 0x98BADCFE
D = 0x10325476

F = lambda x, y, z: (x & y) | (~x & z)
G = lambda x, y, z: (x & z) | (y & ~z)
H = lambda x, y, z: x ^ y ^ z
I = lambda x, y, z: y ^ (x | ~z)

# Define the left rotation function, which rotates `x` left `n` bits.
rotate_left = lambda x, n: (x << n) | (x >> (32 - n))

# Define a function for modular addition.
modular_add = lambda a, b: (a + b) % pow(2, 32)

# Compute the T table from the sine function. Note that the
# RFC starts at index 1, but we start at index 0.
T = [floor(pow(2, 32) * abs(sin(i + 1))) for i in range(64)]

# The total number of 32-bit words to process, N, is always a
# multiple of 16.
N = len(temp) // 32

for chunk_index in range(N // 16):
    # Break the chunk into 16 words of 32 bits in list X.
    start = chunk_index * 512
    X = [temp[start + (x * 32) : start + (x * 32) + 32] for x in range(16)]

    # Convert the `bitarray` objects to integers.
    X = [int.from_bytes(word.tobytes(), byteorder="little") for word in X]

    # Execute the four rounds with 16 operations each.
    for i in range(4 * 16):
        if 0 <= i <= 15:
            k = i
            s = [7, 12, 17, 22]
            temp = F(B, C, D)
        elif 16 <= i <= 31:
            k = ((5 * i) + 1) % 16
            s = [5, 9, 14, 20]
            temp = G(B, C, D)
        elif 32 <= i <= 47:
            k = ((3 * i) + 5) % 16
            s = [4, 11, 16, 23]
            temp = H(B, C, D)
        elif 48 <= i <= 63:
            k = (7 * i) % 16
            s = [6, 10, 15, 21]
            temp = I(B, C, D)

        # The MD5 algorithm uses modular addition. Note that we need a
        # temporary variable here. If we would put the result in `A`, then
        # the expression `A = D` below would overwrite it. We also cannot
        # move `A = D` lower because the original `D` would already have
        # been overwritten by the `D = C` expression.
        temp = modular_add(temp, X[k])
        temp = modular_add(temp, T[i])
        temp = modular_add(temp, A)
        temp = rotate_left(temp, s[i % 4])
        temp = modular_add(temp, B)

        # Swap the registers for the next operation.
        A = D
        D = C
        C = B
        B = temp

    # Update the buffers with the results from this chunk.
    A = modular_add(A, 0x67452301)

    B = modular_add(B, 0xEFCDAB89)
    C = modular_add(C, 0x98BADCFE)
    D = modular_add(D, 0x10325476)

A = struct.unpack("<I", struct.pack(">I", A))[0]
B = struct.unpack("<I", struct.pack(">I", B))[0]
C = struct.unpack("<I", struct.pack(">I", C))[0]
D = struct.unpack("<I", struct.pack(">I", D))[0]

# Output the buffers in lower-case hexadecimal format.
result = f"{format(A, '08x')}{format(B, '08x')}{format(C, '08x')}{format(D, '08x')}"

print(result)

with open("test2.mov","rb") as f:
    bytes = f.read() # read file as bytes
    readable_hash = hashlib.md5(bytes).hexdigest();
    print(readable_hash)