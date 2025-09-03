from cell import Cell
import random as rng
import numpy as np

class Board:
    def __init__(self, size):
        self.size = size
        self.array = [[Cell() for i in range(size)] for j in range(size)]

    def printArray(self):
        print(np.matrix(self.array))

    def populate(self, mineCount): #throw mines everywhere on that john
        # realCount = amount of mines on board
        # if mineCount != realCount, keep going
        # else stop
        realCount = 0
        while(realCount < mineCount):
            row = rng.randint(0, 9)
            col = rng.randint(0, 9)

            if self.array[row][col].val == 0: # if the cell is empty, place a mine and increment realCount
                realCount = realCount + 1
                self.array[row][col].val = 9 # place a mine. will be -1 but it's 9 for now for readability
                print(f"mine {realCount} placed at {row}, {col}")# debug print statement
            
            else:
                print(f"mine placement failed at {row}, {col}")

    def getAdjacentIndices(matrix, row, col):
        rows = len(matrix)
        cols = len(matrix[0]) if matrix else 0
        
        directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1),     # N, S, W, E
            (-1, -1), (-1, 1), (1, -1), (1, 1)    # NW, NE, SW, SE
        ]  # up, down, left, right
        adjacent = []

        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < rows and 0 <= c < cols:
                adjacent.append((r, c))

        return adjacent

    #def update(self):
        # next we have to add adjacency values to each cell
        # iterate through the array and look for a clear spot (0)
        print("updating")
        rowCount = -1
        for row in self.array:
            rowCount = rowCount + 1
            for col in range(len(row)):
                # when a clear spot is found, check every spot around it and add up mines
                
                if row[col].val == 0:
                    for val in self.getAdjacentIndices(self.array, rowCount, col):
                        print(val)
        
        
        # after, set cell.val to the amount of mines found







#debug
#b = Board(10)
#b.populate(25)
#b.printArray()

