# -*- coding: UTF-8 -*-
import sys

FACTOR = 'fsdf^%jks234af&(kndjfd&^jnkjdfg%rgdfgsd&234n123'


def encrypt(s):
    encrypt_str = ""
    for i, j in zip(s, FACTOR):
        temp = str(ord(i) + ord(j)) + '_'
        encrypt_str = encrypt_str + temp
    return encrypt_str


def decrypt(p):
    dec_str = ""
    for i, j in zip(p.split("_")[:-1], FACTOR):
        temp = chr(int(i) - ord(j))
        dec_str = dec_str + temp
    return dec_str


if __name__ == '__main__':
    if len(sys.argv) > 2:
        s_type = sys.argv[1]
        s_str = sys.argv[2]
        if s_type == 'encrypt':
            print(encrypt(s_str))
        elif s_type == 'decrypt':
            print(decrypt(s_str))
        else:
            print(f"不支持的类型：{s_type}")
    else:
        print("""
        请携带类型参数：[*.py type data]
            type : encrypt | decrypt
            data : 需要加密的字符串 
        """)


