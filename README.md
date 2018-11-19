# xor-decrypt
## Description
XOR-decrypt is a simple tool which allows you to find a key for a xor cipher, using which some text was encrypted. It automatically finds the length of the key, and the key itself. 
During the work it shows you all probable key lengths, probable keys and decrypted text samples.

## Options
  * **-i --input-file**       File with encrypted text.
  * **-o --output-file**      File for decrypted text.
  * **-m --maxlen**           The maximum length of the key.
  * **-l --keylen**           The length of the key.
  * **-k --key**              The key for the xor cipher.
  * **-f --most-frequent**    The most frequent byte in the given file type.
  * **-d --decrypt**          Decrypt the file and save to output.
  * **-h --help**             Show this message.

## Usage
You can combine the options as you wish, but here are the most handy ones:
  * To find the key automatically and decrypt the text:
  
    `xor-decrypt.py -i "i.txt" -o "o.txt" -m 32 -f 32 -d`
    
  * To find most probable key lengths and keys:
  
    `xor-decrypt.py -i "i.txt" -m 32 -f 32`

  * To find the key with a given length:
  
    `xor-decrypt.py -i "i.txt" -l 10 -f 32`

  * To decrypt the text with the given key:
  
    `xor-decrypt.py -i "i.txt" -o "o.txt" -k 123 -d`
