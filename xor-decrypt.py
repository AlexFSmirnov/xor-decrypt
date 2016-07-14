help_message = """
XOR-decrypt is a simple tool which allows you to find a key for a xor cipher,
using which some text was encrypted. Is automatically finds the length of the 
key, and the key itself.

Options:
  -i --input-file       File with encrypted text.
  -o --output-file      File for decrypted text.
  -m --maxlen           The maximum length of the key.
  -l --keylen           The length of the key.
  -k --key              The key for the xor cipher.
  -f --most-frequent    The most frequent byte in the given file type.
  -d --decrypt          Decrypt the file and save to output.
  -h --help             Show this message

Usage:
 You can combine the options as you wish, but here are the most handy ones:
  To find the key automatically and decrypt the text:
    xor-decrypt.py -i "i.txt" -o "o.txt" -m 32 -f 32 -d
    
  To find most probable key lengths and keys:
    xor-decrypt.py -i "i.txt" -m 32 -f 32

  To find the key with a given length:
    xor-decrypt.py -i "i.txt" -l 10 -f 32

  To decode the text with the given key:
    xor-decrypt.py -i "i.txt" -o "o.txt" -k 123 -d

"""
from sys import argv
from collections import Counter


def findKeyLen(bytearr, maxlen):
    # Shifting the text <maxlen> times.
    shifted_arrs = []
    for shift in range(1, maxlen + 1):
        shifted_arrs.append(shiftBytearr(bytearr, shift))
    # Counting the matching bytes in the shifted and the source bytearray.
    # The more the matches percent is, the more the chance that the shift is 
    # divisible by keylen is.
    matches = [[0, 0]]
    for shift in range(1, maxlen + 1):
        matches.append([countMatches(bytearr, shifted_arrs[shift - 1]), shift])
    matches.sort(reverse=True)
    # Finding the most probable keylens.
    prob_lens_rep = []
    prev_prc = 0
    for match in matches[1:]:
        curr_prc = match[0]
        if curr_prc < prev_prc * 0.8: 
            break
        prob_lens_rep.append(match)
        prev_prc = curr_prc
    # And now deleting the repetitions. Let me explain:
    # Imagine you've got a key "123". Then 3 is the probable keylen.
    # But 6 is also a probable keylen ("123123"), and 9 is, and so on.
    # So here we delete from the array all "6" and "9", 
    # and leave only "3".
    prob_lens_rep.sort(key=lambda prob_lens_rep: prob_lens_rep[1])
    prob_lens = [prob_lens_rep[0]]
    for len1 in prob_lens_rep[1:]:
        tg = True
        for len2 in prob_lens:
            if len1[1] % len2[1] == 0: tg = False
        if tg: 
            prob_lens.append(len1)
    return sorted(prob_lens, reverse=True)

# Shifts the given bytearray. E.g. "12345" -> "23451" (shift = 1)
def shiftBytearr(bytearr, shift):
    return bytearr[shift:] + bytearr[:shift]

# Counts the matching symbols for two arrays. Returns %.
def countMatches(source, shifted):
    cnt = 0
    for i in range(len(source)):
        if source[i] == shifted[i]: cnt += 1
    return int(cnt / len(source) * 1000) / 10

# Tries to find a key with the given len for the text.
def findXorKey(text, key_len, most_common_byte=32):
    key = bytearray([0] * key_len)
    for st_idx in range(key_len):
        keyspace_text = []
        keyspace_dict = {}
        for idx in range(st_idx, len(text), key_len):
            keyspace_text.append(text[idx])
        most_common_found = Counter(keyspace_text).most_common(1)[0][0]
        key[st_idx] = most_common_byte ^ most_common_found
    return key

def decrypt(bytearr, key):
    output = bytearray()
    for i in range(len(bytearr)):
        output.append(bytearr[i] ^ key[i % len(key)])
    return output
        

input_file    = None
output_file   = None
maxlen        = None
keylen        = None
key           = None
most_frequent = 32
do_decrypt    = False

i = 0
while i < len(argv):
    arg = argv[i]
    if arg in ("-i", "--input-file"):
        i += 1
        input_file = argv[i]
    if arg in ("-o", "--output-file"):
        i += 1
        output_file = argv[i]
    if arg in ("-m", "--maxlen"):
        i += 1
        maxlen = int(argv[i])
    if arg in ("-l", "--keylen"):
        i += 1
        keylen = int(argv[i])
    if arg in ("-k", "--key"):
        i += 1
        key = argv[i].encode("utf-8")
    if arg in ("-f", "--most-frequent"):
        i += 1
        most_frequent = int(argv[i])
    if arg in ("-d", "--decrypt"):
        do_decrypt = True
    if arg in ("-h", "--help"):
        print(help_message)
        exit(0)
    i += 1
    
source_text = open(input_file, 'rb').read()

if maxlen:   # Find keylens and keys.
    prob_lens = findKeyLen(source_text, maxlen)
    print("Probable key lengths: ")
    for prc, length in prob_lens:
        print("   ", length, " - ", prc, "%", sep='')
    keylen = prob_lens[0][1]
if keylen:   # Find a key with a given keylen.
    key = findXorKey(source_text, keylen, most_frequent)
    print("Found a key:", key.decode("utf-8"))
    print("Decrypted text sample:", decrypt(source_text[:50], 
                                            key).decode("utf-8"))
    
if do_decrypt:  # Decrypt a text with a given/found key.
    with open(output_file, 'wb') as fout: fout.write(decrypt(source_text, key))
    fout.close()