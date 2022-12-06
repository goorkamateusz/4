import des


def text2hex(txt: str):
    return txt.encode(encoding='UTF-8').hex().upper()


def hex2text(hex):
    return bytes.fromhex(hex).decode('UTF-8')


def bin2text(bin):
    return hex2text(des.bin2hex(bin))


def text2bin(text):
    return des.hex2bin(text2hex(text))


def xor(x, iv):
    x = [(ord(a) ^ ord(b)) for a, b in zip(x, iv)]
    return "".join(str(i) for i in x)


def chunk(data, n=16):
    blocks = [data[i:i+n] for i in range(0, len(data), n)]
    return blocks
