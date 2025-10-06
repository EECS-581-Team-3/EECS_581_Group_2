"""
File: ai_solver.py

Purpose:
    Provide a rule-based Minesweeper AI/bot that selects next action from current board state.
    Three difficultly tiers: 
    EASY - reveal and random hidden cell
    MEDIUM - follows logic:
               if (clue - flagged) == |hidden|, flag all hidden
               if (clue - flagged) == 0, reveal all hidden
               else guess.
    HARD - runs MEDIUM logic, then check for 1-2-1 horizontal/vertical patterns
           if found, infer flags/reveals around the pattern, else guess

Inputs:
    AISolver(board, difficulty="MEDIUM")
    Requires board: size, array[Cell(val, tag)], select(r,c,flag), and BOMB_VALUE

Outputs:
  nextMove() -> (row, col, "flag"|"reveal"|"random") | None

Errors:
    - Assumes the Board interface is valid
    - Random reveals may hit a mine

Author(s): Jenny Tsotezo, Genea Dinnall, Sam Kelemen, Megan Taggart
Created Date: 2025-10-03
"""


import random

# define modes as strings for ease of use
EASY = "EASY"
MEDIUM = "MEDIUM"
HARD = "HARD"

# creates AI solver class for use, takes in difficulty and board. 
class AISolver:
    # Auto difficulty is medium on initialization
    def __init__(self, board, difficulty=MEDIUM):
        self.board = board
        self.size = board.size
        self.difficulty = difficulty

    # move determined by difficulty selection, easy is random.
    def nextMove(self):
        # easy mode randomly selects move without considering neighbor count
        if self.difficulty == EASY:
            return self._random_reveal()
        # uses medium rules helper function to determine next rule
        move = self._apply_medium_rules()
        # returns move if it exists
        if move:
            return move
        # does 1-2-1 pattern inference if hard mode selected
        if self.difficulty == HARD:
            move = self._apply_121_rules()
            if move:
                return move
        # random reveal is no deterministic move is found 
        return self._random_reveal()
    # picks a random cell and reveals based on size of board
    def _random_reveal(self):
        hidden = [(r, c)
                  for r in range(self.size)
                  for c in range(self.size)
                  if self.board.array[r][c].tag == 0]
        # ensures that cell is not already revealed
        if not hidden:
            return None
        r, c = random.choice(hidden)
        self.board.select(r, c, flag=False)
        return (r, c, "random")
    # flags when bombs are suspected and reveals if there are flagged neighbors
    def _apply_medium_rules(self):
        for r in range(self.size):
            for c in range(self.size):
                cell = self.board.array[r][c]
                if cell.tag != 1:  
                    continue
                if cell.val == 0 or cell.val == self.board.BOMB_VALUE:
                    continue

                hidden_neighbors, flagged_neighbors = self._neighbor_partition(r, c)

                if cell.val == len(hidden_neighbors) and hidden_neighbors:
                    rr, cc = hidden_neighbors[0]
                    self.board.select(rr, cc, flag=True)
                    return (rr, cc, "flag")

                if cell.val == flagged_neighbors and hidden_neighbors:
                    rr, cc = hidden_neighbors[0]
                    self.board.select(rr, cc, flag=False)
                    return (rr, cc, "reveal")

        return None
    # looks for horizontal or vertical 1-2-1 triplets of revealed cells
    # attempts inference to identify safe reveals or flags
    def _apply_121_rules(self):
        # scans horizontally
        for r in range(self.size):
            for c in range(self.size - 2):
                triplet = [self.board.array[r][c + k] for k in range(3)]
                if all(t.tag == 1 for t in triplet) and [triplet[0].val, triplet[1].val, triplet[2].val] == [1, 2, 1]:
                    move = self._apply_121_inference_line(r, c, horizontal=True)
                    if move:
                        return move
        # scans vertically
        for c in range(self.size):
            for r in range(self.size - 2):
                triplet = [self.board.array[r + k][c] for k in range(3)]
                if all(t.tag == 1 for t in triplet) and [triplet[0].val, triplet[1].val, triplet[2].val] == [1, 2, 1]:
                    move = self._apply_121_inference_line(r, c, horizontal=False)
                    if move:
                        return move

        return None
    # generator that yeilds coordinates of the surrounding neighbors
    def _neighbors(self, r, c):
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                rr, cc = r + dr, c + dc
                if 0 <= rr < self.size and 0 <= cc < self.size:
                    yield rr, cc
    # partitions neighbors into hidden or flagged for a given cell
    def _neighbor_partition(self, r, c):
        hidden = []
        flagged = 0
        for rr, cc in self._neighbors(r, c):
            t = self.board.array[rr][cc].tag
            if t == 0:
                hidden.append((rr, cc))
            elif t == 2:
                flagged += 1
        return hidden, flagged
    # starting at cell attempts to infer flags and safe reveals using surrounding cells
    def _apply_121_inference_line(self, r, c, horizontal=True):
        if horizontal:
            mid = (r, c + 1)
            # band covers the row above and row below 3-triplet columns
            band = [(r - 1, c), (r - 1, c + 1), (r - 1, c + 2),
                    (r + 1, c), (r + 1, c + 1), (r + 1, c + 2)]
        else:
            mid = (r + 1, c)
            # band covers the column left and right of the 3-triplet rows
            band = [(r, c - 1), (r + 1, c - 1), (r + 2, c - 1),
                    (r, c + 1), (r + 1, c + 1), (r + 2, c + 1)]
        # prefer to conservatively flag any hidden cell 
        for rr, cc in band:
            if 0 <= rr < self.size and 0 <= cc < self.size:
                if self.board.array[rr][cc].tag == 0:
                    self.board.select(rr, cc, flag=True)
                    return (rr, cc, "flag")
        # if no band hidden cells are found, reveals neighbor of the middle
        for rr, cc in self._neighbors(*mid):
            if self.board.array[rr][cc].tag == 0:
                self.board.select(rr, cc, flag=False)
                return (rr, cc, "reveal")

        return None
