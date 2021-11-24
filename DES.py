from typing import List
from bitarray import bitarray
from bitarray.util import ba2int

IP = [[58, 50, 42, 34, 26, 18, 10, 2],
      [60, 52, 44, 36, 28, 20, 12, 4],
      [62, 54, 46, 38, 30, 22, 14, 6],
      [64, 56, 48, 40, 32, 24, 16, 8],
      [57, 49, 41, 33, 25, 17, 9, 1],
      [59, 51, 43, 35, 27, 19, 11, 3],
      [61, 53, 45, 37, 29, 21, 13, 5],
      [63, 55, 47, 39, 31, 23, 15, 7]]

IP_Inv = [[40, 8, 48, 16, 56, 24, 64, 32],
          [39, 7, 47, 15, 55, 23, 63, 31],
          [38, 6, 46, 14, 54, 22, 62, 30],
          [37, 5, 45, 13, 53, 21, 61, 29],
          [36, 4, 44, 12, 52, 20, 60, 28],
          [35, 3, 43, 11, 51, 19, 59, 27],
          [34, 2, 42, 10, 50, 18, 58, 26],
          [33, 1, 41, 9, 49, 17, 57, 25]]

E = [[32, 1, 2, 3, 4, 5],
     [4, 5, 6, 7, 8, 9],
     [8, 9, 10, 11, 12, 13],
     [12, 13, 14, 15, 16, 17],
     [16, 17, 18, 19, 20, 21],
     [20, 21, 22, 23, 24, 25],
     [24, 25, 26, 27, 28, 29],
     [28, 29, 30, 31, 32, 1]]

P = [[16, 7, 20, 21, 29, 12, 28, 17],
     [1, 15, 23, 26, 5, 18, 31, 10],
     [2, 8, 24, 14, 32, 27, 3, 9],
     [19, 13, 30, 6, 22, 11, 4, 25]]

PC1 = [[57, 49, 41, 33, 25, 17, 9],
       [1, 58, 50, 42, 34, 26, 18],
       [10, 2, 59, 51, 43, 35, 27],
       [19, 11, 3, 60, 52, 44, 36],
       [63, 55, 47, 39, 31, 23, 15],
       [7, 62, 54, 46, 38, 30, 22],
       [14, 6, 61, 53, 45, 37, 29],
       [21, 13, 5, 28, 20, 12, 4]]

LeftShiftSched = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

PC2 = [[14, 17, 11, 24, 1, 5],
       [3, 28, 15, 6, 21, 10],
       [23, 19, 12, 4, 26, 8],
       [16, 7, 27, 20, 13, 2],
       [41, 52, 31, 37, 47, 55],
       [30, 40, 51, 45, 33, 48],
       [44, 49, 39, 56, 34, 53],
       [46, 42, 50, 36, 29, 32]]

S1 = [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
      [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
      [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
      [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]]

S2 = [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
      [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
      [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
      [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]]

S3 = [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
      [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
      [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
      [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]]

S4 = [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
      [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
      [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
      [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]]

S5 = [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
      [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
      [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
      [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]]

S6 = [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
      [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
      [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
      [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]]

S7 = [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
      [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
      [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
      [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]]

S8 = [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
      [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
      [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
      [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]


def file_to_bits(file_path: str) -> bitarray:
    fl = open(file_path, 'rb')
    bit_array = bitarray(endian="big")
    bit_array.fromfile(fl)

    file_bitarray = bit_array.copy()
    return file_bitarray


def apply_transformation(input_string: bitarray, transform):
    out: bitarray = bitarray()
    for i in range(len(transform)):
        for j in range(len(transform[i])):
            out.append(input_string[transform[i][j] - 1])

    return out


def left_shift(input_string: bitarray, num_shifts: int):
    return input_string[num_shifts:] + input_string[0:num_shifts]


def generate_keys(input_key: str):
    if len(input_key) != 16:
        raise ValueError("Key should be a 16 hexadecimal digit input")

    binary_key = bitarray(bin(int(input_key, 16))[2:].zfill(64))
    k_plus = apply_transformation(binary_key, PC1)

    keys: List[bitarray] = [bitarray()] * 16
    mid_index = int(len(k_plus) / 2)
    C: list = [k_plus[0:mid_index], ]
    D: list = [k_plus[mid_index:], ]
    for i in range(1, len(keys) + 1):
        C.append(left_shift(C[i - 1], LeftShiftSched[i - 1]))
        D.append(left_shift(D[i - 1], LeftShiftSched[i - 1]))
        keys[i - 1] = apply_transformation(C[i] + D[i], PC2)

    return keys


def s_box(input_bits: bitarray, s_box_num: int):
    i = ba2int(input_bits[0::5])
    j = ba2int(input_bits[1:5])
    s_box_table = globals()['S' + str(s_box_num)]

    out = bitarray(bin(s_box_table[i][j])[2:].zfill(4))
    return out


def f(input_string: bitarray, input_key: bitarray):
    input_string = apply_transformation(input_string, E)
    input_string = input_key ^ input_string
    B = [input_string[i:i + 6] for i in range(0, len(input_string), 6)]
    F = bitarray()
    for i in range(len(B)):
        F += (s_box(B[i], i + 1))
    F = apply_transformation(F, P)

    return F


def encrypt(input_binary_file: bitarray, input_key: str, is_encryption: bool):
    keys = generate_keys(input_key)
    print('DES Cryptography Tool: Keys Generated')
    if not is_encryption:
        keys.reverse()

    blocks: List[bitarray] = []
    for i in range(int(len(input_binary_file) / 64)):
        blocks.append(input_binary_file[64 * i:64 * (i + 1)])

    # blocks = [bitarray('0000000100100011010001010110011110001001101010111100110111101111')]  # for testing
    # blocks = [bitarray('1000010111101000000100110101010000001111000010101011010000000101')]  # for testing

    output = bitarray()
    for m in blocks:
        messageIP = apply_transformation(m, IP)
        size = int(len(messageIP) / 2)
        L = [messageIP[0:size], ]
        R = [messageIP[size:], ]

        for i in range(1, 17):
            L.append(R[i - 1])
            R.append(L[i - 1] ^ f(R[i - 1], keys[i - 1]))

        output += apply_transformation(R[16] + L[16], IP_Inv)

    print('Original Message: ')
    print(input_binary_file)
    print('Cipher Message: ')
    print(output)

    return output


def encrypt_file(file_path: str, input_key: str, is_encryption: bool = True) -> bitarray:
    input_binary_file = file_to_bits(file_path)
    print('DES Cryptography Tool: File Initialized')

    return encrypt(input_binary_file, input_key, is_encryption)


if __name__ == '__main__':
    path = '/Users/aishwarya/Documents/PycharmProjects/DES_Crypto/testFiles/test1.txt'
    key = '133457799BBCDFF1'
    cipher = encrypt_file(path, key, True)
    decipher = encrypt(cipher, key, False)
