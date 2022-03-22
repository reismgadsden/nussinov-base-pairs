"""
Nussinov base pairs.
Program that predicts a rna sequence's secondary structure.

:author - Reis Gadsden
:version - 21/03/2022
:github - https://github.com/reismgadsden/nussinov-base-pairs

:class - CS-5531 @ Appalachian State University
:instructor - Mohammad Mohebbi
"""


# needed imports
import numpy as np


# main method that will 'probably' make calls to all other methods
def main() -> None:
    s = "UUCUCCAGUGAGACGAAAACCAAUGCCUUCACUGGCAGUAACACCCAGCUUCCUGAACGCAUGUCAUGCAUGCCAGGUUUUGUUGGUU"
    max_base_pairs(s)


def max_base_pairs(s) -> None:
    N = np.empty((len(s), len(s)))
    N.fill(np.NaN)

    BT = np.empty((len(s), len(s)))
    BT.fill(np.NaN)

    for i in range(0, len(s)):
        N[i, i] = 0
        BT[i, i] = -2
        if i != 0:
            N[i, i-1] = 0
            BT[i, i - 1] = -2
    fill_score_array(N, BT, s, 5)
    print(calc_second_struct(BT, 0, len(s) - 1, len(s) * "."))


def fill_score_array(N, BT, s, min_loop_len) -> None:
    for j in range(1, len(s)):
        for i in range(0, len(s) - j):
            N[i, j + i] = get_max(N, BT, s, i, j + i, min_loop_len)
    return N


def get_max(N, BT, s, i, j, min_loop_len):
    if i  >= j - min_loop_len:
        BT[i][j] = -2
        return 0
    first_case = N[i + 1, j]

    k_arr = []
    for k in range(i + 1, j+1):
        if is_pair(s[i], s[k]):
            k_arr.append(k)

    x = 0
    if k_arr:
        for k in k_arr:
            temp = 0
            if i >= k - min_loop_len:
                x = -1
                BT[i][j] = -2
            else:
                if (k + 1) < len(s):
                    temp = N[i + 1, k - 1] + N[k + 1, j]
                else:
                    temp = N[i + 1, k - 1]
                if temp > x or temp == x:
                    BT[i][j] = k
                x = max(temp, x)
        x += 1

    if first_case > x or first_case == x:
        BT[i][j] = -1
    return max(first_case, x)


def calc_second_struct(BT, i, j, output) -> str:

    if i >= len(output) or j >= len(output):
        return output
    else:
        k = BT[i][j]
        if k == -2:
            return output
        elif k == -1:
            output = calc_second_struct(BT, i+1, j, output)
            return output
        elif k == np.NaN:
            print("Something has gone terribly wrong")
            return output
        else:
            k = int(k)
            output = output[0:i] + "(" + output[i+1:len(output)]
            output = output[0:k] + ")" + output[k+1:len(output)]
            output = calc_second_struct(BT, i + 1, k - 1, output)
            output = calc_second_struct(BT, k + 1, j, output)
            return output


def is_pair(c1, c2) -> bool:
    look_up = {
        'A': ['U'],
        'C': ['G'],
        'G': ['C'],
        'T': ['A'],
        'U': ['A']
    }

    return c2 in look_up[c1]

if __name__ == "__main__":
    main()