import pygame
import random
import sys
from game_config import *

class SnakeGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 30)

        self.snake = [(WIDTH//2, HEIGHT//2)]
        self.direction = RIGHT
        self.food = self.generate_food()
        self.score = 0
        self.game_over = False

    def generate_food(self):
        while True:
            x = random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
            y = random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
            if (x, y) not in self.snake:
                return (x, y)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.direction != DOWN:
                    self.direction = UP
                elif event.key == pygame.K_DOWN and self.direction != DOWN:
                    self.direction = DOWN
                elif event.key == pygame.K_LEFT and self.direction != RIGHT:
                    self.direction = LEFT
                elif event.key == pygame.K_RIGHT and self.direction != LEFT:
                    self.direction = RIGHT
                elif event.key == pygame.K_r and self.game_over:
                    self.__init__()

    def move_snake(self):
        if self.game_over:
            return

        head_x, head_y = self.snake[0]
        new_head = (head_x + self.direction[0] * CELL_SIZE,
                    head_y + self.direction[1] * CELL_SIZE)

        # Check collisions
        if (new_head in self.snake or
                new_head[0] < 0 or new_head[0] >= WIDTH or
                new_head[1] < 0 or new_head[1] >= HEIGHT):
            self.game_over = True
            return

        self.snake.insert(0, new_head)

        # Check food collision
        if new_head == self.food:
            self.score += 10
            self.food = self.generate_food()
        else:
            self.snake.pop()

    def draw(self):
        self.screen.fill(BLACK)

        # Draw snake
        for idx, segment in enumerate(self.snake):
            color = GREEN if idx == 0 else BLUE
            pygame.draw.rect(self.screen, color, (segment[0], segment[1], CELL_SIZE, CELL_SIZE))

        # Draw food
        pygame.draw.rect(self.screen, RED, (self.food[0], self.food[1], CELL_SIZE, CELL_SIZE))

        # Draw score
        score_text = self.font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))

        if self.game_over:
            self.draw_game_over()

        pygame.display.flip()

    def draw_game_over(self):
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))

        game_over_text = self.font.render('Game Over!', True, RED)
        score_text = self.font.render(f'Final Score: {self.score}', True, WHITE)
        restart_text = self.font.render('Press R to Restart', True, YELLOW)
        quit_text = self.font.render('Press Q to Quit', True, YELLOW)

        self.screen.blit(game_over_text, (WIDTH//2 - 80, HEIGHT//2 - 60))
        self.screen.blit(score_text, (WIDTH//2 - 90, HEIGHT//2 - 20))
        self.screen.blit(restart_text, (WIDTH//2 - 110, HEIGHT//2 + 20))
        self.screen.blit(quit_text, (WIDTH//2 - 90, HEIGHT//2 + 60))

    def run(self):
        while True:
            self.handle_input()
            self.move_snake()
            self.draw()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = SnakeGame()
    game.run()