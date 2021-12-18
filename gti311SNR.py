import math

def nonSigne(arr, n):
    arr2 = [(val/2**n)*2-1 for val in arr]
    print(arr2)


def signe(arr, n):
    arr2 = [((val + 2**(n-1))/2**n) * 2 - 1 for val in arr]
    print(arr2)


def printNumber(value1, value2):
    print(value1)
    print(value2)


def snr(original, compare):
    vsignal = sum([val ** 2 for val in original])
    vbruit = sum([(val1 - val2) ** 2 for val1, val2 in zip(original, compare)])
    printNumber(vsignal, vbruit)


def stereoToMono(arr):
    a = iter(arr)
    arr2 = []
    for i, j in zip(a, a):
        arr2.append( math.floor(0.5 * (i+j)))

    print(arr2)


def monoToStereo(arr):
    arr2 = []
    for i in arr:
        arr2.append(i)
        arr2.append(i)

    print(arr2)


monoToStereo([111, 118, 127, 122, 119, 112, 109, 124, 137, 144])
snr([111, 111, 118, 118, 127, 127, 122, 122, 119, 119, 112, 112, 109, 109, 124, 124, 137, 137, 144, 144], [115, 115, 121, 124, 133, 125, 115, 117, 115, 126, 113, 113, 103, 105, 130, 126, 134, 136, 136, 137])
