
#!/usr/bin/python3

import functools
import io
import math
import random
import sys

def solveCase(i, N):
    startValue = N
    x1 = 0
    x2 = 1
    N -= 1
    startExponent = math.floor(math.log10(N))
    for exponent in range(startExponent, -1, -1):
        base    = pow(10, exponent)
        digit   = math.floor(N / base)
        val     = digit * base
        N -= val
        if digit == 4:
            x1 += 2 * base
            x2 += 2 * base
        else:
            x1 += val
            
    print("Case #%d: %d %d" % (i, x1, x2))
    # print("%d + %d = %d ==? %d: %s" % (x1, x2, x1+x2, startValue, x1+x2 == startValue))

def solve(input):
    data = [int(x) for x in input.split()]
    count = data[0]
    cases = data[1:]
    if len(cases) != count:
        raise Exception("expecting %d cases but only found %d..." % (count, len(cases)))

    for i, N in enumerate(cases):
        solveCase(i+1, N) #case # starts at 1

def test(count, exp):
    input = "%d\n" % count
    for _ in range(count):
        input += "%d\n" % random.randrange(pow(10, exp))

    print("--test input--")
    print(input)
    print("--output--")
    solve(input)

def main():
    input = ""
    for i in sys.stdin:
        input += i
    solve(input)

if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
