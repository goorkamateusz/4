import os
import pyperclip
import time
from des import hex2bin
from des import bin2hex, hex2bin
from cbc import decrypt_cbc, encrypt_cbc
from ecb import decrypt_ecb, encrypt_ecb

if os.name == 'nt':
    from pyreadline3 import Readline
else:
    import readline


def end_time(start_time):
    t = time.time() - start_time
    print(f"Time: {t * 1_000} ms")


def clipboard(txt):
    pyperclip.copy(txt)
    data.cipher_hex = txt
    print("Copied to clipboard")


def _encrypt_ecb():
    start = time.time()
    text = data.plain_text
    cipher = encrypt_ecb(text, data.key)
    cipher = bin2hex(cipher)
    print(f"Cipher ECB: {cipher}")
    clipboard(cipher)
    end_time(start)


def _decrypt_ecb():
    start = time.time()
    cipher = data.cipher_hex
    cipher = hex2bin(cipher)
    decrypted = decrypt_ecb(cipher, data.key)
    print(f"Decrypted ECB: {decrypted}")
    end_time(start)


def _encrypt_cbc():
    start = time.time()
    text = data.plain_text
    cipher = encrypt_cbc(text, data.key, data.iv)
    cipher = bin2hex(cipher)
    print(f"Cipher CBC: {cipher}")
    clipboard(cipher)
    end_time(start)


def _decrypt_cbc():
    start = time.time()
    cipher = data.cipher_hex
    cipher = hex2bin(cipher)
    decrpyted = decrypt_cbc(cipher, data.key, data.iv)
    print(f"Decrypted CBC: {decrpyted}")
    end_time(start)


def set_key():
    print("     ################")
    data.key = input("key: ").upper().ljust(16, "0")
    print(f"key: {data.key}")


def set_key_ascii():
    print("     ########")
    key = input("key: ").upper()
    data.key = key.encode(encoding='ASCII').hex().ljust(16, "0")
    print(f"key (hex): {data.key}")


def set_iv():
    print("    ################")
    data.iv = input("iv: ").upper().ljust(16, "0")
    print(f"iv: {data.iv}")


def help():
    print("\n".join(data.commands.keys()))


def close():
    exit()


def set_plain_text():
    data.plain_text = input("Plain text: ")


def set_cipher():
    data.cipher_hex = input("Cipher (HEX): ")


def read_from_file():
    file_name = input("File name: ")
    file = open(file_name, "r", encoding='utf-8')
    return "".join(file.readlines())


def plain_text_from_file():
    data.plain_text = read_from_file()


def cipher_from_file():
    data.cipher_hex = read_from_file()


def save_to_file(txt):
    file_name = input("File name: ")
    file = open(file_name, "w", encoding='utf-8')
    file.write(txt)


def plain_text_to_file():
    save_to_file(data.plain_text)


def cipher_to_file():
    save_to_file(data.cipher_hex)


def print_text():
    print(data.plain_text)


def print_cipher():
    print(data.cipher_hex)


class data:
    key = "FFFFFFFFFFFFFFFF"
    iv = hex2bin("FFFFFFFFFFFFFFFF")
    plain_text = None
    cipher_hex = None
    commands = {
        "help": help,
        "exit": close,

        "encrypt_ecb": _encrypt_ecb,
        "decrypt_ecb": _decrypt_ecb,
        "encrypt_cbc": _encrypt_cbc,
        "decrypt_cbc": _decrypt_cbc,

        "set_key": set_key,
        "set_key_ascii": set_key_ascii,
        "set_iv": set_iv,

        "set_plaintext": set_plain_text,
        "set_cipher": set_cipher,

        "print_plaintext": print_text,
        "print_cipher": print_cipher,

        "load_plaintext_from_file": plain_text_from_file,
        "load_cipher_from_file": cipher_from_file,
        "save_plaintext_to_file": plain_text_to_file,
        "save_cipher_to_file": cipher_to_file,
    }


if os.name == 'nt':
    readline = Readline()


def complete(text, state):
    for cmd in data.commands.keys():
        if cmd.startswith(text):
            if not state:
                return cmd
            else:
                state -= 1


readline.parse_and_bind("tab: complete")
readline.set_completer(complete)
readline.readline_setup()

while True:
    try:
        readline.disable_readline = False
        command: str = readline.readline("> ")
        readline.disable_readline = True
        command = command.strip()
        print(f"--- {command} ---")
        data.commands[command]()
    except KeyError:
        help()
    except KeyboardInterrupt:
        close()
    except Exception as e:
        print(e)
