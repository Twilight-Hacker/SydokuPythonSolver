import sys
from math import floor
from copy import deepcopy


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
            self.possibles.append(newPossibles)
    
    def getSudoku(self):
        return self.sudoku
    
    def selectMinIndex(self):
        l = 20
        res = -1
        
        for i in range(81):
            if(len(self.getPossibleValues(i))>0):
                if(len(self.getPossibleValues(i))<l):
                    l = len(self.getPossibleValues(i))
                    res = i
            else:
                if(self.getSudoku().isOpen(i)):
                    return -1
        return res
        
    
    def removePossibleValue(self, n, i):
        d = self.possibles[i]
        d.remove(n)
    
    def getPossibleValues(self, inde):
        if(self.getSudoku().isOpen(inde)):
            return self.possibles[inde]
        else:
            return list()
        return self.possibles[inde]
        
    def foundIndex(self, n, i):
        poss = self.getPossibleValues(i)
        while(poss):
            self.removePossibleValue(poss[0], i)
        
        rel = Sudoku.getRelevantIndexes(i)
        for a in rel:
            if(n in self.getPossibleValues(a)):
                self.removePossibleValue(n, a)
        
        

def backtrack(node):
    fringe = []
    fringe.append(node)
    
    explored = set()
    explored.add(node.getSudoku())
    
    while( not len(fringe)==0):
        currentNode = fringe.pop()
        

        if(currentNode.getSudoku().isSolved()):
            return currentNode.getSudoku()
                
        minInd = currentNode.selectMinIndex()
        
        if(minInd>-1):
            poss = currentNode.getPossibleValues(minInd)
            for n in poss:
                node2 = deepcopy(currentNode)
                node2.getSudoku().setElement(n, minInd)
                node2.foundIndex(n, minInd)
                if(node2.getSudoku() not in explored):
                    fringe.append(node2)
                    explored.add(node2.getSudoku())
                
    return None


t = sys.argv[1]
s = Sudoku(t)
node = Node(s)
solved = backtrack(node)

f_out = open('output.txt', 'w')

f_out.write(str(solved.getTableString()))

f_out.close()


 
