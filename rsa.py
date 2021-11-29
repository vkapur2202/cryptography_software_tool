# rsa
# Jeffrey Kozik

import random
import os

file = "testFiles/test1.txt"

def file_to_bits(file_path):
    L = []
    file = open(file_path, "rb")
    byte = file.read(1)
    int_val = int.from_bytes(byte, "big")
    # print(int_val)
    L.append(int_val)
    while byte:
        # print(byte)
        byte = file.read(1)
        int_val = int.from_bytes(byte, "big")
        # print(int_val)
        L.append(int_val)
    file.close()

    return L

def create_file(file, int_array, new_name):
    L = []
    for int in int_array:
        print("Int", int)
        num = 1
        while True:
            try:
                this_byte = int.to_bytes(num, "big")
                break
            except:
                num += 1
        print("this_byte", this_byte)
        L.append(this_byte)
    directory_name = os.path.dirname(file)
    print("d name!!!", directory_name)
    file_name = ""
    extension = ""
    append_file_name = True
    for char in file:
        if(append_file_name):
            if (char != "."):
                file_name += char
            else:
                append_file_name = False
        else:
            extension += char
    this_files_name = file_name + "_" + new_name + "." + extension
    f = open(this_files_name, 'x')
    f.close()
    f = open(this_files_name, 'wb')
    for byte in L:
        f.write(byte)
    f.close()

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

def passedMillerRabin(potentialPrime):
    evenComponent = potentialPrime - 1
    r = 0
    while evenComponent % 2 == 0:
        evenComponent >>= 1
        r += 1
    assert(2**r * evenComponent == potentialPrime - 1)

    def isComposite(a):
        if pow(a, evenComponent, potentialPrime) == 1:
            return False
        for i in range(r):
            if pow(a, 2**i * evenComponent, potentialPrime) == potentialPrime - 1:
                return False
        return True

    numberOfTrials = 20
    for i in range(numberOfTrials):
        a = random.randrange(2, potentialPrime)
        if isComposite(a):
            return False
    return True

def chooseLargePrime(n):
    while True:
        potentialPrime = getNumberNotDivisibleByFirst100Primes(n)
        if(passedMillerRabin(potentialPrime)):
            return potentialPrime

def chooseE(n, phiN):
    return 65537

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

def generatePublicAndPrivateKey():
    p = chooseLargePrime(1024)
    q = chooseLargePrime(1024)
    n = p*q
    phiN = p*q - p - q + 1
    e = chooseE(n, phiN)
    d = computeD(e, phiN)
    publicKey = [e, n]
    privateKey = d
    return publicKey, privateKey

def encipherMessageForConfidentiality(m, publicKey):
    c = []
    for block in m:
        c.append(pow(block, publicKey[0], publicKey[1]))
    return c

def decipherMessageForConfidentiality(c, d, n):
    m = []
    for block in c:
        m.append(pow(block, d, n))
    return m

def encipherMessageForIntegrityAndAuthentication(m, d, n):
    c = []
    for block in m:
        c.append(pow(block, d, n))
    return c

def decipherMessageForIntegrityAndAuthentication(c, publicKey):
    m = []
    for block in c:
        m.append(pow(block, publicKey[0], publicKey[1]))
    return m

def rsaForConfidentiality(file):
    alicePublicKey, alicePrivateKey = generatePublicAndPrivateKey()
    print("Alice's Public Key: ")
    print(alicePublicKey[0])
    print(alicePublicKey[1])
    bobMessage = file_to_bits(file)
    print("Bob's Message: ", bobMessage)
    bobMessageEncryptedForConfidentiality = encipherMessageForConfidentiality(bobMessage, alicePublicKey)
    create_file(file, bobMessageEncryptedForConfidentiality, "bobMessageEncryptedForConfidentiality")
    print("Bob's Message Encrypted for Confidentiality: ", bobMessageEncryptedForConfidentiality)
    bobMessageDecryptedForConfidentiality = decipherMessageForConfidentiality(bobMessageEncryptedForConfidentiality, alicePrivateKey, alicePublicKey[1])
    create_file(file, bobMessageDecryptedForConfidentiality, "bobMessageDecryptedForConfidentiality")
    print("Bob's Message Decrypted for Confidentiality: ", bobMessageDecryptedForConfidentiality)

