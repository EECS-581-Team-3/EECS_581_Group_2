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

def main(): # acts as the start menu type
    '''
    Args: 
        None
    Output: 
        None
    Purpose:
        The main menu for minesweeper providing start and exit options
        Prompting user for size of board and mineCount
        Initializes board and runs the main game loop function: 
            minesweeper(board, mineCount)

    '''
    start = input("===== Minesweeper =====\nType 'start' to begin the game\nOr 'exit' to quit\n>")

    if start.lower() == 'start': #if user types start
        os.system('clear') # just for looking nice. can be removed if causing issues
        size = int(input("How big should the board be?: ")) #size of board user input
        mineCount = int(input("How many mines should there be?: ")) #amount of mines user input

        # initialize board with user specified parameters
        b = Board(size)
        
        os.system('clear') # just for looking nice. can be removed if causing issues
        minesweeper(b, mineCount) #start game loop with user specified board size and mine count
        
        exit() #exit program

    elif start.lower() == 'exit': #if user wants to manually exit
        exit() #exit program

    else: #any other user input not specified in code
        exit() #exit program

    exit() #exit program

def victory_check(board, mineCount):
    '''
    Args: 
        board: Board object that contains matrix of cells
        mineCount: integer that represents the total number of bombs on the board
    Output:
        returns True (victory) if all the safe cells are revealed and False if not
        False means game continues
    Purpose:
        This is used to determine whether the player has won the game
        by calculating the total number of revealed safe cells and checking if it
        equals the total safe cells on the board.
        Counts safe cells by iterating through each cell and checking for tag == 1
        If all safe cells revealed True is returned and victory state
    '''

    safe_cells_discovered = 0 #amount of safe tiles the user has found
    total_safe_cells = (board.size * board.size) - mineCount

    for row in board.array: #look through each row

        for cell in row: #look through each cell

            if cell.val != board.BOMB_VALUE and cell.tag == 1:#checks to see if bomb is flagged
                safe_cells_discovered += 1 #add to revealed safe cell count

#check if revealed safe cells equals total safe cells
    return total_safe_cells == safe_cells_discovered

def minesweeper(board, mineCount): # runs the actual game
    '''
    Args:
        board: Board object containing matrix of cells
        mineCount: integer representing bombs on the board
    Output:
        returns nothing
        runs the game loop and handles the game logic
    Purpose:
        Runs the main game loop of minesweeper in the console
        Currently can be used for logic testing
        Runs all core game logic excluding the GUI, which is run
        seperately in gui.py
    '''
    firstIter = True #makes sure board is populated only after first move
    flagCount = 0 # need to add based on the amount of flags placed down
    loop = True #controls main loop for game
    while(loop):
        os.system('clear') #making sure console looks nice, can be removed
        print(f"\nMines left: {mineCount - flagCount}") #show remaining potential mines
        board.printArray() #display current board
        action = input("Flag or clear? (f/c): ") #ask user for flag or clear
        flag = False #default is to reveal unless specified for flag
        if action.lower() == 'f': #user wnats to flag
            flag = True #signal that user wants to flag

        elif action.lower() == 'c': #user wants to clear
            flag = False #signal that user wants to reveal
        
        else: #if neither option is chosen
            pass #do nothing, wait for valid input

        row = int(input("Row?: ")) #ask user the row of the cell they want to interact with
        col = int(input("Column?: ")) #ask user the column of the cell they want to interact with

        if firstIter: # this makes sure that the board is populated AFTER the first cell is selected
            firstIter = False
            board.populate(mineCount, row, col) #populates board after first move

        flagged = board.select(row, col, flag) #complete user requested action on the given cell

        if flagged == "flag": #if cell was flagged
            flagCount += 1 #add to flag count
        elif flagged == "unflag": #if cell was unflagged
            flagCount -= 1 #subtract from flag count
            
        if victory_check(board, mineCount): #check if all safe cells are revealed
            loop = False #stop the game loop
            os.system('clear') #for clean console output
            print(f"\nAll {mineCount} mines have been found") #signal all bombs have been cleared
            board.show_contents() #reveal all cells
            board.printArray() #show final board
            print("VICTORY!!!") #victory state

        if not board.alive: #check if player hit mine
            loop = False #end game
            os.system('clear') #clean console output
            print(f"\nMines left: {mineCount - flagCount}") #check how many bombs were left uncleared
            board.show_contents() #show all cells
            board.printArray() #show final board
            print("BOOOOM!!!") #defeat state
    
    again = input("Play again?(y/n)").lower() # asks the user if they wish to play again after the main loop ends

    if again == 'y':
        main()
    
        

#runs main
if __name__ == '__main__':
    main()