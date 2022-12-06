from typing import List
from des import bin2hex, decrypt, encrypt, hex2bin
from generate_key import generate_key
from utils import bin2text, chunk, hex2text, text2hex


def encrypt_ecb_iter(text: str, key: str):
    (rkb, rk) = generate_key(key)
    pt = text2hex(text)
    blocks = chunk(pt)

    for cipher in blocks:
        t = hex2bin(cipher)
        bin = encrypt(t, rkb, rk)
        hex = bin2hex(bin)
        print(f"{hex = }")
        yield bin


def encrypt_ecb_arr(text: str, key):
    return [i for i in encrypt_ecb_iter(text, key)]


def encrypt_ecb(text: str, key):
    return "".join(encrypt_ecb_arr(text, key))


def decrypt_ecb(cipher: str | List[str], key: str):
    (rkb, rk) = generate_key(key)

    if isinstance(cipher, str):
        cipher = chunk(cipher, 64)

    decrypteds = []
    for cipher_text in cipher:
        bin = decrypt(cipher_text, rkb, rk)
        hex = bin2hex(bin)
        text = hex2text(hex)
        print(f"{hex = } | {text = }")
        decrypteds.append(text)

    return "".join(decrypteds)
