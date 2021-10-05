
# from z3 import *

class Helper:

    def __init__(self, blockno, initval):
        self.blockno = blockno  # block info of puzzle
        self.initval = initval  # initial values of current puzzle
        self.m = len(self.blockno)  # number of rows
        self.n = len(self.blockno[0])  # number of columns
        self.R = range(self.m)
        self.C = range(self.n)
        self.bmax = max(
            [self.blockno[i][j] for i in self.R for j in self.C])  # maximum no. of blocks in the current puzzle

    # returns the maximum no. of blocks in the current puzzle
    def getBlockNumber(self):
        return self.bmax
