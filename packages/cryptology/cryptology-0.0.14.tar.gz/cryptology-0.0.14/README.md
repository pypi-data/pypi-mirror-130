# Cryptology
This is a package which decrypt/encrypts text using a few different methods.

## Installation
Run the following to install:

```python
pip install cryptology
```

## Usage
```python
from cryptology import atbash_decrypt

# Generate decryption
string=atbash_decrypt(cipher_text="GSRHRHMLGEVIBHVXIVGZGZOO")

print(string)
```

Other functions include:

```python
import cryptology as cp

# Generate decryption

# Atbash
str_atbash_decrypted=cp.atbash_decrypt(cipher_text="GSRHRHMLGEVIBHVXIVGZGZOO")

str_atbash_encrypted=cp.atbash_encrypt(plain_text="THISISNOTVERYSECRETATALL")

# Ceaser
str_ceaser_decrypted=cp.ceaser_decrypt(cipher_text="MTBVZNHPQDINIDTZGWJFPYMNX",
                                      shift=5)

str_ceaser_encrypted=cp.ceaser_encrypt(plain_text="HOWQUICKLYDIDYOUBREAKTHIS",
                                      shift=5)

# Vigenere
str_ceaser_decrypted=cp.vigenere_decrypt(cipher_text="YDXGJHCJVODXUGGZ",
                                         keyword="NIGHTTIME",
                                         permutation="thislepgywnomarkdbfcjquvxz")

str_ceaser_encrypted=cp.vigenere_encrypt(plain_text="VISABILITYISPOOR",
                                         keyword="NIGHTTIME",
                                         permutation="thislepgywnomarkdbfcjquvxz")

# Playfair
str_playfair_decrypted=cp.playfair_decrypt(cipher_text="GIVHYCHGSYPCFHWHGDHPUTSMYTLD",
                                        keyword="GLAMORGAN")

str_playfair_decrypted=cp.playfair_encrypt(plain_text="MEETMEATTREFFORESTSTATION",
                                        keyword="GLAMORGAN")

print(string)
```

