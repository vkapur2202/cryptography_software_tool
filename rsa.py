# rsa
# Jeffrey Kozik

num_bytes_in_block = 1
prime_bit = 64

import random # to generate random n-bit numbers and find large prime numbers
import time

start = time.time()

# bit array of file
def file_to_bits(file_path):
    L = ""
    return_array = []
    byte_array = file_path.read()
    for byte in byte_array:
        L += (bin(byte)[2:]).zfill(8)
        print("byte", byte)
    print(L)
    current_position = 0
    while current_position < len(L):
        if (current_position + 8*(num_bytes_in_block)) >= (len(L) - 1):
            return_array.append(int(L[current_position:], 2))
        else:
            return_array.append(int(L[current_position:(current_position + 8*num_bytes_in_block)], 2))
        current_position += num_bytes_in_block*8
    for block in return_array:
        print("block", block)
    return return_array

# because regular pow function in python is inaccurate with large numbers
def mypow(base, exponent, mod):
    # pow(base, exponent, mod)
    res = 1

    if ((base := base % mod) == 0):
        return 0

    while (exponent > 0):
        if ((exponent&1) == 1):
            res = (res*base) % mod

        exponent = exponent >> 1
        base = (base*base) % mod
    return res

# generate many n bit numbers until you find one that is (probably) prime
def randomNBitNumber(n):
    return (random.randrange(((2**(n-1)) + 1), ((2**n) - 1)))

first100Primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
                    31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
                    73, 79, 83, 89, 97, 101, 103, 107, 109, 113,
                    127, 131, 137, 139, 149, 151, 157, 163, 167, 173,
                    179, 181, 191, 193, 197, 199, 211, 223, 227, 229,
                    233, 239, 241, 251, 257, 263, 269, 271, 277, 281,
                    283, 293, 307, 311, 313, 317, 331, 337, 347, 349,
                    353, 359, 367, 373, 379, 383, 389, 397, 401, 409,
                    419, 421, 431, 433, 439, 443, 449, 457, 461, 463,
                    467, 479, 487, 491, 499, 503, 509, 521, 523, 541]

# naive check to filter out numbers that are obviously not prime
def getNumberNotDivisibleByFirst100Primes(n):
    while True:
        randomNumber = randomNBitNumber(n)
        isComposite = True
        for prime in first100Primes:
            if randomNumber % prime == 0:
                isComposite = False
                break
        if (isComposite):
            return randomNumber

# might not actually be prime if it passes this test (only 75% chance it is)
# When run 20 times 1 - (0.75^20) chance it is
def passedMillerRabin(potentialPrime):
    evenComponent = potentialPrime - 1
    r = 0
    while evenComponent % 2 == 0:
        evenComponent >>= 1
        r += 1
    assert(2**r * evenComponent == potentialPrime - 1)

    def isComposite(a):
        if mypow(a, evenComponent, potentialPrime) == 1:
            return False
        for i in range(r):
            if mypow(a, 2**i * evenComponent, potentialPrime) == potentialPrime - 1:
                return False
        return True

    numberOfTrials = 20
    for i in range(numberOfTrials):
        a = random.randrange(2, potentialPrime)
        if isComposite(a):
            return False
    return True

# for computing p & q
def chooseLargePrime(n):
    while True:
        potentialPrime = getNumberNotDivisibleByFirst100Primes(n)
        if(passedMillerRabin(potentialPrime)):
            return potentialPrime

# 65537 is always relatively prime to phi(n) when n is large enough
def chooseE(n, phiN):
    return 65537
    # return 3

# ed mod phi(n) = 1
def computeD(e, phiN):
    a = 0
    b = phiN
    u = 1
    x = e
    while x > 0:
        q = b // x
        oldX = x
        oldA = a
        oldB = b
        oldU = u
        x = oldB % oldX
        a = oldU
        b = oldX
        u = oldA - q * oldU
    if b == 1:
        return a % phiN

