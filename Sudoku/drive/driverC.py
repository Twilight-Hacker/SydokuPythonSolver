import sys
from math import floor
from copy import deepcopy
from _collections import deque


class Sudoku():
    def __init__(self, tabl):
        if(len(tabl)==81):
            self.table = [str(x) for x in tabl]
        else:
            print len(tabl)
            raise Exception("Illegal Input")
        
    def setElement(self, n, i):
        if(i<0) | (i>80):
            print "index: " + str(i)
            raise Exception("Illegal Index")
        if(n<1) | (n>9):
            print "Entry: " + str(n)
            raise Exception("Illegal Entry")
            
        self.table[i] = str(n)
        
    def isSolved(self):
        return not "0" in self.table
    
    def isOpen(self, i):
        return self.getNum(i)=="0"
        
    def getLine(self, i):
        if(i<0) | (i>8):
            print "index: " + str(i)
            raise Exception("Illegal Index")
        s = i*9
        res = []
        for k in range(9):
            res.append(self.getNum(s+k))
        return res
        
    def getCol(self, i):
        if(i<0) | (i>8):
            print "index: " + str(i)
            raise Exception("Illegal Index")
        res = []
        for k in range(9):
            res.append(self.getNum(k*9 + i))
        return res
    
    def getSquare(self, num):
        if(num<0) | (num>8):
            return None
        res = []
        s = int( floor(num/3)*27 + 3*(num%3) )
        for i in range(3):
            for j in range(3):
                res.append(self.getNum(s + 9*i + j))
                 
        return res
        
    def getNum(self, num):
        if(num<0) | (num>80):
            print "Index: " + str(num)
            raise Exception("Illegal Index")
        return self.table[num]
    
    @staticmethod
    def getLineNum(i):
        return int(floor(i/9))
    
    @staticmethod    
    def getColNum(i):
        return int(i%9)
    
    @staticmethod
    def getTableIndex(line, col):
        return int(line*9 + col)
    
    def isValidElement(self, num, i):
        if(self.getNum(i)!="0"):
            return False
        rel = Sudoku.getRelevantIndexes(i)
        for x in rel:
            if str(num) == self.getNum(x):
                return False
        return True
    
    def getTable(self):
        return self.table
    
    def getTableString(self):
        return ''.join(str(x) for x in self.table)
    
    @staticmethod
    def getLineIndexes(i):
        l = list()
        lineNum = Sudoku.getLineNum(i)
        for col in range(9):
            l.append(Sudoku.getTableIndex(lineNum, col))
        
        return l
    
    @staticmethod
    def getColIndexes(i):
        l = list()
        colNum = Sudoku.getColNum(i)
        for line in range(9):
            l.append(Sudoku.getTableIndex(line, colNum))
        
        return l
    
    @staticmethod
    def getSquareNum(i):
        line = Sudoku.getLineNum(i)
        col = Sudoku.getColNum(i)
        return int(floor(col/3)+3*floor(line/3))
        
        
    @staticmethod
    def getSquareIndexes(i):
        l = list()
        num = Sudoku.getSquareNum(i)
        s = int( floor(num/3)*27 + 3*(num%3) )
        for i in range(3):
            for j in range(3):
                l.append(s + 9*i + j)
        return l
        
    @staticmethod
    def getRelevantIndexes(i):
        l = []
        lineI = Sudoku.getLineIndexes(i)
        for line in lineI:
            if(line not in l):
                l.append(line)
        lineI = Sudoku.getColIndexes(i)
        for line in lineI:
            if(line not in l):
                l.append(line)
        lineI = Sudoku.getSquareIndexes(i)
        for line in lineI:
            if(line not in l):
                l.append(line)
        return l
        
    def printTableLine(self):
        print ''.join(str(x) for x in self.table)
    
    def printTable(self):
        for i in range(9):
            line = ""
            for j in range(9):
                line += self.getNum(i*9 + j) + " "
                if(j%3==2):
                    line += " "
            if(i%3==2):
                line += "\n"
            print line

