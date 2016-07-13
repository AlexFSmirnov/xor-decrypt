from collections import Counter


def shiftText(n):
    return n[1:] + bytes([n[0]])

def countMatches(source, shifted):
    cnt = 0
    for i in range(len(source)):
        if source[i] == shifted[i]: cnt += 1
    return int(cnt / len(source) * 1000) / 10

def findXorKey(text, key_len):
    key = bytearray([0] * key_len)
    for st_idx in range(key_len):
        keyspace_text = []
        keyspace_dict = {}
        for idx in range(st_idx, len(text), key_len):
            keyspace_text.append(text[idx])
        most_common = Counter(keyspace_text).most_common(1)[0][0]
        
        key[st_idx] = ord(' ') ^ most_common
    return key
        


fin = open("hamlet-xor.txt", 'rb')

source_text = fin.read()
shifted_texts = [source_text]

for shift in range(32):
    shifted_texts.append(shiftText(shifted_texts[-1]))


for i, shifted in enumerate(shifted_texts):
    print(i, ": ", countMatches(source_text, shifted), "%", sep='')