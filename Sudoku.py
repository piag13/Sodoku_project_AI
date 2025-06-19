import numpy as np
import time

class Sudoku:
    def __init__(self, N):
        self.N = N
        self.SRN = int(np.sqrt(N))
        self.answer_board = np.zeros((9, 9), dtype=int)

        self.fill_diagonal()
        while not self.fill_remaining(0, 0):
            self.answer_board = np.zeros((9, 9), dtype=int)
            self.fill_diagonal()

        self.solution_board = np.copy(self.answer_board)
        self.question_board = np.copy(self.solution_board)

    def fill_diagonal(self):
        for i in range(0, self.N, self.SRN):
            self.fill_cell(i, i)

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

    def fill_remaining(self, row, col):
        if row == self.N - 1 and col == self.N:
            return True
        if col == self.N:
            row += 1
            col = 0
        if self.answer_board[row][col] != 0:
            return self.fill_remaining(row, col + 1)
        for num in range(1, self.N + 1):
            if self.safe_position(row, col, num):
                self.answer_board[row][col] = num
                if self.fill_remaining(row, col + 1):
                    return True
                self.answer_board[row][col] = 0
        return False

    def remove_digits(self, level):
        self.question_board = np.copy(self.solution_board)

        count = level
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
        return self.solution_board

    def print(self):
        print("Question:")
        print(self.question_board)
        print("\nSolution:")
        print(self.solution_board)

    # Backtracking solver
    def solve_backtracking(self):
        board = np.copy(self.question_board)
        self.loop_count = 0
        start = time.time()
        self._backtracking(board)
        end = time.time()
        return board, end - start, self.loop_count

    def _backtracking(self, board):
        self.loop_count += 1
        for i in range(self.N):
            for j in range(self.N):
                if board[i][j] == 0:
                    for num in range(1, self.N + 1):
                        if self._is_safe(board, i, j, num):
                            board[i][j] = num
                            if self._backtracking(board):
                                return True
                            board[i][j] = 0
                    return False
        return True

    # MRV solver
    def solve_mrv(self):
        board = np.copy(self.question_board)
        self.loop_count = 0
        start = time.time()
        self._mrv_solver(board)
        end = time.time()
        return board, end - start, self.loop_count

    def _mrv_solver(self, board):
        self.loop_count += 1
        empty = self._find_mrv_cell(board)
        if not empty:
            return True
        row, col = empty
        for num in range(1, self.N + 1):
            if self._is_safe(board, row, col, num):
                board[row][col] = num
                if self._mrv_solver(board):
                    return True
                board[row][col] = 0
        return False

    def _find_mrv_cell(self, board):
        min_candidates = 10
        best_cell = None
        for i in range(self.N):
            for j in range(self.N):
                if board[i][j] == 0:
                    candidates = [n for n in range(1, 10) if self._is_safe(board, i, j, n)]
                    if len(candidates) < min_candidates:
                        min_candidates = len(candidates)
                        best_cell = (i, j)
        return best_cell

    def _is_safe(self, board, row, col, num):
        block_row, block_col = row - row % self.SRN, col - col % self.SRN
        return (num not in board[row] and
                num not in board[:, col] and
                num not in board[block_row:block_row + self.SRN, block_col:block_col + self.SRN])