def generatePublicAndPrivateKey(steps):
    p = chooseLargePrime(prime_bit) # 1024-2048 bit prime numbers used in industry
    if (not "Alice p" in steps):
        steps["Alice p"] = p
    else:
        steps["Bob p"] = p
    # print("p", p)
    q = chooseLargePrime(prime_bit)
    if (not "Alice q" in steps):
        steps["Alice q"] = q
    else:
        steps["Bob q"] = q
    # print("q", q)
    n = p*q
    if (not "Alice n" in steps):
        steps["Alice n"] = n
    else:
        steps["Bob n"] = n
    phiN = p*q - p - q + 1
    if (not "Alice phiN" in steps):
        steps["Alice phiN"] = phiN
    else:
        steps["Bob phiN"] = phiN
    print("phiN", phiN)
    e = chooseE(n, phiN)
    if (not "Alice e" in steps):
        steps["Alice e"] = e
    else:
        steps["Bob e"] = e
    print("e", e)
    d = computeD(e, phiN)
    if (not "Alice d" in steps):
        steps["Alice d"] = d
    else:
        steps["Bob d"] = d
    print("d", d)
    publicKey = [e, n]
    privateKey = d
    return publicKey, privateKey

def encipherMessageForIntegrityAndAuthentication(m, d, n):
    c = []
    for block in m:
        c.append(mypow(block, d, n))
    return c

def decipherMessageForIntegrityAndAuthentication(c, publicKey):
    m = []
    for block in c:
        m.append(mypow(block, publicKey[0], publicKey[1]))
    return m

# def encipherMessageForConfidentiality(m, publicKey):
#     c = []
#     for big_block in m:
#         # turn block into binary, break block into smaller int blocks, encrypt blocks
#         binary_big_block = bin(big_block)[2:]
#         print("binary_big_block", binary_big_block)
#         mini_block_array = []
#         current_position = 0
#         while current_position < len(binary_big_block):
#             if (current_position + 8*(num_bytes_in_block)) >= (len(binary_big_block) - 1):
#                 print("binary_big_block[" , current_position , ":]", binary_big_block[current_position:])
#                 mini_block_array.append(int(binary_big_block[current_position:], 2))
#             else:
#                 print("binary_big_block[", current_position, ":" , str(current_position + 8*num_bytes_in_block) , "]", binary_big_block[current_position:(current_position + 8*num_bytes_in_block)])
#                 mini_block_array.append(int(binary_big_block[current_position:(current_position + 8*num_bytes_in_block)], 2))
#             current_position += num_bytes_in_block*8
#         print(mini_block_array)
#         mini_block_cs = []
#         for mini_block in mini_block_array:
#             mini_block_cs.append(mypow(mini_block, publicKey[0], publicKey[1]))
#         c.append(mini_block_cs)
#     return c

# def decipherMessageForConfidentiality(c, d, n, num_zeros):
#     m = []
#     for big_array_block in c:
#         # decrypt blocks, combine smaller int blocks into larger binary, turn binary into int
#         mini_block_ms = []
#         for cs in big_array_block:
#             mini_block_ms.append(mypow(cs, d, n))
#         print("mini_block_ms", mini_block_ms)
#         m_binary_string = ""
#         count = 0
#         while count < len(mini_block_ms):
#             if (count == (len(mini_block_ms) - 1)):
#                 print("bin(mini_block_ms[", count, "])[2:]", bin(mini_block_ms[count])[2:])
#                 m_binary_string += (bin(mini_block_ms[count])[2:])
#             else:
#                 print("(bin(mini_block_ms[", count, "])[2:]).zfill(", 8*num_bytes_in_block, ")", bin(mini_block_ms[count])[2:].zfill(8*num_bytes_in_block))
#                 m_binary_string += (bin(mini_block_ms[count])[2:]).zfill(8*num_bytes_in_block)
#             count += 1
#         int_m = int(m_binary_string, 2)
#         m.append(int_m)
#     return m

def encipherMessageForConfidentiality(m, publicKey):
    c = []
    for block in m:
        c.append(mypow(block, publicKey[0], publicKey[1]))
    return c

def decipherMessageForConfidentiality(c, d, n):
    m = []
    for block in c:
        m.append(mypow(block, d, n))
    return m

