import base64

#Text files
def file_to_bits(file_path):
    l = []
    with open(file_path, 'r') as f:
        content = f.read()
    byte_form = content.encode(encoding = 'UTF-8')
    print(byte_form)
    for bytes in byte_form:
        l.append(bytes)
    
    return l

def file2_to_bits(file_path):
    l = []
    image = open(file_path, 'rb')
    image_read = image.read()
    image_64_encode = base64.encodebytes(image_read) 
    print(image_64_encode)
    for bytes in image_64_encode:
        l.append(bytes)

    return l

def bits2_to_file(file_path):
    l = []
    image = open(file_path, 'rb')
    image_read = image.read()
    image_64_decode = base64.decodebytes(base64.encodebytes(image_read)) 
    print(image_64_decode)
    for bytes in image_64_decode:
        l.append(bytes)

    return l

# image_64_decode = base64.decodebytes(image_64_encode) 
# image_result = open('deer_decode.jpg', 'wb')
# image_result.write(image_64_decode)
    
def key_function(key, phrase):
    if len(key) == len(phrase):
        return key
    
    else:
        phrase_diff = len(phrase) - len(key)
        for i in range(phrase_diff):
            key.append(key[i%len(key)])
    
    return key

def cipher_function_display(key,phrase):
    cipher = []
    for i in range(len(phrase)):
        #temp = ((ord(phrase[i]) + ord(key[i])) % 26) + 65
        temp = ((phrase[i] + key[i]) % 26) + 65
        cipher.append(chr(temp))
    
    return("".join(cipher))

def cipher_function(key,phrase):
    cipher = []
    for i in range(len(phrase)):
        #temp = ((ord(phrase[i]) + ord(key[i])) % 26) + 65
        temp = ((phrase[i] + key[i]) % 26) + 65
        cipher.append(temp)
    
    return(cipher)

def english_text_function(key, phrase):
    english = []
    for i in range(len(phrase)):
        temp = (((phrase[i] - key[i])+26) % 26) + 65
        english.append(chr(temp))
    
    return("".join(english))


#english_text = "MOMUD EKAPV TQEFM OEVHP AJMII CDCTI FGYAG JSPXY ALUYM NSMYH VUXJE LEPXJ FXGCM JHKDZ RYICU HYPUS PGIGM OIYHF WHTCQ KMLRD ITLXZ LJFVQ GHOLW CUHLO MDSOE KTALU VYLNZ RFGBX PHVGA LWQIS FGRPH JOOFW GUBYI LAPLA LCAFA AMKLG CETDW VOELJ IKGJB XPHVG"
#vigenere_key = "EYTR"
english_text = file_to_bits("text_content.txt")
vigenere_key = file_to_bits("vigenere_key.txt")


print(english_text)
print(vigenere_key)
repeated_key = key_function(vigenere_key,english_text)
print(repeated_key)
encoded_text = cipher_function_display(repeated_key,english_text)
print(encoded_text)
encoded_list = cipher_function(repeated_key,english_text)
print(english_text_function(repeated_key,encoded_list))
video_bits = file2_to_bits("test2.mp4")
print(video_bits)
print(cipher_function_display(key_function(vigenere_key,video_bits),video_bits))
print(english_text_function(key_function(vigenere_key,video_bits),cipher_function(key_function(vigenere_key,video_bits),video_bits)))
print(bits2_to_file("test2.mp4"))
#Bytes

# public static Byte[] encryptByteVigenere(Byte[] plaintext, string key) 
# {

#     Byte[] result= new Byte[plaintext.Length];

#     key = key.Trim().ToUpper();

#     int keyIndex = 0;
#     int keylength = key.Length;

#     for (int i = 0; i < plaintext.Length; i++)
#     {
#         keyIndex = keyIndex % keylength;
#         int shift = (int)key[keyIndex] - 65;
#         result[i] = (byte)(((int)plaintext[i] + shift) % 256);
#         keyIndex++;
#     }

#     return result;
# }
# public static Byte[] decryptByteVigenere(Byte[] ciphertext, string key)
# {
#     Byte[] result = new Byte[ciphertext.Length];

#     key = key.Trim().ToUpper();

#     int keyIndex = 0;
#     int keylength = key.Length;

#     for (int i = 0; i < ciphertext.Length; i++)
#     {             
#         keyIndex = keyIndex % keylength;
#         int shift = (int)key[keyIndex] - 65;
#         result[i]= (byte)(((int)ciphertext[i] + 256 - shift) % 256);
#         keyIndex++;               
#     }

#     return result;
# }