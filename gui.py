'''
Module Name: MinesweeperGUI class
Purpose: serves as graphical interface for the minesweeper game
         controls graphical display, processes user input, checks for end status
Input(s): None
Output(s): None
Author(s): Jamie King
           Jacob Kice
Outside Source(s):  None
Creation Date: 09/17/2025
Updated Date: 09/21/2025
'''

import tkinter as tk
from tkinter import ttk, messagebox
from board import Board
from ai_solver import AISolver

EASY = "EASY"
MEDIUM = "MEDIUM"
HARD = "HARD"


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
        self.ai_mode = tk.StringVar(value="OFF")     
        self.ai_solver = None
        self.ai_auto = False                         
        self.current_turn = "HUMAN"                  
        self.multiplayer = tk.BooleanVar(value=False)
        self.current_player = 1 

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
        """
            Args:
                None
            Output:
                None
            Purpose:
                Initialize the main UI components.
        """
        self.create_menu_bar()

        self.game_frame = ttk.Frame(self.root)
        self.game_frame.pack(pady=(0, 10))

        self.status_frame = ttk.Frame(self.root)
        self.status_frame.pack(pady=(0, 10))
        
        self.status_label = ttk.Label(self.status_frame, text="Click any cell to start!")
        self.status_label.pack()
    
    def create_menu_bar(self):
        """
            Args:
                None
            Output:
                None
            Purpose:
                Create the top menu bar with game controls.
        """
        menu_frame = ttk.Frame(self.root)
        menu_frame.pack(fill=tk.X, padx=10, pady=10)

        new_game_btn = ttk.Button(menu_frame, text="New Game", command=self.new_game)
        new_game_btn.pack(side=tk.LEFT, padx=(0, 10))

        ttk.Label(menu_frame, text="Set difficulty:").pack(side=tk.LEFT, padx=(10, 5))
        ttk.Button(menu_frame, text="Custom", command=self.custom_difficulty).pack(side=tk.LEFT, padx=2)

        custom_btn = ttk.Button(menu_frame, text="Custom", command=self.custom_difficulty)
        custom_btn.pack(side=tk.LEFT, padx=2)

        ttk.Label(menu_frame, text="AI:").pack(side=tk.LEFT, padx=(15, 5))
        ai_combo = ttk.Combobox(menu_frame, width=10, state="readonly",
                                values=["OFF", "EASY", "MEDIUM", "HARD"],
                                textvariable=self.ai_mode)
        ai_combo.pack(side=tk.LEFT, padx=2)

        self.ai_mode.trace_add("write", lambda *a: self._on_ai_mode_change())
        ttk.Button(menu_frame, text="AI Step", command=self.ai_next_move).pack(side=tk.LEFT, padx=6)
        ttk.Button(menu_frame, text="AI Auto", command=self.ai_toggle_auto).pack(side=tk.LEFT, padx=2)

        ttk.Checkbutton(menu_frame, text="Multiplayer", variable=self.multiplayer,
                        command=self._on_multiplayer_toggle).pack(side=tk.LEFT, padx=(15, 0))
    
    def set_difficulty(self, size, mines):
        '''
            Args:
                size: integer indicating N value of NxN board
                mines: integer indicating number of mines
            Output:
                None
            Purpose:
                Updates game parameters
                Calls new_game function to reset game state
        '''
        self.board_size = size
        self.mine_count = mines
        self.new_game()
    
    def custom_difficulty(self):
        """
            Args:
                None
            Output:
                None
            Purpose:
                Open dialog for custom board size and mine count configuration.
        """
        dialog = tk.Toplevel(self.root)
        dialog.title("Custom Difficulty")
        dialog.geometry("400x250")
        dialog.transient(self.root)
        dialog.grab_set()

        # Center dialog relative to main window
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
            """
                Args:
                    None
                Output:
                    None
                Purpose:
                    Validate and apply custom difficulty settings.
            """
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
        """
            Args:
                None
            Output:
                None
            Purpose:
                Initialize a new game with current difficulty settings.
        """
        # Clear existing UI elements
        for widget in self.game_frame.winfo_children():
            widget.destroy()
        
        self.game_started = False
        self.flag_count = 0
        self.board = Board(self.board_size)
        self.buttons = []

        self.current_turn = "HUMAN"
        self.current_player = 1
        self.ai_auto = False 
        self._rebuild_ai_solver()

        self.create_game_grid()
        self._update_status()

        # Auto-resize window to fit content
        self.root.update_idletasks()
        self.root.geometry("")
    
    def create_game_grid(self):
        """
            Args:
                None
            Output:
                None
            Purpose:
                Create the game grid with row/column labels and interactive buttons.
        """
        self.buttons = []

        for j in range(self.board_size):
            col_label = tk.Label(
                self.game_frame,
                text=str(j + 1),
                font=('Arial', 8, 'bold'),
                width=3,
                height=1,
                bg='lightblue',
                relief='raised'
            )
            col_label.grid(row=0, column=j + 1, padx=1, pady=1)

        for i in range(self.board_size):
            row_label = tk.Label(
                self.game_frame,
                text=chr(65 + i),  # A=65, B=66, etc.
                font=('Arial', 8, 'bold'),
                width=3,
                height=1,
                bg='lightblue',
                relief='raised'
            )
            row_label.grid(row=i + 1, column=0, padx=1, pady=1)
            
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
                btn.grid(row=i + 1, column=j + 1, padx=1, pady=1)
                button_row.append(btn)
            self.buttons.append(button_row)
        
    def left_click(self, row, col):
        """
            Args:
                row: integer indicating the row value of the cell that was clicked
                col: integer indicating the column value of the cell that was clicked
            Output:
                None
            Purpose:
                Handle left mouse clicks on game cells.
        """
        if not self.board.alive:
            return
        
        # Initialize board on first click to avoid starting on a mine
        if not self.game_started:
            self.board.populate(self.mine_count, row, col)
            self.game_started = True

        result = self.board.select(row, col, flag=False)
        self.update_display()

        # Check for game end conditions
        if not self.board.alive:
            self.game_over()
        elif self.check_win():
            self.game_won()
        self._advance_turns()
    
    def right_click(self, row, col):
        """
            Args:
                row: integer indicating the row of the cell that was clicked
                col: integer indicating the column of the cell that was clicked
            Output:
                None
            Purpose:
                Handle right mouse clicks for flag placement/removal.
        """
        if not self.board.alive or not self.game_started:
            return

        result = self.board.select(row, col, flag=True)
        
        # Update flag counter based on action
        if result == 'flag':
            self.flag_count += 1
        elif result == 'unflag':
            self.flag_count -= 1

        self.update_display()
        self._advance_turns()

    def _rebuild_ai_solver(self):
        mode = self.ai_mode.get()
        if mode == "OFF":
            self.ai_solver = None
            return

        MODE_MAP = {"EASY": EASY, "MEDIUM" : MEDIUM, "HARD" : HARD}
        diff = MODE_MAP.get(self.ai_mode.get())
        if diff is None:
            self.ai_solver = None
            return
        existing = getattr(self, "ai_solver", None)
        if isinstance(existing, AISolver) and existing.difficulty == diff and existing.board is self.board:
            return
        self.ai_solver = AISolver(self.board, difficulty=diff)

    def _on_ai_mode_change(self):
        self._rebuild_ai_solver()
        self.current_turn = "HUMAN"
        self._update_status()

    def ai_next_move(self):
        if not self.board.alive or self.ai_solver is None:
            return

        if not self.game_started:
            r = self.board_size // 2
            c = self.board_size // 2
            self.board.populate(self.mine_count, r, c)
            self.game_started = True

        move = self.ai_solver.nextMove()
        self.flag_count = sum(1 for i in range(self.board.size) for j in range(self.board.size) if self.board.array[i][j].tag == 2)
        self.update_display()
        self._update_status()

        if move is None:
            self.current_turn = "HUMAN"
            return

        if not self.board.alive:
            self.game_over()
            return
        if self.check_win():
            self.game_won()
            return

        if not self.multiplayer.get():
            self.current_turn = "HUMAN"
            self._update_status()

    def ai_toggle_auto(self):
        if self.ai_solver is None:
            return
        self.ai_auto = not self.ai_auto
        if self.ai_auto:
            self._ai_tick()

    def _ai_tick(self):
        if not self.ai_auto or not self.board.alive or self.ai_solver is None:
            return
        if not self.multiplayer.get():
            self.current_turn = "AI"

        self.ai_next_move()

        if self.ai_auto and self.board.alive and not self.check_win():
            self.root.after(150, self._ai_tick)

    def _advance_turns(self):
        if self.multiplayer.get():
            self.current_player = 2 if self.current_player == 1 else 1
            self._update_status()
            return

        if self.ai_solver is None:
            self._update_status()
            return

        self.current_turn = "AI"
        self._update_status()

        if self.ai_auto:
            self._ai_tick()

    def _on_multiplayer_toggle(self):
        if self.multiplayer.get():
            self.current_player = 1
            self.current_turn = "HUMAN"
        else:
            self.current_turn = "HUMAN"
        self._update_status()
    
    def update_display(self):
        """
            Args:
                None
            Output:
                None
            Purpose:
                Refresh the visual state of all game buttons based on board state.
        """
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

    def _update_status(self):
        mines_remaining = self.mine_count - self.flag_count
        if self.multiplayer.get():
            self.status_label.config(text=f"{mines_remaining} mines remaining | Player {self.current_player}'s turn")
        else:
            who = self.ai_mode.get() if self.ai_solver else "No AI"
            turn = self.current_turn if self.ai_solver else "HUMAN"
            self.status_label.config(text=f"{mines_remaining} mines remaining | AI: {who} | Turn: {turn}")
    
    def game_over(self):
        """
            Args:
                None
            Output:
                None
            Purpose:
                Handle game over state by revealing all mines.
        """
        # Reveal all unflagged bombs
        for i in range(self.board_size):
            for j in range(self.board_size):
                cell = self.board.array[i][j]
                if cell.val == self.board.BOMB_VALUE and cell.tag != 3:
                    btn = self.buttons[i][j]
                    btn.config(text="💣", bg='lightcoral', relief='sunken')
        
        if self.multiplayer.get():
            loser = self.current_player
            winner = 2 if loser == 1 else 1
            self.status_label.config(text=f"Game over! Player {loser} hit a mine. Player {winner} wins!")
            messagebox.showinfo("Game Over", f"Player {loser} hit a mine. Player {winner} wins!")
        else:
            self.status_label.config(text="Game over! You hit a mine!")
            messagebox.showinfo("Game Over", "You hit a mine!")
    
    def check_win(self):
        """
            Args:
                None
            Output:
                returns False if the game has not yet been won
                returns True otherwise
            Purpose:
                Check if player has won by revealing all non-mine cells.
        """
        for i in range(self.board_size):
            for j in range(self.board_size):
                cell = self.board.array[i][j]
                # Win condition: all non-mine cells must be revealed
                if cell.val != self.board.BOMB_VALUE and (cell.tag == 0 or cell.tag == 2):
                    return False
        return True

    def game_won(self):
        """
            Args:
                None
            Output:
                None
            Purpose:
                Handle win condition by auto-flagging remaining mines.
        """
        for i in range(self.board_size):
            for j in range(self.board_size):
                cell = self.board.array[i][j]
                if cell.val == self.board.BOMB_VALUE:
                    cell.tag = 2
                    self.buttons[i][j].config(text="🚩", bg='lightgreen', relief='raised')
        
        if self.multiplayer.get():
            self.status_label.config(text="All mines cleared — Tie!")
            messagebox.showinfo("Victory", "All mines cleared — Tie!")
        else:
            self.status_label.config(text="Congratulations, you won!")
            messagebox.showinfo("Victory", "Congratulations, you won!")

def main():
    root = tk.Tk()
    game = MinesweeperGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()