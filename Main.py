# main.py
import pygame
import sys
from setting import WIDTH, HEIGHT, CELL_SIZE
from Table import Table

pygame.init()

SCREEN_HEIGHT = HEIGHT + (CELL_SIZE[1] * 3)
screen = pygame.display.set_mode((WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sudoku")
pygame.font.init()

class SudokuGame:
    def __init__(self, screen):
        self.screen = screen
        self.table = Table(screen)
        self.lives_font = pygame.font.SysFont("monospace", CELL_SIZE[0] // 2)
        self.message_font = pygame.font.SysFont("Bauhaus 93", CELL_SIZE[0])
        self.success_color = pygame.Color("darkgreen")

    def run(self):
        while True:
            self.handle_events()
            self.draw()
            pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.table.handle_mouse_click(event.pos)
            elif event.type == pygame.KEYDOWN:
                self.table.handle_key_press(event.key)

    def draw(self):
        self.screen.fill("gray")
        self.table.update()

        if self.table.game_over:
            self.show_game_message()
        else:
            self.show_lives_left()

    def show_lives_left(self):
        text = self.lives_font.render(
            f"Lives Left: {self.table.lives}", True, pygame.Color("white")
        )
        pos = ((WIDTH // self.table.SRN), HEIGHT + CELL_SIZE[1] * 2.2)
        self.screen.blit(text, pos)

    def show_game_message(self):
        if self.table.lives <= 0:
            msg = "GAME OVER!!"
            color = pygame.Color("red")
        else:
            msg = "You Made It!!!"
            color = self.success_color

        message = self.message_font.render(msg, True, color)
        self.screen.blit(message, (CELL_SIZE[0], HEIGHT + CELL_SIZE[1] * 2))

    def draw_buttons(self):
        font = pygame.font.SysFont("monospace", 24)
        reset_btn = pygame.Rect(WIDTH // 2 - 50, HEIGHT + 10, 100, 40)
        pygame.draw.rect(self.screen, pygame.Color("white"), reset_btn)
        text = font.render("Reset", True, pygame.Color("black"))
        self.screen.blit(text, (reset_btn.x + 10, reset_btn.y + 5))
        return reset_btn

if __name__ == "__main__":
    game = SudokuGame(screen)
    game.run()


