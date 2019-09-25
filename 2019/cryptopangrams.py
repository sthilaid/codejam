#!/usr/bin/python3

import functools
# import io
# import itertools
# import math
import random
import sys

def findPrimes(N):
    primes = set([2])
    nonprimes = set()
    p = 2
    while p <= N:
        primes.add(p)
        for i in range(2, N+1):
            x = i * p
            if x <= N:
                nonprimes.add(x)
            else:
                break
        while True:
            p += 1
            if p not in nonprimes:
                break
            elif p > N:
                break
    return primes

def solveCase(i, N, cyphertext, expectedClearTextStr=None):
    def findCypherPrime(index, cypherData, cyphertext, dir=1, debug=False):
        if debug:
            print("findCypherPrime(%d, %s, %s, %d)" % (index, cypherData, cyphertext, dir))
        if len(cypherData) != len(cyphertext):
            raise Exception("Unexpected lengths of cypherdata/cyphertext (%d/%d)"
                            % (len(cypherData), len(cyphertext)))
        nextIndex = index+dir
        if debug:
            print("len(cypherData): %d, index: %d, nextIndex: %d"
                  % (len(cypherData), index, nextIndex))
        # if index >= len(cypherData) or index < 0:
        #     return False
        primeIndex = 0
        if nextIndex >= len(cypherData) or nextIndex < 0:
            if dir > 0:
                return findCypherPrime(index, cypherData, cyphertext, -dir, debug)
            else:
                return False
        if cyphertext[index] != cyphertext[nextIndex]:
            primeIndex = 1 if cypherData[index][0] in cypherData[index+dir] else 0
            if dir < 0:
                primeIndex = (primeIndex+1) % 2
            return cypherData[index][primeIndex]
        else:
            nextPrime = findCypherPrime(nextIndex, cypherData, cyphertext, dir, debug)
            if nextPrime:
                primeIndex = 1 if nextPrime == cypherData[index][0] else 0
            else:
                prevOtherPrime = findCypherPrime(index-dir, cypherData, cyphertext, -dir, debug)
                if not prevOtherPrime:
                    raise Exception("Unabled to find prime value for index %d in %s"
                                    % (index, cypherData))
                primeIndex = 0 if prevOtherPrime == cypherData[index][0] else 1
            return cypherData[index][primeIndex]
        
    primes = findPrimes(N)
    cypherData = []
    for cypherIndex, cypher in enumerate(cyphertext):
        for p in primes:
            if cypher % p == 0:
                cypherData.append((p, int(cypher/p)))
                break
        if len(cypherData) != cypherIndex+1:
            raise Exception("invalid data extracted: %d != %d"
                            % (len(cypherData), cypherIndex))
    alphabet = set()
    for data in cypherData:
        alphabet.add(data[0])
        alphabet.add(data[1])
    alphabet = sorted(alphabet)

    cleartextKeys = []
    for dataIndex in range(len(cypherData)):
        cleartextKeys.append(findCypherPrime(dataIndex, cypherData, cyphertext, 1))
        if not cleartextKeys[-1]:
            findCypherPrime(dataIndex, cypherData, cyphertext, 1, True)
            raise Exception("Couldn't find key for dataIndex: %d" % dataIndex)
    primeIndex = 1 if cleartextKeys[-1] == cypherData[-1][0] else 0
    cleartextKeys.append(cypherData[-1][primeIndex])
        
    cleartext = [chr(ord('A') + alphabet.index(key)) for key in cleartextKeys]
    cleartextStr = "".join(cleartext)
    print("Case #%d: %s" % (i, cleartextStr))

    if expectedClearTextStr and cleartextStr != expectedClearTextStr:
        print("*** Debug info dump ****")
        print("i: %d, N: %d, L: %d" % (i, N, len(cyphertext)))
        print(cyphertext)
        print(cypherData)
        print([(chr(ord('A')+i), letter) for i, letter in enumerate(alphabet)])
        print(cleartextKeys)
        print("%s != %s" % (cleartextStr, expectedClearTextStr))
        raise Exception("Invalid decyphered text!")

    return cleartextStr
    
def solve(input, cleartexts=None):
    data = input.split(sep="\n")
    count = int(data[0])
    casesData = data[1:len(data)]

    results = []
    for i in range(count):
        firstRow = casesData[i*2].split()
        N = int(firstRow[0])
        L = int(firstRow[1])
        ciphertext = [int(x) for x in casesData[i*2+1].split()]
        if len(ciphertext) != L:
            raise Exception("expecting %d cipher text elements, found %d"
                            % (L, len(ciphertext)))
        if cleartexts and i >= len(cleartexts):
            raise Exception("no cleartext matching cypher text for index %d" % i)
        results.append(solveCase(i+1, N, ciphertext, cleartexts[i] if cleartexts else None)) #case num starts at 1
    return results

def test(count, maxN):
    input = "%d\n" % count
    cleartexts = []
    for _ in range(count):
        N = random.randrange(101, maxN)
        L = random.randrange(25, 101)
        primes = list(findPrimes(N))
        selectedPrimes = []
        for _ in range(26):
            primeIndex = random.randrange(len(primes))
            selectedPrimes.append(primes[primeIndex])
            primes.remove(primes[primeIndex])
        selectedPrimes = sorted(selectedPrimes)
        clearText = list(range(26))
        missingLettersCount = L+1 - len(clearText)
        for _ in range(missingLettersCount):
            clearText.append(random.randrange(26))
        if len(clearText) != L+1:
            raise Exception("unexpected clearText length (%d) expecting %d"
                            % (len(clearText), L+1))
        randimizationItCount = random.randrange(len(clearText) * 5)
        for _ in range(randimizationItCount):
            i1 = random.randrange(len(clearText))
            i2 = random.randrange(len(clearText))
            clearText[i1], clearText[i2] = clearText[i2], clearText[i1]
        clearTextStr = "".join([chr(ord('A')+ x) for x in clearText])
        cleartexts.append(clearTextStr)
        ciphertext = []
        for i in range(1,len(clearText)):
            ciphertext.append(selectedPrimes[clearText[i-1]] * selectedPrimes[clearText[i]])
            # print("    [%d - %s/%s] %d * %d => %d" %(i, clearText[i-1], clearText[i],
            #                                  selectedPrimes[clearText[i-1]],
            #                                  selectedPrimes[clearText[i]],
            #                                  ciphertext[-1]))
        ciphertextStr = functools.reduce(lambda a,x: a+"%d " % x, ciphertext, "")
        input += "%d %d\n%s\n" % (N, L, ciphertextStr[:len(ciphertextStr)-1])
    print("--test input--")
    print(input)
    print("--output--")
    results = solve(input, cleartexts)
    print("--results--")
    for i in range(len(results)):
        if cleartexts[i] == results[i]:
            print("case #%2d [OK]" % (i+1))
        else:
            print("case #%3d [FAILED] input: %s" % (i+1, cleartexts[i]))
            print("                  output: %s" % (results[i]))

testcase = """2
103 31
217 1891 4819 2291 2987 3811 1739 2491 4717 445 65 1079 8383 5353 901 187 649 1003 697 3239 7663 291 123 779 1007 3551 1943 2117 1679 989 3053
10000 25
3292937 175597 18779 50429 375469 1651121 2102 3722 2376497 611683 489059 2328901 3150061 829981 421301 76409 38477 291931 730241 959821 1664197 3057407 4267589 4729181 5335543"""

def main():
    input = ""
    for i in sys.stdin:
        input += i
    solve(input)

if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
