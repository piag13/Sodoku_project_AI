import tkinter as tk
from tkinter import messagebox
import numpy as np
from Backtracking import Backtracking

class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Game")
        self.cells = {}
        self.selected = None
        self.level = {
            'easy': 30, 
            'normal': 45, 
            'hard': 55, 
            'extreme': 65
        }
        self.matches = None
        self.create_board()
        self.create_buttons()

    def create_board(self):
        # Create 9x9 grid of entry widgets
        for i in range(9):
            for j in range(9):
                cell = tk.Entry(
                    self.root,
                    width=2,
                    font=('Arial', 18),
                    justify='center'
                )
                cell.grid(row=i, column=j, padx=1, pady=1)
                cell.bind('<FocusIn>', lambda e, i=i, j=j: self.cell_selected(i, j))
                cell.bind('<Key>', self.key_pressed)

                # Add thicker borders for 3x3 boxes
                if (i in [0, 3, 6] and j in range(9)):
                    cell.grid(pady=(3, 1))
                if (i in range(9) and j in [0, 3, 6]):
                    cell.grid(padx=(3, 1))

                self.cells[(i, j)] = cell

    def create_buttons(self):
        # Frame for buttons
        button_frame = tk.Frame(self.root)
        button_frame.grid(row=9, column=0, columnspan=9, pady=10)

        # New Game button
        new_game_btn = tk.Button(
            button_frame,
            text="New Game",
            command=self.new_game
        )
        new_game_btn.pack(side=tk.LEFT, padx=5)

        # Check button
        check_btn = tk.Button(
            button_frame,
            text="Check Solution",
            command=self.check_solution
        )
        check_btn.pack(side=tk.LEFT, padx=5)

        # Clear button
        clear_btn = tk.Button(
            button_frame,
            text="Clear",
            command=self.clear_board
        )
        clear_btn.pack(side=tk.LEFT, padx=5)

        # Difficulty selection
        self.difficulty_var = tk.StringVar(value="normal")
        difficulties = ["easy", "normal", "hard", "extreme"]

        for diff in difficulties:
            rb = tk.Radiobutton(
                button_frame,
                text=diff.capitalize(),
                variable=self.difficulty_var,
                value=diff
            )
            rb.pack(side=tk.LEFT, padx=5)

    def create_level(self, level_value):
        # Create initial random matches if not exists
        if self.matches is None:
            self.matches = np.random.randint(0, 10, size=(9, 9))

        hole = np.random.randint(0, 2, size=(9, 9))
        current_one = np.sum(hole)

        while current_one != (9 * 9) - level_value:
            if current_one > (9 * 9) - level_value:
                onediff = np.where(hole == 1)
                rand_index = np.random.randint(0, len(onediff[0]))
                hole[onediff[0][rand_index], onediff[1][rand_index]] = 0
                current_one = np.sum(hole)
            else:
                zerodiff = np.where(hole == 0)
                rand_index = np.random.randint(0, len(zerodiff[0]))
                hole[zerodiff[0][rand_index], zerodiff[1][rand_index]] = 1
                current_one = np.sum(hole)

        return self.matches * hole

    def cell_selected(self, i, j):
        self.selected = (i, j)

    def key_pressed(self, event):
        if self.selected:
            if event.char in '123456789':
                self.cells[self.selected].delete(0, tk.END)
                self.cells[self.selected].insert(0, event.char)
            elif event.char == '':  # Backspace
                self.cells[self.selected].delete(0, tk.END)

    def new_game(self):
        self.clear_board()
        # Get the selected difficulty level
        difficulty = self.difficulty_var.get()
        # Generate new puzzle using create_level
        puzzle = self.create_level(self.level[difficulty])

        # Fill the board with the generated puzzle
        for i in range(9):
            for j in range(9):
                value = puzzle[i][j]
                if value != 0:
                    self.cells[(i, j)].insert(0, str(int(value)))
                    self.cells[(i, j)].config(state='readonly')  # Make initial numbers readonly
                else:
                    self.cells[(i, j)].config(state='normal')

    def check_solution(self):
        # Basic check - verify if all cells are filled
        for cell in self.cells.values():
            if not cell.get():
                messagebox.showinfo("Check", "Please fill all cells!")
                return
        messagebox.showinfo("Check", "Solution checking not implemented yet")

    def clear_board(self):
        for cell in self.cells.values():
            cell.config(state='normal')  # Enable all cells first
            cell.delete(0, tk.END)


def main():
    root = tk.Tk()
    game = SudokuGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()