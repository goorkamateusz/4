from des import bin2hex, decrypt, encrypt
from generate_key import generate_key
from utils import bin2text, chunk, hex2text, text2bin, xor


def encrypt_cbc_iter(text: str, key: str, iv: str):
    (rkb, rk) = generate_key(key)
    text = text2bin(text)
    blocks = chunk(text, 64)

    for block in blocks:
        block = xor(block, iv)

        bin = encrypt(block, rkb, rk)
        iv = bin

        hex = bin2hex(bin)
        print(f"{hex = }")

        yield bin

    length = len(blocks[-1]) % 64
    length = 64 if length == 0 else length
    print(f"{length = }")
    yield text2bin(str(length))


def encrypt_cbc(text: str, key: str, iv: str):
    out_blocks = [i for i in encrypt_cbc_iter(text, key, iv)]
    return "".join(out_blocks)


def decrypt_cbc(cipher: str, key: str, iv: str):
    out_blocks = []
    (rkb, rk) = generate_key(key)
    cipher_blocks = chunk(cipher, 64)

    last_block = cipher_blocks.pop()
    length_last = int(bin2text(last_block))
    print(f"{length_last = }")

    for i, cipher in enumerate(cipher_blocks):
        x = decrypt(cipher, rkb, rk)
        x = xor(x, iv)

        iv = cipher

        if i == len(cipher_blocks) - 1:
            x = x[:length_last].ljust(64, '0')

        hex = bin2hex(x)
        text = hex2text(hex)
        print(f"{hex = } | {text = }")
        out_blocks.append(text)

    return "".join(out_blocks)
