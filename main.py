'''
Module Name: Main module (terminal interface)
Purpose: serves as terminal interface for the minesweeper game
         controls terminal display, processes user input, checks for end status
Input(s): None
Output(s): None
Author(s): Gunther Luechtefeld
           Srihari Meyoor
Outside Source(s):  None
Creation Date: 09/02/2025
Updated Date: 09/08/2025
'''

from cell import *
from board import *
import os

def main(): # acts as the start menu type shit

    start = input("===== Minesweeper =====\nType 'start' to begin the game\nOr 'exit' to quit\n>")

    if start.lower() == 'start':
        os.system('clear') # just for looking nice. can be removed if causing issues
        size = int(input("How big should the board be?: "))
        mineCount = int(input("How many mines should there be?: "))

        # initialize board with user specified parameters
        b = Board(size)
        
        os.system('clear')
        minesweeper(b, mineCount)
        
        exit()

    elif start.lower() == 'exit':
        exit()

    else:
        exit()

    exit()

def victory_check(board, mineCount):
        safe_cells_discovered = 0 #amount of safe tiles the user has found
        total_safe_cells = (board.size * board.size) - mineCount

        for row in board.array: #look through each row

            for cell in row: #look through each cell

                if cell.val != board.BOMB_VALUE and cell.tag == 1:#checks to see if bomb is flagged
                    safe_cells_discovered += 1

        return total_safe_cells == safe_cells_discovered

def minesweeper(board, mineCount): # runs the actual game
    firstIter = True
    flagCount = 0 # need to add based on the amount of flags placed down
    loop = True
    while(loop):
        os.system('clear')
        print(f"\nMines left: {mineCount - flagCount}")
        board.printArray()
        action = input("Flag or clear? (f/c): ")
        flag = False
        if action.lower() == 'f':
            flag = True

        elif action.lower() == 'c':
            flag = False
        
        else:
            pass

        row = int(input("Row?: "))
        col = int(input("Column?: "))

        if firstIter: # this makes sure that the board is populated AFTER the first cell is selected
            firstIter = False
            board.populate(mineCount, row, col)

        flagged = board.select(row, col, flag)

        if flagged == "flag":
            flagCount += 1
        elif flagged == "unflag":
            flagCount -= 1
            
        if victory_check(board, mineCount):
            loop = False
            os.system('clear')
            print(f"\nAll {mineCount} mines have been found")
            board.show_contents()
            board.printArray()
            print("VICTORY!!!")

        if not board.alive:
            loop = False
            os.system('clear')
            print(f"\nMines left: {mineCount - flagCount}")
            board.show_contents()
            board.printArray()
            print("BOOOOM!!!")
    
    again = input("Play again?(y/n)").lower() # asks the user if they wish to play again after the main loop ends

    if again == 'y':
        main()
    
        


main()