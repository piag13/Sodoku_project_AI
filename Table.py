import pygame
from Cell import Cell
from Sudoku import Sudoku
from setting import WIDTH, HEIGHT, N_CELLS, CELL_SIZE
import numpy as np
from Solve import solve_backtracking, solve_backtracking_mrv

pygame.font.init()

class Table:
    def __init__(self, screen, difficulty='medium'):
        self.screen = screen
        self.difficulty = difficulty
        self.font = pygame.font.SysFont('Arial', CELL_SIZE[0] // 2)
        self.font_color = pygame.Color("white")
        self.dropdown_open = False
        self.levels = ['hard', 'medium', 'easy']
        self._start_new_game()

    def _start_new_game(self):
        # chỉ gọi 1 lần
        self.puzzle = Sudoku(N_CELLS)
        self.puzzle.remove_digits(self._get_remove_count_from_difficulty())
        self.answers = self.puzzle.get_solution()
        self.answerable_table = self.puzzle.get_puzzle()
        self.SRN = self.puzzle.SRN
        self.table_cells = []
        self.clicked_cell = None
        self.lives = 3
        self.game_over = False
        self._generate_game()
        self._init_buttons()

    def _get_remove_count_from_difficulty(self):
        total_cells = N_CELLS * N_CELLS
        return {
            'hard': total_cells * 3 // 4,    # xóa 3/4 số ô (67 ô)
            'medium': total_cells // 2,      # xóa 1/2 số ô (40 ô)
            'easy': total_cells // 3         # xóa 1/3 số ô (30 ô)
        }.get(self.difficulty, total_cells // 2)

    def _generate_game(self):
        self.table_cells.clear()
        for row in range(N_CELLS):
            for col in range(N_CELLS):
                value = self.answerable_table[row][col]
                is_fixed = value != 0
                self.table_cells.append(Cell(row, col, CELL_SIZE, value, is_fixed))

    def _init_buttons(self):
        y_pos = HEIGHT + 10
        self.buttons = {
            "hint": pygame.Rect(10, y_pos, 45, 40),
            "solve_bt": pygame.Rect(60, y_pos, 100, 40),
            "solve_mrv": pygame.Rect(165, y_pos, 100, 40),
            "new_game": pygame.Rect(270, y_pos, 105, 40),
            "level": pygame.Rect(390, y_pos, 70, 40),
        }

    def _draw_grid(self):
        grid_color = (50, 80, 80)
        pygame.draw.rect(self.screen, grid_color, (-3, -3, WIDTH + 6, HEIGHT + 6), 6)
        for i in range(1, N_CELLS):
            line_width = 2 if i % self.SRN else 4
            pygame.draw.line(self.screen, grid_color, (i * CELL_SIZE[0], 0), (i * CELL_SIZE[0], HEIGHT), line_width)
            pygame.draw.line(self.screen, grid_color, (0, i * CELL_SIZE[1]), (WIDTH, i * CELL_SIZE[1]), line_width)

    def _draw_buttons(self):
        for name, rect in self.buttons.items():
            pygame.draw.rect(self.screen, pygame.Color("gray"), rect)
            label = self.font.render(name.replace("_", " ").capitalize(), True, self.font_color)
            self.screen.blit(label, (rect.x + 5, rect.y + 5))

        # Hiển thị dropdown nếu mở
        if self.dropdown_open:
            for i, level in enumerate(self.levels):
                dropdown_rect = pygame.Rect(360, HEIGHT + 50 + (i * 35), 140, 35)
                pygame.draw.rect(self.screen, pygame.Color("lightgray"), dropdown_rect)
                label = self.font.render(level.capitalize(), True, pygame.Color("black"))
                self.screen.blit(label, (dropdown_rect.x + 10, dropdown_rect.y + 5))

    def _get_cell_at_pos(self, pos):
        for cell in self.table_cells:
            if cell.rect.collidepoint(pos):
                return cell
        return None

    def _puzzle_solved(self):
        return all(
            cell.value == self.answers[cell.row][cell.col]
            for cell in self.table_cells
        )

    def handle_mouse_click(self, pos):
        if pos[1] < HEIGHT:
            cell = self._get_cell_at_pos(pos)
            if cell and not cell.is_fixed:
                self.clicked_cell = cell
        else:
            for name, rect in self.buttons.items():
                if rect.collidepoint(pos):
                    getattr(self, f"_on_{name}_click")()
                    return

            if self.dropdown_open:
                for i, level in enumerate(self.levels):
                    dropdown_rect = pygame.Rect(360, HEIGHT + 50 + (i * 35), 140, 35)
                    if dropdown_rect.collidepoint(pos):
                        self.difficulty = level
                        self.dropdown_open = False

                        # ✅ Tạo lại hoàn toàn Sudoku mới khi đổi level
                        self.puzzle = Sudoku(N_CELLS)
                        self.puzzle.remove_digits(self._get_remove_count_from_difficulty())
                        self.answers = self.puzzle.get_solution()
                        self.answerable_table = self.puzzle.get_puzzle()
                        self._generate_game()
                        self.lives = 3
                        self.game_over = False
                        return
            else:
                self.dropdown_open = False


    def handle_key_press(self, key):
        if self.clicked_cell and not self.clicked_cell.is_fixed and not self.game_over:
            number = None
            if pygame.K_1 <= key <= pygame.K_9:
                number = key - pygame.K_0
            elif pygame.K_KP1 <= key <= pygame.K_KP9:
                number = key - pygame.K_KP0

            if number:
                row = self.clicked_cell.row
                col = self.clicked_cell.col
                correct = self.answers[row][col]

                self.clicked_cell.value = number
                if number == correct:
                    self.clicked_cell.is_correct_guess = True
                else:
                    self.clicked_cell.is_correct_guess = False
                    self.lives -= 1

    def _on_hint_click(self):
        empty_cells = [cell for cell in self.table_cells if cell.value == 0]
        if empty_cells:
            cell = np.random.choice(empty_cells)
            row, col = cell.row, cell.col
            cell.value = self.answers[row][col]
            cell.is_correct_guess = True

    def _on_solve_click(self):
        puzzle = self.answerable_table
        stat_bt = solve_backtracking(puzzle)
        stat_mrv = solve_backtracking_mrv(puzzle)

        print("="*40)
        print("✅ Evaluation")
        print(stat_bt.report())
        print(stat_mrv.report())
        print("="*40)

        # Hiển thị lời giải MRV lên màn hình
        for cell in self.table_cells:
            row, col = cell.row, cell.col
            cell.value = stat_mrv.solved_board[row][col]
            cell.is_correct_guess = True

        self.game_over = True

    def _on_solve_bt_click(self):
        solved, t, loops = self.puzzle.solve_backtracking()
        for cell in self.table_cells:
            cell.value = solved[cell.row][cell.col]
            cell.is_correct_guess = True
        print(f"Backtracking: {loops} steps, {t:.4f}s")
        self.game_over = True

    def _on_solve_mrv_click(self):
        solved, t, loops = self.puzzle.solve_mrv()
        for cell in self.table_cells:
            cell.value = solved[cell.row][cell.col]
            cell.is_correct_guess = True
        print(f"MRV: {loops} steps, {t:.4f}s")
        self.game_over = True



    def _on_new_game_click(self):
        self.puzzle = Sudoku(N_CELLS)  # ✅ Tạo lại lời giải mới
        self.puzzle.remove_digits(self._get_remove_count_from_difficulty())
        self.answers = self.puzzle.get_solution()
        self.answerable_table = self.puzzle.get_puzzle()
        self._generate_game()
        self.lives = 3
        self.game_over = False



    def _on_level_click(self):
        self.dropdown_open = not self.dropdown_open

    def update(self):
        self.screen.fill((30, 30, 30))
        for cell in self.table_cells:
            cell.update(self.screen, self.SRN)
        self._draw_grid()
        self._draw_buttons()
        if self._puzzle_solved() or self.lives <= 0:
            self.game_over = True
