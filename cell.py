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
    
    


