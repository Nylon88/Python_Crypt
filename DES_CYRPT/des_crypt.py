import math
import random


"""
    サブ鍵を生成する
"""
pc1_table = [57,49,41,33,25,17,9,
            1,58,50,42,34,26,18,
            10,2,59,51,43,35,27,
            19,11,3,60,52,44,36,
            63,55,47,39,31,23,15,
            7,62,54,46,38,30,22,
            14,6,61,53,45,37,29,
            21,13,5,28,20,12,4]

pc2_table = [14,17,11,24,1,5,
            3,28,15,6,21,10,
            23,19,12,4,26,8,
            16,7,27,20,13,2,
            41,52,31,37,47,55,
            30,40,51,45,33,48,
            44,49,39,56,34,53,
            46,42,50,36,29,32]

bit_list = [0,1]


#
# odd_parity()
# 入力：リストl
# 出力：0 or 1
# リストlにおけるハミング重みが奇数個ならば0, 偶数個ならば1
#
def odd_parity(l):
    odd_count = 0
    for l_bit in l:
        if l_bit == 1:
            odd_count += 1

    if (odd_count % 2 == 0):
        return 1
    else:
        return 0


#
# key_generate()
# 入力：なし
# 出力：秘密鍵64bit
# 秘密鍵を生成する.
#
def key_generate():
    key = []
    for i in range(8):
        l = random.choices(bit_list, k=7)
        key += l
        key.append(odd_parity(l))

    return key


#
# PC1
# 入力：配列secret_key...64bit
# 出力： C0, D0...それぞれ28bit
# C0は左28bit, D0は右28bit
#
def pc1(secret_key:list) -> list:
    c0 = []
    d0 = []
    for i in range(56):
        if i <= 27:
            c0.append(secret_key[pc1_table[i]-1])
        else:
            d0.append(secret_key[pc1_table[i]-1])
    return c0, d0


#
# PC2
# 入力：配列c_d_list(C0とD0を連結させたもの)...56bit
# 出力： サブ鍵k 48bit
#
def pc2(c_d_list:list) -> list:
    k = []
    for i in range(48):
        k.append(c_d_list[pc2_table[i]-1])

    return k


#
# shift
# 入力：リストl, 移動ビット数n
# 出力：巡回シフト結果 (n=1のとき左に1bit巡回シフト)
#
def shift(l, n):
    return l[n:] + l[:n]


#
# enc_sub_key_generate()
# 入力：秘密鍵key
# 出力：sub_key_list
#
def enc_sub_key_generate(key:list) -> list:
    c = []
    d = []
    sub_key_list = []

    c, d = pc1(key)

    for i in range(1, 1+16):
        if (i == 1) or (i == 2) or (i == 9) or (i == 16):
            c = shift(c, 1)
            d = shift(d, 1)
        else:
            c = shift(c, 2)
            d = shift(d, 2)
        sub_key_list.append(pc2(c + d))

    return sub_key_list


#
# dec_sub_key_generate(key)
# 入力：秘密鍵
# 出力：sub_key_list (encのときと逆順)
#
def dec_sub_key_generate(key:list) -> list:
    c = []
    d = []
    sub_key_list = []

    c, d = pc1(key)

    for i in range(1, 1+16):
        if i == 1:
            c = c
            d = d
        elif (i == 2) or (i == 9) or (i == 16):
            c = shift(c, -1)
            d = shift(d, -1)
        else:
            c = shift(c, -2)
            d = shift(d, -2)
        sub_key_list.append(pc2(c + d))

    return sub_key_list


if __name__ == '__main__':
    key = key_generate()
    sub_key_list = enc_sub_key_generate(key)
    
    for i, v in enumerate(sub_key_list):
        print(f'{i+1}個目のsub key:{v}')
