
class Backtracking:
    def __init__(self):
        pass
    def is_safe(grid, row, col, num):
        # Check row
        for x in range(9):
            if grid[row][x] == num:
                return False

        # Check column
        for x in range(9):
            if grid[x][col] == num:
                return False

        # Check 3x3 box
        start_row = row - row % 3
        start_col = col - col % 3
        for i in range(3):
            for j in range(3):
                if grid[i + start_row][j + start_col] == num:
                    return False
        return True

    def find_empty_location(grid):
        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    return i, j
        return None

    def solve_sudoku(grid):
        # Find empty location
        empty = find_empty_location(grid)

        # If no empty location, puzzle is solved
        if not empty:
            return True

        row, col = empty

        # Try digits 1 to 9
        for num in range(1, 10):
            # Check if it's safe to place number
            if is_safe(grid, row, col, num):
                # Make tentative assignment
                grid[row][col] = num

                # Return if success
                if solve_sudoku(grid):
                    return True

                # Failure, unmake & try again
                grid[row][col] = 0

        # Trigger backtracking
        return False

    def print_grid(grid):
        for i in range(9):
            for j in range(9):
                print(grid[i][j], end=" ")
            print()