key = "123"

fin = open("hamlet.txt")
ham = fin.read()

new_ham = bytearray()
for i in range(len(ham)):
    new_ham.append(ord(ham[i]) ^ ord(key[i % len(key)]))
    
fout = open("hamlet-xor.txt", 'wb')
fout.write(new_ham)
fout.close()