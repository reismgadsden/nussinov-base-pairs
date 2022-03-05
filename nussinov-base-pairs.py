"""
Nussinov base pairs.
Program that predicts a rna sequence's secondary structure.

:author - Reis Gadsden
:version - 02/03/2022
:github - https://github.com/reismgadsden/nussinov-base-pairs

:class - CS-5531 @ Appalachian State University
:instructor - Mohammad Mohebbi
"""


# needed imports
import numpy as np


# main method that will 'probably' make calls to all other methods
def main() -> None:
    s = "AUCG"
    max_base_pairs(s)


def max_base_pairs(s) -> None:
    N = np.empty((len(s), len(s)))
    N.fill(np.NaN)

    for i in range(0, len(s)):
        N[i, i] = 0
        if i != 0:
            N[i, i-1] = 0
    print(np.matrix(get_secondary_struct(N, s)))


def get_secondary_struct(N, s) -> None:
    for j in range(1, 4):
        for i in range(0, 4 - j):
            #print("i = " + str(i) + "; j =" + str(j + i) + ";")
            N[i, j + i] = get_max(N, s, i, j + i)
    return N


def get_max(N, s, i, j):
    print("i = " + str(i) + "; j =" + str(j) + ";")
    first_case = N[i + 1, j]

    k_arr = []
    for k in (i + 1, j):
        print("k = " +str(k) + ";")
        if is_pair(s[i], s[k]):
            k_arr.append(k)

    x = 1
    for k in k_arr:
        print("j = " + str(j) + "; k = " + str(k) + ";")
        if (k + 1) < len(s):
            x += N[i + 1, k - 1] + N[k + 1, j]
        else:
            x += N[i + 1, k - 1]

    return max(first_case, x)


def is_pair(c1, c2) -> bool:
    look_up = {
        'A': ['U','T'],
        'C': ['G'],
        'G': ['C', 'U'],
        'T': ['A'],
        'U': ['A']
    }

    return c2 in look_up[c1]

if __name__ == "__main__":
    main()