class Node():
    def PrintNodeTable(self):
        #TODO Print the node's table
        for i in range(9):
            line = ""
            for j in range(9):
                num = self.getSudoku().getNum(i*9 + j) + " "
                if( str(num) == "0"):
                    line += str(self.getPossibleValues(i*9 + j))
                else:
                    line += num
                if(j%3==2):
                    line += " "
            if(i%3==2):
                line += "\n"
            print line

    
    def __init__(self, s):
        self.sudoku = s
        self.possibles = list()
        allPossibles = [1,2,3,4,5,6,7,8,9]
        for i in range(81):
            newPossibles = []
            for n in allPossibles:
                if(self.sudoku.isValidElement(n, i) ):
                    newPossibles.append(n)
            #print "Possible Values: " + str(newPossibles) + " for " + str(i) + "th element" 
            self.possibles.append(newPossibles)
    
    def getSudoku(self):
        return self.sudoku
    
    def selectMinIndex(self):
        l = 20
        res = -1
        
        for i in range(81):
            #print self.possibles[i]
            if(len(self.getPossibleValues(i))>0):
                if(len(self.getPossibleValues(i))<l):
                    l = len(self.getPossibleValues(i))
                    res = i
                    #print self.possibles[i]
            else:
                if(self.getSudoku().isOpen(i)):
                    #self.getSudoku().printTable()
                    #print "Possibles: " + str(self.possibles[i]) + " at index " + str(i)
                    return -1
        return res
        
    
    def removePossibleValue(self, n, i):
        d = self.possibles[i]
        d.remove(n)
        #print "RPV " + str( (i,n) )
    
    def getPossibleValues(self, inde):
        #print "GPS" + str( (inde, self.possibles[inde]) )
        if(self.getSudoku().isOpen(inde)):
            return self.possibles[inde]
        else:
            return list()
        return self.possibles[inde]
        
    def foundIndex(self, n, i):
        poss = self.getPossibleValues(i)
        while(poss):
            #print "Removing " + str( poss[0] )
            self.removePossibleValue(poss[0], i)
        
        rel = Sudoku.getRelevantIndexes(i)
        #print rel
        for a in rel:
            if(n in self.getPossibleValues(a)):
                self.removePossibleValue(n, a)
        
        
def ac3(node):
    '''
    For illustration, here is an example of a very simple constraint problem: X (a variable) has the possible values {0, 1, 2, 3, 4, 5} 
    -- the set of these values are the domain of X, or D(X). The variable Y likewise has the domain D(Y) = {0, 1, 2, 3, 4, 5}. 
    Together with the constraints C1 = "X must be even" and C2 = "X + Y must equal 4" we have a CSP which AC-3 can solve. 
    Notice that the actual constraint graph representing this problem must contain two edges between X and Y since C2 is undirected but 
    the graph representation being used by AC-3 is directed.

    It does so by first removing the non-even values out of the domain of X as required by C1, leaving D(X) = { 0, 2, 4 }. 
    It then examines the arcs between X and Y implied by C2. Only the pairs (X=0, Y=4), (X=2, Y=2), and (X=4, Y=0) match the constraint C2. 
    AC-3 then terminates, with D(X) = {0, 2, 4} and D(Y) = {0, 2, 4}.

    '''
    #node.getSudoku().printTable()
    while( not node.getSudoku().isSolved()):
        #node.getSudoku().printTableLine()
        minInd = node.selectMinIndex()
        #print minInd
        if(minInd>=0):
            poss = node.getPossibleValues(minInd)
            #print (minInd, poss)
            if(len(poss)==1):
                n = poss[0]
                node.foundIndex(n, minInd)
                node.getSudoku().setElement(n, minInd)
                #print "Element " + str( (Sudoku.getLineNum(minInd)+1, 1+Sudoku.getColNum(minInd)) ) + ": " + str(n)
            else:
                return node.getSudoku()
        else:
            return node.getSudoku()
        
        #node.PrintNodeTable()
        #raw_input("Press a key...")
    
    return node.getSudoku()
    
