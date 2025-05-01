# Adam Schantz, Cole Wendrowski, Adarsh Rajamanickam, Siena Landerkin
def hex_to_bin64(hex_key):
    return bin(int(hex_key, 16))[2:].zfill(64)

# permutation C. gives C(K) = C0
PC1_C = [57, 49, 41, 33, 25, 17, 9,
         1, 58, 50, 42, 34, 26, 18,
         10, 2, 59, 51, 43, 35, 27,
         19, 11, 3, 60, 52, 44, 36]
# permutation D. gives D(K) = D0
PC1_D = [63, 55, 47, 39, 31, 23, 15,
         7, 62, 54, 46, 38, 30, 22,
         14, 6, 61, 53, 45, 37, 29,
         21, 13, 5, 28, 20, 12, 4]
# each of the values of l, which we shift by 
SHIFT_SCHEDULE = [1, 1, 2, 2, 2, 2, 2, 2,
                  1, 2, 2, 2, 2, 2, 2, 1]
# permutation PC2, where PC2(Ci||Di) = Ki
PC2 = [14, 17, 11, 24, 1, 5,
       3, 28, 15, 6, 21, 10,
       23, 19, 12, 4, 26, 8,
       16, 7, 27, 20, 13, 2,
       41, 52, 31, 37, 47, 55,
       30, 40, 51, 45, 33, 48,
       44, 49, 39, 56, 34, 53,
       46, 42, 50, 36, 29, 32]
# permute the bits by the given table
def permute(bits, table):
    return ''.join(bits[i - 1] for i in table)
# get C0 and D0 from K
def get_C0_D0(key64):
    return permute(key64, PC1_C), permute(key64, PC1_D)
# left shift function
def left_shift(bits, n):
    return bits[n:] + bits[:n]
# given the previous C and D values, find Ci and Di
def get_Ci_Di(C0, D0):
    Ci = [C0]
    Di = [D0]
    for shift in SHIFT_SCHEDULE:
        Ci.append(left_shift(Ci[-1], shift))
        Di.append(left_shift(Di[-1], shift))
    return Ci[1:], Di[1:]
# with a given Ci and Di, combine and permute with PC2
def get_round_keys(C_list, D_list):
    round_keys = []
    for C, D in zip(C_list, D_list):
        combined = C + D
        round_keys.append(permute(combined, PC2))
    return round_keys
# given a key in hexadecimal, return 16 round keys
def generate_DES_round_keys(hex_key):
    key64 = hex_to_bin64(hex_key)
    C0, D0 = get_C0_D0(key64)
    C_list, D_list = get_Ci_Di(C0, D0)
    round_keys = get_round_keys(C_list, D_list)
    return round_keys
#main program
if __name__ == "__main__":
    hex_key = input("16 character hex key: ").replace(" ", "").strip()
    if len(hex_key) != 16:
        print("Error: Key must be exactly 16 hex characters (64 bits).")
    else:
        keys = generate_DES_round_keys(hex_key)
        for i, k in enumerate(keys, 1):
            print(f"K{i}: {k}")
