import binascii, sys, os.path

integer_sine = [0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee, 0xf57c0faf, 
                0x4787c62a, 0xa8304613, 0xfd469501, 0x698098d8, 0x8b44f7af,
                0xffff5bb1, 0x895cd7be, 0x6b901122, 0xfd987193, 0xa679438e, 
                0x49b40821, 0xf61e2562, 0xc040b340, 0x265e5a51, 0xe9b6c7aa, 
                0xd62f105d, 0x2441453, 0xd8a1e681, 0xe7d3fbc8, 0x21e1cde6, 
                0xc33707d6, 0xf4d50d87, 0x455a14ed, 0xa9e3e905, 0xfcefa3f8, 
                0x676f02d9, 0x8d2a4c8a, 0xfffa3942, 0x8771f681, 0x6d9d6122, 
                0xfde5380c, 0xa4beea44, 0x4bdecfa9, 0xf6bb4b60, 0xbebfbc70, 
                0x289b7ec6, 0xeaa127fa, 0xd4ef3085, 0x4881d05, 0xd9d4d039,
                0xe6db99e5, 0x1fa27cf8, 0xc4ac5665, 0xf4292244, 0x432aff97,
                0xab9423a7, 0xfc93a039, 0x655b59c3, 0x8f0ccc92, 0xffeff47d, 
                0x85845dd1, 0x6fa87e4f, 0xfe2ce6e0, 0xa3014314, 0x4e0811a1, 
                0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391]

shifts = [[7, 12, 17, 22], [5,  9, 14, 20], [4, 11, 16, 23], [6, 10, 15, 21]]

def left_rotate(k,bits):
    bits %= 32
    k %= 2**32
    upper = (k<<bits) % (2**32)
    result = upper | (k>>(32-(bits)))
    return result

def fmt8(num):
    bighex = "{0:08x}".format(num)
    binver = binascii.unhexlify(bighex)
    result = "{0:08x}".format(int.from_bytes(binver,byteorder='little'))
    return result

def md5sum(msg):
    msg_length = len(msg) * 8 % (2**64)
    msg += b'\x80'
    zeros = (448 - (msg_length + 8) % 512) % 512 // 8
    msg += b'\x00' * zeros 

    result = [msg_length, zeros * 8]

    msg += msg_length.to_bytes(8, byteorder='little')

    result.append(bin(msg_length)[2:])

    chunks = len(msg) * 8 // 512

    a0 = 0x67452301
    b0 = 0xefcdab89
    c0 = 0x98badcfe
    d0 = 0x10325476

    for i in range(0, chunks):
        A = a0
        B = b0
        C = c0
        D = d0

        block = msg[i * 64 : (i + 1) * 64]
        
        M = []
        for j in range(16):
            M.append(int.from_bytes(block[j * 4 : (j+1) * 4], byteorder="little"))

        for j in range(64):
            quarter = j // 16
            if quarter == 0:
                F = B & C | ~B & D
                g = j
            elif quarter == 1:
                F = B & D | C & ~D
                g = (5 * j + 1) % 16
            elif quarter == 2:
                F = B ^ C ^ D
                g = (3 * j + 5) % 16
            elif quarter == 3:
                F = C ^ (B | ~D)
                g = (7 * j) % 16
            F = F + A + integer_sine[j] + M[g]
            A = D
            D = C
            C = B
            B = B + left_rotate(F, shifts[quarter][j % 4])

        a0 = (a0 + A) % (2**32)
        b0 = (b0 + B) % (2**32)
        c0 = (c0 + C) % (2**32)
        d0 = (d0 + D) % (2**32)

    result.append(fmt8(a0)+fmt8(b0)+fmt8(c0)+fmt8(d0))
    return result