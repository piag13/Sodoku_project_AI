# cell.py
import pygame
from setting import convert_list

pygame.font.init()

class Cell:
    def __init__(self, row, col, cell_size, value, is_fixed=False):
        self.row = row
        self.col = col
        self.value = value
        self.is_fixed = is_fixed  # Added this line
        self.is_correct = None
        self.width, self.height = cell_size
        self.x = row * self.width
        self.y = col * self.height
        self.color = pygame.Color("white")
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.guesses = None if value != 0 else [0] * 9

        self.font = pygame.font.SysFont('monospace', self.width)
        self.g_font = pygame.font.SysFont('monospace', self.width // 3)

    def update(self, screen, SRN=None):
        pygame.draw.rect(screen, self.color, self.rect)

        if self.value != 0:
            color = pygame.Color("black") if self.is_fixed or self.is_correct else pygame.Color("red")
            text = self.font.render(str(self.value), True, color)
            screen.blit(text, (self.x, self.y))
        elif self.guesses is not None:
            guess_grid = convert_list(self.guesses, [SRN] * 3)
            cell_w, cell_h = self.width // SRN, self.height // SRN

            for i in range(SRN):
                for j in range(SRN):
                    val = guess_grid[i][j]
                    if val != 0:
                        guess = self.g_font.render(str(val), True, pygame.Color("orange"))
                        pos = (self.x + j * cell_w, self.y + i * cell_h)
                        screen.blit(guess, pos)