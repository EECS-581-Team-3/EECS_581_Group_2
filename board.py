from cell import Cell
import random as rng
import numpy as np

class Board:
    def __init__(self, size):
        self.size = size
        self.array = [[Cell() for i in range(size)] for j in range(size)]
        self.alive = True # changes to false when user gets blown up with a bomb
        self.BOMB_VALUE = 9 #Value to indicate cell is a bomb


    def printArray(self): # now with labeled edges
        print("  " + str([i for i in range(self.size)]))
        #print(np.matrix(self.array))
        j = 0
        for row in self.array:
            print(f"{j} " + str(row))
            j = j+ 1


    def populate(self, mineCount): #throw mines everywhere on that john
        # realCount = amount of mines on board
        # if mineCount != realCount, keep going
        # else stop
        realCount = 0
        while(realCount < mineCount):
            row = rng.randint(0, self.size - 1)
            col = rng.randint(0, self.size - 1)

            if self.array[row][col].val != self.BOMB_VALUE: # if the cell is not a bomb, place a mine and increment realCount
                realCount = realCount + 1
                self.array[row][col].val = self.BOMB_VALUE # place a mine.
                self.update_adjacency(row, col) #Update adjacency value of adjacent cells
                #print(f"mine {realCount} placed at {row}, {col}") # debug print statement
            
            else:
                #print(f"mine placement failed at {row}, {col}") # debug print statement
                pass

    def select(self, row, col, flag): # this function "clicks" on the mine. flag is boolean

        if flag:
            self.array[row][col].tag = 2 # set tag to flagged
        
        else:
            self.array[row][col].tag = 1 # set tag to cleared

        return self.array[row][col].val # this returns the val of the selected cell
    

        
    def getAdjacentIndices(self, matrix, row, col):
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

    def update_adjacency(self, row, col):
        '''Takes in a row and column value, increments adjacency values in valid adjacent cells'''
        for i in range(-1,2):   #Offsets for adjacent cells in row direction
            if row + i < 0 or row + i >= len(self.array):   #If offset puts the target row off either side of the board, skip this offset
                continue
            for j in range(-1,2):   #Offsets for adjacent cells in column direction
                if col + j < 0 or col + j >= len(self.array[0]):    #If offset puts the target column off either side of the board, skip this offset
                    continue
                elif i == 0 and j == 0: #If the target cell is the originating cell (offset 0,0), skip this cell
                    continue
                elif self.array[row + i][col + j].val == self.BOMB_VALUE:   #If target cell is already a bomb, skip this cell
                    continue
                else:
                    self.array[row + i][col + j].val += 1   #Otherwise, increment val in target cell

    '''
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
    '''
        
    def show_contents(self):
        '''Reveal contents of board by setting all cell tags to 1'''
        for i in range(len(self.array)):
            for j in range(len(self.array[0])):
                self.array[i][j].tag = 1






if __name__ == '__main__':
    #debug
    b = Board(10)
    b.populate(25)
    #b.select(0,1)
    b.show_contents()
    b.printArray()

