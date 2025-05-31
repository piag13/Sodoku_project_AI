import numpy as np

class Sudoku:
    def __init__(self, N, level):
        self.N = N
        self.level = level
        self.SRN = int(np.sqrt(N))
        self.answer_board = np.zeros((9, 9), dtype=int)
        self.question_board = None
        self._generate_board()

    def _generate_board(self):
        self.fill_diagonal()
        self.fill_remaining_with_heuristic()
        self.remove_digits()

    def fill_diagonal(self):
        for i in range(0, self.N, self.SRN):
            self.fill_cell(i, i)

    def find_mrv(self):
        min_options = 10
        best_cell = None
        for i in range(self.N):
            for j in range(self.N):
                if self.answer_board[i][j] == 0:
                    options = 0
                    for k in range(1, self.N + 1):
                        if self.safe_position(i, j, k):
                            options += 1
                    if options < min_options:
                        min_options = options
                        best_cell = (i, j)
        return best_cell

    def not_in_group(self, rowstart, colstart, num):
        for i in range(self.SRN):
            for j in range(self.SRN):
                if self.answer_board[rowstart + i][colstart + j] == num:
                    return False
        return True

    def fill_cell(self, row, col):
        num = np.random.permutation(range(1, self.N + 1))
        k = 0
        for i in range(self.SRN):
            for j in range(self.SRN):
                self.answer_board[row + i][col + j] = num[k]
                k += 1

    def safe_position(self, row, col, num):
        return (self.not_in_row(row, num) and
                self.not_in_col(col, num) and
                self.not_in_group(row - row % self.SRN, col - col % self.SRN, num))

    def fill_remaining_with_heuristic(self):
        cell = self.find_mrv()
        if not cell:
            return True  # no empty cell left
        row, col = cell

        for num in range(1, self.N + 1):
            if self.safe_position(row, col, num):
                self.answer_board[row][col] = num
                if self.fill_remaining_with_heuristic():
                    return True
                self.answer_board[row][col] = 0
        return False

    def remove_digits(self):
        self.question_board = self.answer_board.copy()
        count = self.level
        while count > 0:
            row = np.random.randint(0, self.N)
            col = np.random.randint(0, self.N)
            if self.question_board[row][col] != 0:
                self.question_board[row][col] = 0
                count -= 1

    def not_in_row(self, row, num):
        return num not in self.answer_board[row, :]

    def not_in_col(self, col, num):
        return num not in self.answer_board[:, col]

    def get_puzzle(self):
        return self.question_board

    def get_solution(self):
        return self.answer_board

    def print(self):
        print("Question:")
        print(self.question_board)
        print("\nSolution:")
        print(self.answer_board)


import time

if __name__ == "__main__":
    puzzle = Sudoku(9, 70)
    puzzle.print()

    print("\nSolving...")
    start_time = time.time()

    puzzle.fill_remaining_with_heuristic()

    end_time = time.time()
    elapsed_time = end_time - start_time

    puzzle.print()
    print(f"\n⏱️ Time to solve: {elapsed_time:.15f} seconds")
