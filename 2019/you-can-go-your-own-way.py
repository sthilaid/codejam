#!/usr/bin/python3

import functools
import io
import itertools
import math
import random
import sys

shouldVerify = False

class simpleLinkedList():
    class iterator():
        def __init__(self, node):
            head = simpleLinkedList(None)
            head.next = node
            self.node = head
        def __iter__(self):
            return self
        def __next__(self):
            if self.node and self.node.next:
                self.node = self.node.next
                return self.node.value
            else:
                raise StopIteration()
        def __repr__(self):
            return "iterator(%s)" % self.node
            
    def __init__(self, val):
        self.prev   = None
        self.next   = None
        self.value  = val

    def link(n1, n2):
        if not n1 or not n2:
            return 
        n1.next = n2
        n2.prev = n1

    def stringify(self):
        outStr = ""
        node = self
        while node:
            outStr += str(node.value)
            node = node.next
        return outStr

    def __iter__(self):
        return self.iterator(self)

    def __repr__(self):
        return "simpleLinkedList(%s)" % self.value

    def __str__(self):
        prefix = "[" if not self.prev else ""
        if self.next:
            return prefix + "%s - %s" % (self.value, str(self.next))
        else:
            return prefix + "%s]" % (self.value)
        
def findBackwardPath(target, moveDict, x, y, solution):
    # print("findBackwardPath(%s, dict, %d, %d, %s)" % (target, x, y, str(solution)))
    if solution == False:
        raise Exception("invalid solution: %s [target: %s, (x,y): %s]"
                        % (solution, target, (x,y)))
    if x < target[0] or y < target[1]:
        return False
    elif x == target[0] and y == target[1]:
        return solution
    
    newSolution = False
    if x > target[0] and (not (x-1,y) in moveDict or moveDict[(x-1,y)] != (x,y)):
        newNode = simpleLinkedList("E")
        simpleLinkedList.link(newNode, solution)
        newSolution = findBackwardPath(target, moveDict, x-1, y, newNode)

    if (not newSolution
        and y > target[1]
        and (not (x,y-1) in moveDict
             or moveDict[(x,y-1)] != (x,y))):
        newNode = simpleLinkedList("S")
        simpleLinkedList.link(newNode, solution)
        newSolution = findBackwardPath(target, moveDict, x, y-1, newNode)

    return newSolution

def solveCase(i, N, moves):
    moveDict = dict()
    x, y = 0, 0
    for m in moves:
        lastX, lastY = x, y
        if m == "E":
            x += 1
        else:
            y += 1
        moveDict[(lastX, lastY)] = (x,y)

    step = 5
    itCount = max(int(N / step), 1)
    solution = None
    x, y = 0,0
    for j in range(itCount+1):
        # itSize  = min(j * step, N-1)
        x, y    = tuple(itertools.repeat(max(0, N-1-(j*step)), 2))
        target  = tuple(itertools.repeat(max(0, N-1-((j+1)*step)), 2))
        # print("N: %d, itCount: %d, target: %s, x: %d, y: %d"
        #       % (N, itCount, target, x, y))
        solution = findBackwardPath(target, moveDict, x, y, solution)
    print("case #%d: %s" % (i, solution.stringify()))
    if shouldVerify:
        # print("input: %s output: %s" % ("".join(moves), solution.stringify()))
        print("-- verification -- input: %s, output: %s" % (verify(N, moves), verify(N, solution)))



    
def solve(input):
    data = input.split(sep="\n")
    count = int(data[0])
    casesData = data[1:len(data)-1]
    if len(casesData) != count * 2:
        raise Exception("expecting %d cases but only found %d..." % (count*2, len(casesData)))
    for i in range(count):
        N = int(casesData[i*2])
        moves = casesData[i*2+1]
        solveCase(i+1, N, moves) #case num starts at 1

def test(count, maxN):
    input = "%d\n" % count
    for _ in range(count):
        N = random.randrange(2, maxN)
        moves = []
        e, s = 0, 0
        while True:
            move = None
            if e == N-1:
                move = "S"
                s += 1
            elif s == N-1:
                move = "E"
                e += 1
            else:
                if random.random() > 0.5:
                    move = "E"
                    e += 1
                else:
                    move = "S"
                    s += 1
            moves.append(move)
            if e == N-1 and s == N-1:
                break
        input += "%d\n%s\n" % (N, "".join(moves))
    print("--test input--")
    print(input)
    print("--output--")
    solve(input)

def verify(N, moves):
    e, s = 0, 0
    for m in moves:
        if m == "E":
            e += 1
        else:
            s += 1
    return e == N-1 and s == N-1

def main():
    input = ""
    for i in sys.stdin:
        input += i
    solve(input)

if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()

