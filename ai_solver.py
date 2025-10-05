import random

EASY = "EASY"
MEDIUM = "MEDIUM"
HARD = "HARD"

class AISolver:
    def __init__(self, board, difficulty=MEDIUM):
        self.board = board
        self.size = board.size
        self.difficulty = difficulty

    def nextMove(self):
        if self.difficulty == EASY:
            return self._random_reveal()

        move = self._apply_medium_rules()
        if move:
            return move

        if self.difficulty == HARD:
            move = self._apply_121_rules()
            if move:
                return move

        return self._random_reveal()

    def _random_reveal(self):
        hidden = [(r, c)
                  for r in range(self.size)
                  for c in range(self.size)
                  if self.board.array[r][c].tag == 0]
        if not hidden:
            return None
        r, c = random.choice(hidden)
        self.board.select(r, c, flag=False)
        return (r, c, "random")

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

    def _apply_121_rules(self):
        for r in range(self.size):
            for c in range(self.size - 2):
                triplet = [self.board.array[r][c + k] for k in range(3)]
                if all(t.tag == 1 for t in triplet) and [triplet[0].val, triplet[1].val, triplet[2].val] == [1, 2, 1]:
                    move = self._apply_121_inference_line(r, c, horizontal=True)
                    if move:
                        return move

        for c in range(self.size):
            for r in range(self.size - 2):
                triplet = [self.board.array[r + k][c] for k in range(3)]
                if all(t.tag == 1 for t in triplet) and [triplet[0].val, triplet[1].val, triplet[2].val] == [1, 2, 1]:
                    move = self._apply_121_inference_line(r, c, horizontal=False)
                    if move:
                        return move

        return None

    def _neighbors(self, r, c):
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                rr, cc = r + dr, c + dc
                if 0 <= rr < self.size and 0 <= cc < self.size:
                    yield rr, cc

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

    def _apply_121_inference_line(self, r, c, horizontal=True):
        if horizontal:
            mid = (r, c + 1)
            band = [(r - 1, c), (r - 1, c + 1), (r - 1, c + 2),
                    (r + 1, c), (r + 1, c + 1), (r + 1, c + 2)]
        else:
            mid = (r + 1, c)
            band = [(r, c - 1), (r + 1, c - 1), (r + 2, c - 1),
                    (r, c + 1), (r + 1, c + 1), (r + 2, c + 1)]

        for rr, cc in band:
            if 0 <= rr < self.size and 0 <= cc < self.size:
                if self.board.array[rr][cc].tag == 0:
                    self.board.select(rr, cc, flag=True)
                    return (rr, cc, "flag")

        for rr, cc in self._neighbors(*mid):
            if self.board.array[rr][cc].tag == 0:
                self.board.select(rr, cc, flag=False)
                return (rr, cc, "reveal")

        return None