from collections import Counter


#-------------------------------------------------------------------------------    
# FINDING XOR KEY LENGTH BELOW                                                 
#-------------------------------------------------------------------------------

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
    # Finding the most probable keylens.
    prob_lens_rep = []
    prev_prc = 0
    for match in matches:
        curr_prc = match[0]
        if curr_prc < prev_prc * 0.8: 
            break
        prob_lens_rep.append(i)
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
    return prob_lens

# Shifts the given bytearray. E.g. "12345" -> "23451" (shift = 1)
def shiftBytearr(bytearr, shift):
    return bytearr[shift:] + bytearr[:shift]

# Counts the matching symbols for two arrays. Returns %.
def countMatches(source, shifted):
    cnt = 0
    for i in range(len(source)):
        if source[i] == shifted[i]: cnt += 1
    return int(cnt / len(source) * 1000) / 10

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
        


fin = open("hamlet-xor.txt", 'rb')

source_text = fin.read()
prob_lens = sorted(findKeyLen(source_text, 32), reverse=True)


