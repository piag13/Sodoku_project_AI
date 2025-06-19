# solver.py
import time

class SolverStats:
    def __init__(self, name):
        self.name = name
        self.steps = 0
        self.time = 0
        self.solved_board = None

    def report(self):
        return f"{self.name}: Time = {self.time:.4f}s, Steps = {self.steps}"

def solve_backtracking(board):
    stats = SolverStats("Backtracking")
    start = time.time()
    solved = [row[:] for row in board]

    def is_valid(r, c, val):
        for i in range(9):
            if solved[r][i] == val or solved[i][c] == val:
                return False
        br, bc = 3 * (r // 3), 3 * (c // 3)
        for i in range(br, br + 3):
            for j in range(bc, bc + 3):
                if solved[i][j] == val:
                    return False
        return True

    def backtrack():
        for r in range(9):
            for c in range(9):
                if solved[r][c] == 0:
                    for val in range(1, 10):
                        if is_valid(r, c, val):
                            solved[r][c] = val
                            stats.steps += 1
                            if backtrack():
                                return True
                            solved[r][c] = 0
                    return False
        return True

    backtrack()
    stats.time = time.time() - start
    stats.solved_board = solved
    return stats


def solve_backtracking_mrv(board):
    stats = SolverStats("Backtracking + MRV")
    start = time.time()
    solved = [row[:] for row in board]

    def is_valid(r, c, val):
        for i in range(9):
            if solved[r][i] == val or solved[i][c] == val:
                return False
        br, bc = 3 * (r // 3), 3 * (c // 3)
        for i in range(br, br + 3):
            for j in range(bc, bc + 3):
                if solved[i][j] == val:
                    return False
        return True

    def get_mrv_cell():
        min_options = 10
        best = None
        for r in range(9):
            for c in range(9):
                if solved[r][c] == 0:
                    options = sum(is_valid(r, c, val) for val in range(1, 10))
                    if options < min_options:
                        min_options = options
                        best = (r, c)
        return best

    def backtrack():
        cell = get_mrv_cell()
        if not cell:
            return True
        r, c = cell
        for val in range(1, 10):
            if is_valid(r, c, val):
                solved[r][c] = val
                stats.steps += 1
                if backtrack():
                    return True
                solved[r][c] = 0
        return False

    backtrack()
    stats.time = time.time() - start
    stats.solved_board = solved
    return stats
