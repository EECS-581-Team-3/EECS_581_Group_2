from cell import *
from board import *
import os

def main():
   loop = True
   while(loop):
        
        start = input("===== Minesweeper =====\nType 'start' to begin the game\nOr 'exit' to quit\n>")

        if start.lower() == 'start':
            os.system('clear')
            size = input("How big should the board be?: ")
            mineCount = input("How many mines should there be?: ")

            b = Board(size)
            b.populate(mineCount)
            
            exit()

        elif start.lower() == 'exit':
            loop = False

        else:
            exit()

        exit()
main()