def rsaForConfidentialityIntegrityAndAuthentication(steps, aliceMessage):
    alicePublicKey, alicePrivateKey = generatePublicAndPrivateKey(steps)
    print("Alice's Public Key: ")
    print(alicePublicKey[0])
    print(alicePublicKey[1])
    print("Alice's Private Key: ")
    print(alicePrivateKey)
    bobPublicKey, bobPrivateKey = generatePublicAndPrivateKey(steps)
    print("Bob's Public Key: ")
    print(bobPublicKey[0])
    print(bobPublicKey[1])
    print("Bob's Private Key: ")
    print(bobPrivateKey)
    print("Alice's Message: ", aliceMessage)
    aliceMessageEncryptedForIntegrityAndAuthentication = encipherMessageForIntegrityAndAuthentication(aliceMessage, alicePrivateKey, alicePublicKey[1])
    steps["aliceMessageEncryptedForIntegrityAndAuthentication"] = aliceMessageEncryptedForIntegrityAndAuthentication
    print("Alice's Message Encrypted for Integrity and Authentication: ", aliceMessageEncryptedForIntegrityAndAuthentication)
    aliceMessageEncryptedForConfidentialityIntegrityAndAuthentication = encipherMessageForConfidentiality(aliceMessageEncryptedForIntegrityAndAuthentication, bobPublicKey)
    steps["aliceMessageEncryptedForConfidentialityIntegrityAndAuthentication"] = aliceMessageEncryptedForConfidentialityIntegrityAndAuthentication
    print("Alice's Message Encrypted for Confidentiality, Integrity, and Authentication: ", aliceMessageEncryptedForConfidentialityIntegrityAndAuthentication)
    aliceMessageDecryptedForConfidentiality = decipherMessageForConfidentiality(aliceMessageEncryptedForConfidentialityIntegrityAndAuthentication, bobPrivateKey, bobPublicKey[1])
    steps["aliceMessageDecryptedForConfidentiality"] = aliceMessageDecryptedForConfidentiality
    print("Alice's Message Decrypted for Confidentiality: ", aliceMessageDecryptedForConfidentiality)
    aliceMessageDecryptedForConfidentialityIntegrityAndAuthentication = decipherMessageForIntegrityAndAuthentication(aliceMessageDecryptedForConfidentiality, alicePublicKey)
    steps["aliceMessageDecryptedForConfidentialityIntegrityAndAuthentication"] = aliceMessageDecryptedForConfidentialityIntegrityAndAuthentication
    print("Alice's Message Decrypted for Confidentiality, Integrity, and Authentication: ", aliceMessageDecryptedForConfidentialityIntegrityAndAuthentication)

def rsa(file):
    aliceMessage = file_to_bits(file)
    done = False
    # basically what's happening here is that sometimes it doesn't work because Bn > An so when it's encrypting for confidentiality it doesn't work
    # so it keeps running until it works. I tried to solve this problem by breaking the intermediate encryption into smaller blocks but that didn't work
    while(not done):
        steps = {}
        print("file", file)
        rsaForConfidentialityIntegrityAndAuthentication(steps, aliceMessage)
        aliceLength = len(steps['aliceMessageDecryptedForConfidentialityIntegrityAndAuthentication'])
        if(aliceLength > 0):
            count = 0
            for char in steps['aliceMessageDecryptedForConfidentialityIntegrityAndAuthentication']:
                print(char)
                if (char > 255):
                    print("char too long")
                    print(char)
                    break
                count += 1
            print("count", count)
            print("aliceLength", aliceLength)
            print(done)
            if(count == aliceLength):
                done = True
    end = time.time()
    print("time elapsed", end - start)
    return steps["Alice p"], steps["Alice q"], steps["Bob p"], steps["Bob q"], steps["Alice n"], steps["Alice phiN"], steps["Bob n"], steps["Bob phiN"], steps["Alice d"], steps["Bob d"], steps['aliceMessageEncryptedForIntegrityAndAuthentication'], steps['aliceMessageEncryptedForConfidentialityIntegrityAndAuthentication'], steps['aliceMessageDecryptedForConfidentiality'], steps['aliceMessageDecryptedForConfidentialityIntegrityAndAuthentication']
