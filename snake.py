import pygame
import sys
import random

pygame.init()

# Game window settings
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20
ROWS, COLS = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Snake and food
snake = [(2, 2), (2, 3), (2, 4)]
snake_dir = (0, 1)
food = None

def spawn_food():
    while True:
        candidate = (random.randint(0, ROWS - 1), random.randint(0, COLS - 1))
        if candidate not in snake:
            return candidate

food = spawn_food()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        snake_dir = (-1, 0)
    elif keys[pygame.K_DOWN]:
        snake_dir = (1, 0)
    elif keys[pygame.K_LEFT]:
        snake_dir = (0, -1)
    elif keys[pygame.K_RIGHT]:
        snake_dir = (0, 1)

    head = snake[-1]
    new_head = (head[0] + snake_dir[0], head[1] + snake_dir[1])

    if (
        new_head[0] < 0 or new_head[0] >= ROWS or
        new_head[1] < 0 or new_head[1] >= COLS or
        new_head in snake
    ):
        break

    snake.append(new_head)

    if new_head == food:
        food = spawn_food()
    else:
        snake.pop(0)

    screen.fill(WHITE)

    for segment in snake:
        pygame.draw.rect(screen, GREEN, (segment[1] * CELL_SIZE, segment[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    pygame.draw.rect(screen, RED, (food[1] * CELL_SIZE, food[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Draw grid lines
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, (200, 200, 200), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, (200, 200, 200), (0, y), (WIDTH, y))
    
    pygame.display.flip()
    clock.tick(10)


