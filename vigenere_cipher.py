# Team 2
# Vigenere Cypher is one of the simpler cyphers that encrypt only alphabetical text through repeated Caeser cypher.
# Traditional vigenere cypher is repeated on alphabetical key with strictly alphabetic characters.
# This code performs vigenere in a more advanced way
# Two ways shown in this peice: 1) all ascii encoding (not just alphabets)
#                               2) encryption done in bytes rather than strings for efficiency


#All readable ascii encryption using vigenere cypher

#Dictionary list of all readable ascii
ascii = [characterCode for characterCode in (chr(i) for i in range(32,127))]

# Helper functions

# Reading from file upload
def file_read(file_path):
  with open(file_path, 'r') as f:
    content = f.read()

  return content

# To binary
def keychange(key):
  key = key.decode('utf-8')

  return key
# Key generation
# Vigenere key is taken as input and repeated till the length of the English text
def keygen(key, ascii_text):
  v_key = ""
  for i in range(len(ascii_text)):
    v_key+=key[i%len(key)]

  return v_key

# Encryption
# Takes repeated key and shifts the ascii text given to encrypt
def encrypt(key, ascii_text):
  # ascii_text = ascii_text.decode('utf-8')
  # key = key.decode('utf-8')
  cipher_text = ""
  for i in range(len(ascii_text)):
    cipher_text+= ascii[(ascii.index(ascii_text[i])+ascii.index(key[i%len(key)]))%len(ascii)]
  return cipher_text

# Decryption
# Takes repeated key and bak shifts the cipher text given to edecrypt
def decrypt(key, cipher_text):
  #cipher_text = cipher_text.decode('utf-8')
  # key = key.decode('utf-8')
  original_text = ""
  for i in range(len(cipher_text)):
    original_text+= ascii[(ascii.index(cipher_text[i])-ascii.index(key[i%len(key)]))%len(ascii)]

  return original_text

# key = file_read("testFiles/vigenere_key.txt")
# print(keychange(key))
# Testing for inputs and encryption/decryption process

key = file_read("testFiles/vigenere_key.txt")
ascii_text = file_read("testFiles/test1.txt")

# Generating the repeated key
repeated_key = keygen(key, ascii_text)
print("The repeated key is: " + repeated_key)

# Encryption of text
encrypted_text = encrypt(key, ascii_text)
print("The encypted message is: " + encrypted_text)

# Decryption of cipher text
decrypted_text = decrypt(key, encrypted_text)
print("The decypted message is: " + decrypted_text)


#All readable ascii encryption using vigenere cypher in bytes to improve efficiency

# Helper functions

# Byte conversion
# Converting inputted string to bytearray
def to_byte(str) :
  b_str = bytes(str,"ascii")

  return b_str

# Key genereation
# Vigenere key is taken as input and repeated till the length of the English text but in bytes
def b_keygen(key, ascii_text):
  b_v_key = key*(len(ascii_text)//len(key)) + key[:len(ascii_text)%len(key)]

  return b_v_key

# Encryption
# Takes repeated key and shifts the ascii text given to encrypt
def b_encrypt(key, ascii_text):
  cipher_text = bytes(a^r for a,r in zip(to_byte(ascii_text), b_keygen(to_byte(key), to_byte(ascii_text))))

  return cipher_text.decode('ascii')

# Decryption
# Takes repeated key and bak shifts the cipher text given to edecrypt
def b_decrypt(key, cipher_text):
  original_text = bytes(a^r for a,r in zip(to_byte(cipher_text), b_keygen(to_byte(key), to_byte(cipher_text))))

  return original_text.decode('ascii')

# Testing for inputs and encryption/decryption process with bytes method

# key = file_read("testFiles/vigenere_key.txt")
# ascii_text = file_read("testFiles/test1.txt")

# # Generating the repeated key
# repeated_key = b_keygen(key, ascii_text)
# print("The repeated key is: " + repeated_key)

# # Encryption of text
# encrypted_text = b_encrypt(key, ascii_text)
# print("The encypted message is: " + encrypted_text)

# # Decryption of cipher text
# decrypted_text = b_decrypt(key, encrypted_text)
# print("The decypted message is: " + decrypted_text)
