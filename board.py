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
        j = 0
        for row in self.array:
            print(f"{j} " + str(row))
            j = j+ 1


    def populate(self, mineCount, firstRow, firstCol): #throw mines everywhere on that john
        # realCount = amount of mines on board
        # if mineCount != realCount, keep going
        # else stop
        realCount = 0
        while(realCount < mineCount):
            row = rng.randint(0, self.size - 1)
            col = rng.randint(0, self.size - 1)

            if self.array[row][col].val != self.BOMB_VALUE: # if the cell is not a bomb, place a mine and increment realCount
                if not (row == firstRow and col == firstCol): # makes sure that a mine is not placed on the first selected square
                    realCount = realCount + 1
                    self.array[row][col].val = self.BOMB_VALUE # place a mine.
                    self._update_adjacency(row, col) #Update adjacency value of adjacent cells


    def select(self, row, col, flag): # this function "clicks" on the mine. flag is boolean

        if flag:
            if self.array[row][col].tag == 2:
                self.array[row][col].tag = 0 #set tag back to hidden
                return "unflag"
            elif self.array[row][col].tag == 0:
                self.array[row][col].tag = 2 # set tag to flagged
                return "flag"
        
        else:
            self._reveal(row, col)

        return None


    def _update_adjacency(self, row, col):
        '''
            Args: 
                row: integer indicating row of cell to reveal
                col: integer indicating column of cell to reveal
            Output:
                returns nothing
            Purpose:
                called by the populate function when a new bomb is placed
                iterates over adjacent cells in the row and column directions
                for each adjacent cell, checks if it is within the bounds of the board
                if so, checks if the cell contains a bomb or is the originating cell
                if the adjacent cell is within the board, does not contain a bomb, and is not the originating cell
                increments the .val member of the cell, to increment the adjacency value
        '''
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

    def _reveal(self, row, col):
        ''' Args:
                row: integer indicating row of cell to reveal
                col: integer indicating column of cell to reveal
            Output:
                returns True if cell was successfully revealed
                returns False otherwise
            Purpose:
                called when user selects to reveal, or clear, a cell
                checks cell's tag is set to 0, for 'hidden'
                if so, checks if the cell contains a bomb
                    if so, sets self.alive to False to indicate 'death'
                if cell has no adjacent bombs, calls recursive reveal function to reveal other cells
        '''
        cell = self.array[row][col] #Get the target cell
        if cell.tag == 0:   #Check that the cell is 'hidden'
            if cell.val == self.BOMB_VALUE: #Cell contains a bomb
                self.alive = False  #Set alive status to False
                cell.tag = 3    #Set cell's status to triggered
                return True     #Return a successful cell reveal
            elif cell.val == 0: #Cell has no adjacent bombs
                cell.tag = 1    #Set cell's status to revealed, or cleared
                self._rec_reveal(row, col)  #Call recursive reveal function on cell coordinates
                return True     #Return a successful cell reveal
            else:       #Cell has some adjacent bombs
                cell.tag = 1    #Set cell's status to revealed, or cleared
                return True     #Return successful cell reveal
        else:   #If the cell is not 'hidden', return False as the cell cannot be revealed
            return False
        
    def _rec_reveal(self, row, col):
        ''' Args:
                row: integer indicating row of cell to reveal
                col: integer indicating column of cell to reveal
            Output:
                returns nothing
            Purpose:
                called if a cell is cleared, that has no adjacent mines (cell.val == 0)
                for each adjacent cell, calls reveal function to reveal that cell
                    if adjacent cell has no adjacent mines, reveal will call rec_reveal again
                    this will only happen if the adjacent cells are mine free, so subsequent calls to reveal should not trigger mines
        '''
        for i in range(-1,2):   #Offsets for adjacent cells in row direction
            if row + i < 0 or row + i >= len(self.array):   #If offset puts the target row off either side of the board, skip this offset
                continue
            for j in range(-1,2):   #Offsets for adjacent cells in column direction
                if col + j < 0 or col + j >= len(self.array[0]):    #If offset puts the target column off either side of the board, skip this offset
                    continue
                else:   #Target cell is valid
                    # print(f'({row+i},{col+j})')
                    self._reveal(row + i, col + j)   #Call reveal function on target cell coordinates
        
    def _show_contents(self):
        ''' Args:
                None
            Output:
                returns nothing
            Purpose:
                For development use only
                'Reveals' contents of board by setting all cell tags to 1
                Causes printArray to print the adjacency value of each cell (cell.val)       
        '''
        for i in range(len(self.array)):
            for j in range(len(self.array[0])): 
                if self.array[i][j].tag != 3: # won't "reveal" the exploded bomb so that it remains an 'X'
                    self.array[i][j].tag = 1






if __name__ == '__main__':
    #debug
    b = Board(10)
    b.populate(10, 0, 0)
    #b.select(0,1)
    #b._show_contents()
    b.select(0,9,False)
    b.printArray()
    b.select(0,9,False)
    b.printArray()