def backtrack2(node):
    while( not node.getSudoku().isSolved()):
        #node.getSudoku().printTableLine()        
        minInd = node.selectMinIndex()
        if(minInd>-1):
            poss = node.getPossibleValues(minInd)
            if(len(poss)==1):
                n = poss[0]
                node.getSudoku().setElement(n, minInd)
                node.foundIndex(minInd, n)
            elif(len(poss)==0):
                if(node.getSudoku().isOpen(minInd)):
                    return None
            else:
                print "Call Deepen"
                for i in range(len(poss)):
                    print "Switch: " + str(i+1) +" of " + str(len(poss))
                    node2 = deepcopy(node)
                    n = poss[i]
                    node2.getSudoku().setElement(n, minInd)
                    node2.foundIndex(n, minInd)
                    trial = backtrack(node2)
                    if(trial):
                        return trial
                    else:
                        print "Call Switch"
                        continue
                print "Call Return"
                return None
        elif(minInd==-128):
            return None
    return node.getSudoku()

def backtrack(node):
    fringe = []
    fringe.append(node)
    
    explored = set()
    explored.add(node.getSudoku())
    
    while( not len(fringe)==0):
        currentNode = fringe.pop()
        
        #f.write( currentNode.getSudoku().getTableString() + "\n")

        if(currentNode.getSudoku().isSolved()):
            #currentNode.getSudoku().printTable()
            return currentNode.getSudoku()
                
        minInd = currentNode.selectMinIndex()
        
        if(minInd>-1):
            poss = currentNode.getPossibleValues(minInd)
            for n in poss:
                node2 = deepcopy(currentNode)
                #print (minInd, poss[i])
                node2.getSudoku().setElement(n, minInd)
                node2.foundIndex(n, minInd)
                if(node2.getSudoku() not in explored):
                    fringe.append(node2)
                    explored.add(node2.getSudoku())
                
                #node2.getSudoku().printTable()
                #raw_input("Press Enter")
            #print "Added " + str(len(poss))
            
        #raw_input("Press Enter...")      
    return None

'''
THE MISTAKE IS SOMEWHERE IN POSSIBLE VALUE REMOVAL
RECHECK LINE NUMBERS, COLUMN NUMBERS, SQUARE NUMBERS AND TABLE INDICES


f = open('temp.txt', 'w')
t = sys.argv[1]
s = Sudoku(t)
node = Node(s)
solved = backtrack(deepcopy(node), f)
if(solved):
    print "Done Backtrack: " + str(solved.getTableString())
else:
    print "Backtrack Failed"

f.close()
'''

f_a = open('output_ac3.txt', 'w')
f_b = open('output_backtrack.txt', 'w')

completed = deque()

with open("sudokus_finish.txt") as fFin:
    for st in fFin:
        t = ''.join(e for e in st if e.isalnum())
        completed.append(t)

with open("sudokus_start.txt") as fIn:
    for st in fIn:
        t = ''.join(e for e in st if e.isalnum())
        print "Starting " + str(t)
        sud = Sudoku(t)
        node = Node(sud)
        
        solved = ac3(deepcopy(node))
        if(solved.isSolved()):
            print "AC3 Done: " + str(solved.getTableString())
            #TODO: Remove the newline characters before submitting
            f_a.write(str(solved.getTableString()) + "\n")
        else:
            print "AC3 Failed"
            f_a.write("Failed \n")
        
        solved = backtrack(deepcopy(node))
        if(solved):
            print "Backtrack: " + str(solved.getTableString())
            #TODO: Remove the newline characters before submitting
            f_b.write(str(solved.getTableString()) + "\n")
        else:
            print "Backtrack Failed"
            f_b.write("Failed\n")
        
        f=completed.popleft()
        print "Correct  " + str(f)
        print "\n"
    
f_a.close()
f_b.close()

 
