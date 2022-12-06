# Code from: https://www.geeksforgeeks.org/data-encryption-standard-des-set-1/

import des


def generate_key(key: str):
    # Key generation
    # --hex to binary
    key = des.hex2bin(key)

    # getting 56 bit key from 64 bit using the parity bits
    key = des.permute(key, des.keyp, 56)

    # Splitting
    left = key[0:28]  # rkb for RoundKeys in binary
    right = key[28:56]  # rk for RoundKeys in hexadecimal

    rkb = []
    rk = []
    for i in range(0, 16):
        # Shifting the bits by nth shifts by checking from shift table
        left = des.shift_left(left, des.shift_table[i])
        right = des.shift_left(right, des.shift_table[i])

        # Combination of left and right string
        combine_str = left + right

        # Compression of key from 56 to 48 bits
        round_key = des.permute(combine_str, des.key_comp, 48)

        rkb.append(round_key)
        rk.append(des.bin2hex(round_key))

    return (rkb, rk)
