'''
Module Name: Cell class
Purpose: serves as a grid cell for the minesweeper game
         stores cell information of mine/adjacency value and current cell status
Input(s): None
Output(s): None
Author(s): Gunther Luechtefeld
Outside Source(s):  None
Creation Date: 09/02/2025
Updated Date: 09/03/2025
'''

class Cell:
    def __init__(self):
        self.val = 0 # mine = 9, clear = 0, adjacency = 1-8
        self.tag = 0 # 0, 1, 2, 3 = hidden, cleared, flagged, BOOM

    def __repr__(self):
        if self.tag == 0: # if hidden
            return "H"
        
        elif self.tag == 1: # if cleared
            return f"{self.val}"
        
        elif self.tag == 2: # if flagged
            return "F"
        
        elif self.tag == 3: # a bom
            return "X"
    
    def __str__(self):
        return f"{self.val}"
    
    


