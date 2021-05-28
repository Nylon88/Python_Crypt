import random
from typing import Tuple


# ラウンド関数の最初の転置で使う
E = [32,1,2,3,4,5,
    4,5,6,7,8,9,
    8,9,10,11,12,13,
    12,13,14,15,16,17,
    16,17,18,19,20,21,
    20,21,22,23,24,25,
    24,25,26,27,28,29,
    28,29,30,31,32,1]

# ラウンド関数の最後の転置で使う
P = [16,7,20,21,
    29,12,28,17,
    1,15,23,26,
    5,18,31,10,
    2,8,24,14,
    32,27,3,9,
    19,13,30,6,
    22,11,4,25]

# s-box変換用
S1 = [[14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7],
      [0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8],
      [4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0],
      [15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13]]

S2 = [[15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10],
      [3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5],
      [0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15],
      [13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9]]

S3 = [[10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8],
      [13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1],
      [13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7],
      [1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12]]

S4 = [[7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15],
      [13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9],
      [10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4],
      [3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14]]

S5 = [[2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9],
      [14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6],
      [4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14],
      [11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3]]

S6 = [[12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11],
      [10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8],
      [9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6],
      [4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13]]

S7 = [[4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1],
      [13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6],
      [1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2],
      [6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12]]

S8 = [[13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7],
      [1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2],
      [7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8],
      [2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11]]

S_list = [S1, S2, S3, S4, S5, S6, S7, S8]

# IP、IP-1転置用
IP = [58,50,42,34,26,18,10,2,
     60,52,44,36,28,20,12,4,
     62,54,46,38,30,22,14,6,
     64,56,48,40,32,24,16,8,
     57,49,41,33,25,17,9,1,
     59,51,43,35,27,19,11,3,
     61,53,45,37,29,21,13,5,
     63,55,47,39,31,23,15,7]

IP_inverse = [40,8,48,16,56,24,64,32,
             39,7,47,15,55,23,63,31,
             38,6,46,14,54,22,62,30,
             37,5,45,13,53,21,61,29,
             36,4,44,12,52,20,60,28,
             35,3,43,11,51,19,59,27,
             34,2,42,10,50,18,58,26,
             33,1,41,9,49,17,57,25]

bit_list = [0,1]


"""
    鍵(56bit)Class
"""

class SecretKey:
    # リストlにおけるハミング重みが奇数個ならば0, 偶数個ならば1
    def odd_parity(self, l:list) -> int:
        odd_count = 0
        for l_bit in l:
            if l_bit == 1:
                odd_count += 1

        if (odd_count % 2 == 0):
            return 1
        else:
            return 0

    # 秘密鍵(56bit)を生成する.
    def generate(self) -> list:
        key = []
        for _ in range(8):
            l = random.choices(bit_list, k=7)
            key += l
            key.append(self.odd_parity(l))

        return key


"""
    サブ鍵(48bit)Class
"""

class SubKey:
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


    # 秘密鍵(56bit)をp1で縮小転置する
    def pc1(self, secret_key:list) -> Tuple[list, list]:
        c0 = []
        d0 = []
        for i in range(56):
            if i <= 27:
                c0.append(secret_key[SubKey.pc1_table[i]-1])
            else:
                d0.append(secret_key[SubKey.pc1_table[i]-1])
        return c0, d0

    # サブ鍵(56bit)をp2で縮小転置する
    def pc2(self, c_d_list:list) -> list:
        k = []
        for i in range(48):
            k.append(c_d_list[SubKey.pc2_table[i]-1])

        return k


# 暗号化用のサブ鍵
class EncSubKey(SubKey):
    def __init__(self) -> None:
        super().__init__()

    # サブ鍵(48bit)の生成
    def generate(self, key:list) -> list:
        c = []
        d = []
        sub_key_list = []

        # p1で秘密鍵(56bit)を転置(56bit)して、2つに分ける
        c, d = self.pc1(key)

        # 暗号化用のサブ鍵生成アルゴリズム
        for i in range(1, 1+16):

            # 1,2,9,16個目の鍵(56bit)は１シフトする
            if (i == 1) or (i == 2) or (i == 9) or (i == 16):
                c = shift(c, 1)
                d = shift(d, 1)
            # それ以外の鍵(56bit)は、2シフトする
            else:
                c = shift(c, 2)
                d = shift(d, 2)
            
            # 生成したサブ鍵(56bit)を、p2で縮小転置(48bit)して格納する
            sub_key_list.append(self.pc2(c + d))

        return sub_key_list


