class Cell:
    def __init__(self):
        self.val = 0 # mine = -1, clear = 0, adjacency = 1-8
        self.tag = 0 # 0, 1, 2, 3 = hidden, cleared, flagged, BOOM

    def __repr__(self):
        return f"{self.val}"
    
    def __str__(self):
        return f"{self.val}"
    
    


