import tkinter as tk
from tkinter import ttk, messagebox
from board import Board

class MinesweeperGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Minesweeper")
        
        self.board = None
        self.buttons = []
        self.game_started = False
        self.board_size = 10
        self.mine_count = 10

        self.flag_count = 0

        self.number_colors = {
            1: '#0000FF',  # Blue
            2: '#008000',  # Green
            3: '#FF0000',  # Red
            4: '#800080',  # Purple
            5: '#800000',  # Maroon
            6: '#008080',  # Teal
            7: '#000000',  # Black
            8: '#808080'   # Gray
        }

        self.setup_ui()
        self.new_game()
    
    def setup_ui(self):
        self.create_menu_bar()

        self.game_frame = ttk.Frame(self.root)
        self.game_frame.pack(pady=(0, 10))

        self.status_frame = ttk.Frame(self.root)
        self.status_frame.pack(pady=(0, 10))
        
        self.status_label = ttk.Label(self.status_frame, text="Click any cell to start!")
        self.status_label.pack()
    
    def create_menu_bar(self):
        menu_frame = ttk.Frame(self.root)
        menu_frame.pack(fill=tk.X, padx=10, pady=10)

        new_game_btn = ttk.Button(menu_frame, text="New Game", command=self.new_game)
        new_game_btn.pack(side=tk.LEFT, padx=(0, 10))

        ttk.Label(menu_frame, text="Set difficulty:").pack(side=tk.LEFT, padx=(10, 5))

        custom_btn = ttk.Button(menu_frame, text="Custom", command=self.custom_difficulty)
        custom_btn.pack(side=tk.LEFT, padx=2)
    
    def set_difficulty(self, size, mines):
        self.board_size = size
        self.mine_count = mines
        self.new_game()
    
    def custom_difficulty(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Custom Difficulty")
        dialog.geometry("400x250")
        dialog.transient(self.root)
        dialog.grab_set()

        dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))
        
        ttk.Label(dialog, text="Board Size:").pack(pady=5)
        size_var = tk.StringVar(value=str(self.board_size))
        size_entry = ttk.Entry(dialog, textvariable=size_var, width=10)
        size_entry.pack(pady=5)
        
        ttk.Label(dialog, text="Number of Mines:").pack(pady=5)
        mines_var = tk.StringVar(value=str(self.mine_count))
        mines_entry = ttk.Entry(dialog, textvariable=mines_var, width=10)
        mines_entry.pack(pady=5)

        def apply_custom():
            try:
                size = int(size_var.get())
                mines = int(mines_var.get())
                if size < 4 or size > 20:
                    raise ValueError("Size must be between 4 and 20")
                if mines < 1 or mines >= size * size:
                    raise ValueError("Mines must be between 1 and size²-1")
            
                self.board_size = size
                self.mine_count = mines
                dialog.destroy()
                self.new_game()
            except ValueError as e:
                messagebox.showerror("Invalid Input", str(e))
        
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Apply", command=apply_custom).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def new_game(self):
        for widget in self.game_frame.winfo_children():
            widget.destroy()
        
        self.game_started = False
        self.flag_count = 0
        self.board = Board(self.board_size)
        self.buttons = []

        self.create_game_grid()

        self.status_label.config(text=f"New game started!")

        self.root.update_idletasks()
        self.root.geometry("")
    
    def create_game_grid(self):
        self.buttons = []

        for i in range(self.board_size):
            button_row = []
            for j in range(self.board_size):
                btn = tk.Button(
                    self.game_frame,
                    text="",
                    width=3,
                    height=1,
                    font=('Arial', 10, 'bold'),
                    command=lambda r=i, c=j: self.left_click(r, c)
                )
                btn.bind("<Button-3>", lambda e, r=i, c=j: self.right_click(r, c)) 
                btn.grid(row=i, column=j, padx=1, pady=1)
                button_row.append(btn)
            self.buttons.append(button_row)
        
    def left_click(self, row, col):
        if not self.board.alive:
            return
        
        if not self.game_started:
            self.board.populate(self.mine_count, row, col)
            self.game_started = True

        result = self.board.select(row, col, flag=False)

        self.update_display()

        if not self.board.alive:
            self.game_over()
        elif self.check_win():
            self.game_won()
    
    def right_click(self, row, col):
        if not self.board.alive or not self.game_started:
            return

        result = self.board.select(row, col, flag=True)
        if result == 'flag':
            self.flag_count += 1
        elif result == 'unflag':
            self.flag_count -= 1

        self.update_display()
    
    def update_display(self):
        for i in range(self.board_size):
            for j in range(self.board_size):
                cell = self.board.array[i][j]
                btn = self.buttons[i][j]

                if cell.tag == 0: # hidden
                    btn.config(text="", bg='#f0f0f0', relief='raised')
                elif cell.tag == 1: # revealed
                    if cell.val == 0:
                        btn.config(text="", bg='lightgray', relief='sunken')
                    else:
                        color = self.number_colors.get(cell.val, 'black')
                        btn.config(text=str(cell.val), bg='lightgray', relief='sunken', fg=color)
                elif cell.tag == 2: # flagged
                    btn.config(text="🚩", bg='yellow', relief='raised')
                elif cell.tag == 3: # exploded bomb
                    btn.config(text="💣", bg='red', relief='sunken')

        self.status_label.config(text=f"{self.mine_count - self.flag_count} mines remaining!")
    
    def game_over(self):
        # reveal all bombs
        for i in range(self.board_size):
            for j in range(self.board_size):
                cell = self.board.array[i][j]
                if cell.val == self.board.BOMB_VALUE and cell.tag != 3:
                    btn = self.buttons[i][j]
                    btn.config(text="💣", bg='lightcoral', relief='sunken')
        
        self.status_label.config(text="Game over! You hit a mine!")
        messagebox.showinfo("Game over! You hit a mine!")
    
    def check_win(self):
        for i in range(self.board_size):
            for j in range(self.board_size):
                cell = self.board.array[i][j]
                if cell.val != self.board.BOMB_VALUE and (cell.tag == 0 or cell.tag == 2):
                    return False
        return True

    def game_won(self):
        # flag all remaining bombs
        for i in range(self.board_size):
            for j in range(self.board_size):
                cell = self.board.array[i][j]
                if cell.val == self.board.BOMB_VALUE:
                    cell.tag = 2
                    self.buttons[i][j].config(text="🚩", bg='lightgreen', relief='raised')
        
        self.status_label.config(text="Congratulations, you won!")
        messagebox.showinfo("Congratulations, you won!")

def main():
    root = tk.Tk()
    game = MinesweeperGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()