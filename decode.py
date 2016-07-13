key = "pfvodngbf"

fin = open("hamlet-xor.txt", 'rb')
ham = fin.read()

new_ham = ""
for i in range(len(ham)):
    new_ham += chr(ham[i] ^ ord(key[i % len(key)]))
    
fout = open("hamlet2.txt", 'w')
fout.write(new_ham)