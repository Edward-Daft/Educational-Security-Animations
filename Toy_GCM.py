def encrypt(x, y, const):
    Intx = int(x, 2)
    Inty = int(y, 2)
    CT = (Intx + Inty + const) % 16
    BCT = format(CT, '04b')
    return BCT

def XOR(a, b):
    counter = 0
    result = ''
    for character in a:
        if character == b[counter]:
            result = result + str(0)
        else:
            result = result + str(1)
        counter += 1
    return result

def perform_toy_GCM(plaintext, key, iv):
    print("Performing toy GCM")
    PT = plaintext
    K = key
    I = iv
    Int_i = int(I, 2)
    const = 10
    CT = []
    KS = []
    Iv_list = []
    Y_list = []

    # Creating keystreams
    counter = 0
    for i in PT:
        counter += 1
        TempIV = Int_i + counter
        TempIV = format(TempIV, '04b')
        Iv_list.append(TempIV)
        KS.append(encrypt(TempIV, K, const))

    # Encrypting plaintext blocks
    counter = 0
    for PT_block in PT:
        CT.append(XOR(PT_block, KS[counter]))
        counter += 1

    # Creating authentication tag
    Y = '0000'
    H = encrypt(K, Y, const)
    Y_list.append(Y)

    for block in CT:
        Y = XOR(block, Y)
        Y_list.append(Y)
        IntY = (int(Y, 2) * int(H, 2)) % 16
        Y = format(IntY, '04b')
        Y_list.append(Y)

    print(CT, Y_list)
    return Iv_list, KS, CT, Y_list, H

"""
BPlainText = ["0001", "1100", "0011"]
BKey = "1111"
BIV = "0010"
print(perform_toy_GCM(BPlainText, BKey, BIV))
"""