# 復号化用のサブ鍵
class DecSubKey(SubKey):
    def __init__(self) -> None:
        super().__init__()

    # サブ鍵(56bit)の生成
    def generate(self, key:list) -> list:
        c = []
        d = []
        sub_key_list = []

        # p1で秘密鍵(56bit)を転置(56bit)して、2つに分ける
        c, d = self.pc1(key)

        # 復号化用のサブ鍵生成アルゴリズム
        for i in range(1, 1+16):
            if i == 1:
                c = c
                d = d
            
            # 2,9,16個目の鍵(56bit)は-１シフトする
            elif (i == 2) or (i == 9) or (i == 16):
                c = shift(c, -1)
                d = shift(d, -1)
            # それ以外の鍵(56bit)は、-2シフトする
            else:
                c = shift(c, -2)
                d = shift(d, -2)
            sub_key_list.append(self.pc2(c + d))

        return sub_key_list


"""
    Utils関数と暗号化、復号化の関数
"""

# 出力：巡回シフト結果 (n=1のとき左に1bit巡回シフト)
def shift(l:list, n:int) -> list:
    return l[n:] + l[:n]


# xorを計算
def calc_xor(x:list, k:list) -> int:
    if (x == k):
        return 0
    else:
        return 1


# 10進数numを2進数に変換して配列に格納(4bitで固定)
def calc_binary(num:int) -> list:
    list = []
    while num > 0:
        list.append(num % 2)
        num = num // 2

    while len(list) != 4:
        list.append(0)

    list.reverse()
    return list


#  ラウンド関数
def f(x:list, k:list) -> list:

    x1 = []
    x2 = []
    x3 = []
    y = []

    # x(32bit)を48bitに拡大転置
    for i in range(48):
        x1.append(x[E[i]-1])

    # X(48bit)とサブ鍵k(48bit)で排他的論理和をとる
    for x1_item, k_item in zip(x1, k):
        x2.append(calc_xor(x1_item, k_item))

    # 
    for i in range(0, 48, 6):
        arg1 = (i//6)
        arg2 = x2[i+0] * 2 + x2[i+5] * 1
        arg3 = x2[i+1] * 8 + x2[i+2] * 4 + x2[i+3] * 2 + x2[i+4] * 1
        x3 = x3 + calc_binary(S_list[arg1][arg2][arg3])

    # 元の32bitに縮小転置
    for i in range(32):
        y.append(x3[P[i]-1])

    return y


# 暗号化アルゴリズム
def encryption(m:list, sub_key_list:list) ->list:
    n = 1

    m_list = []
    for i in range(64):
        # 転置する
        m_list.append(m[IP[i]-1])

    # 転置した平文(64bit)を左右に分ける(32bit毎に)
    L = m_list[:32]
    R = m_list[32:]

    # R(n-1)と各サブ鍵(n)をラウンド関数で計算
    for k in sub_key_list:
        y = f(R, k)

        # L(n-1)とy(n-1)で排他的論理和を取る
        for i in range(32):
            L[i] = calc_xor(L[i], y[i])
        
        # 施行が16回目でなければ、L(n-1)とR(n-1)を入れ替える
        if n != 16:
            L, R = R, L
        n += 1

    c = []
    # 16回施行後、L(16)とR(16)を連結させる
    LR = L + R
    for i in range(64):

        # 逆転置させる
        c.append(LR[IP_inverse[i]-1])

    # 暗号化文を返す
    return c


# 復号化アルゴリズム
def decryption(c:list, reverse_sub_key_list:list) -> list:
    n = 1
    
    c_list = []
    for i in range(64):
        c_list.append(c[IP[i]-1])

    L = c_list[:32]
    R = c_list[32:]

    for k in reverse_sub_key_list:
        if n != 1:
            L, R = R, L
        y = f(R, k)
        for i in range(32):
            L[i] = calc_xor(L[i], y[i])
        n += 1

    m = []
    LR = L + R
    for i in range(64):
        m.append(LR[IP_inverse[i]-1])

    return m


# 実行
if __name__ == '__main__':

    # 平文の生成
    m = random.choices(bit_list, k=64)
    print(f'平文：{m}')

    # 秘密鍵の生成
    secret_key_obj = SecretKey()
    secret_key = secret_key_obj.generate()

    # 暗号化サブ鍵の生成
    enc_sub_key_obj = EncSubKey()
    enc_sub_key_list = enc_sub_key_obj.generate(secret_key)

    # 復号化用サブ鍵の生成
    dec_sub_key_obj = DecSubKey()
    dec_sub_key_list = dec_sub_key_obj.generate(secret_key)

    # 平文を暗号化
    c = encryption(m, enc_sub_key_list)

    # 暗号文を復号化
    m = decryption(c, dec_sub_key_list)

    print(f'暗号文：{c}')
    print(f'復号化した平文：{m}')
