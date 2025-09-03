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
        b.populate(mineCount)

        os.system('clear')
        minesweeper(b, mineCount)
        
        exit()

    elif start.lower() == 'exit':
        exit()

    else:
        exit()

    exit()

def minesweeper(board, mineCount): # runs the actual game
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
            flagCount = flagCount + 1

        elif action.lower() == 'c':
            flag = False
        
        else:
            pass

        row = int(input("Row?: "))
        col = int(input("Column?: "))

        if board.select(row, col, flag) == 9:
            loop = False
            os.system('clear')
            print(f"\nMines left: {mineCount - flagCount}")
            board.printArray()
            print("BOOOOM!!!")

main()