def rsaForIntegrityAndAuthentication(file):
    alicePublicKey, alicePrivateKey = generatePublicAndPrivateKey()
    print("Alice's Public Key: ")
    print(alicePublicKey[0])
    print(alicePublicKey[1])
    print("Alice's Private Key: ")
    print(alicePrivateKey)
    aliceMessage = file_to_bits(file)
    print("Alice's Message: ", aliceMessage)
    aliceMessageEncryptedForIntegrityAndAuthentication = encipherMessageForIntegrityAndAuthentication(aliceMessage, alicePrivateKey, alicePublicKey[1])
    create_file(file, aliceMessageEncryptedForIntegrityAndAuthentication, "aliceMessageEncryptedForIntegrityAndAuthentication")
    print("Alice's Message Encrypted for Integrity and Authentication: ", aliceMessageEncryptedForIntegrityAndAuthentication)
    aliceMessageDecryptedForIntegrityAndAuthentication = decipherMessageForIntegrityAndAuthentication(aliceMessageEncryptedForIntegrityAndAuthentication, alicePublicKey)
    create_file(file, aliceMessageDecryptedForIntegrityAndAuthentication, "aliceMessageDecryptedForIntegrityAndAuthentication")
    print("Alice's Message Decrypted for Integrity and Authentication: ", aliceMessageDecryptedForIntegrityAndAuthentication)

def rsaForConfidentialityIntegrityAndAuthentication(file):
    alicePublicKey, alicePrivateKey = generatePublicAndPrivateKey()
    print("Alice's Public Key: ")
    print(alicePublicKey[0])
    print(alicePublicKey[1])
    print("Alice's Private Key: ")
    print(alicePrivateKey)
    bobPublicKey, bobPrivateKey = generatePublicAndPrivateKey()
    print("Bob's Public Key: ")
    print(bobPublicKey[0])
    print(bobPublicKey[1])
    print("Bob's Private Key: ")
    print(bobPrivateKey)
    aliceMessage = file_to_bits(file)
    print("Alice's Message: ", aliceMessage)
    aliceMessageEncryptedForIntegrityAndAuthentication = encipherMessageForIntegrityAndAuthentication(aliceMessage, alicePrivateKey, alicePublicKey[1])
    create_file(file, aliceMessageEncryptedForIntegrityAndAuthentication, "aliceMessageEncryptedForIntegrityAndAuthentication")
    print("Alice's Message Encrypted for Integrity and Authentication: ", aliceMessageEncryptedForIntegrityAndAuthentication)
    aliceMessageEncryptedForConfidentialityIntegrityAndAuthentication = encipherMessageForConfidentiality(aliceMessageEncryptedForIntegrityAndAuthentication, bobPublicKey)
    create_file(file, aliceMessageEncryptedForConfidentialityIntegrityAndAuthentication, "aliceMessageEncryptedForConfidentialityIntegrityAndAuthentication")
    print("Alice's Message Encrypted for Confidentiality, Integrity, and Authentication: ", aliceMessageEncryptedForConfidentialityIntegrityAndAuthentication)
    aliceMessageDecryptedForConfidentiality = decipherMessageForConfidentiality(aliceMessageEncryptedForConfidentialityIntegrityAndAuthentication, bobPrivateKey, bobPublicKey[1])
    create_file(file, aliceMessageDecryptedForConfidentiality, "aliceMessageDecryptedForConfidentiality")
    print("Alice's Message Decrypted for Confidentiality: ", aliceMessageDecryptedForConfidentiality)
    aliceMessageDecryptedForConfidentialityIntegrityAndAuthentication = decipherMessageForIntegrityAndAuthentication(aliceMessageDecryptedForConfidentiality, alicePublicKey)
    create_file(file, aliceMessageDecryptedForConfidentialityIntegrityAndAuthentication, "aliceMessageDecryptedForConfidentialityIntegrityAndAuthentication")
    print("Alice's Message Decrypted for Confidentiality, Integrity, and Authentication: ", aliceMessageDecryptedForConfidentialityIntegrityAndAuthentication)

def rsa(file):
    rsaForConfidentiality(file)
    print()
    rsaForIntegrityAndAuthentication(file)
    print()
    # rsaForConfidentialityIntegrityAndAuthentication(file)

rsa(file)
