import pygame
import sys
import random

pygame.init()
pygame.font.init()
font = pygame.font.Font(None, 36)

# Game window settings
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20
ROWS, COLS = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Snake and food
snake = [(2, 2), (2, 3), (2, 4)]
snake_dir = (0, 1)
food = None
obstacles = []
obstacle_directions = []
NUM_OBSTACLES = 10

def draw_score(score):
    text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(text, (10, 10))

def spawn_food():
    while True:
        candidate = (random.randint(0, ROWS - 1), random.randint(0, COLS - 1))
        if candidate not in snake:
            return candidate

def spawn_obstacles():
    global obstacle_directions
    obstacle_list = []
    obstacle_directions = []
    snake_head = snake[-1]
    forbidden_positions = [snake_head]

    # Add the next 10 positions in front of the snake to the forbidden_positions list
    for i in range(1, 11):
        forbidden_position = (snake_head[0] + snake_dir[0] * i, snake_head[1] + snake_dir[1] * i)
        if 0 <= forbidden_position[0] < ROWS and 0 <= forbidden_position[1] < COLS:
            forbidden_positions.append(forbidden_position)

    while len(obstacle_list) < NUM_OBSTACLES:
        candidate = (random.randint(0, ROWS - 1), random.randint(0, COLS - 1))
        if candidate not in forbidden_positions and candidate not in obstacle_list and candidate != food:
            obstacle_list.append(candidate)
            obstacle_directions.append((random.choice([-1, 1]), random.choice([-1, 1])))
            forbidden_positions.append(candidate)
    return obstacle_list

def update_obstacle_positions():
    global obstacles, obstacle_directions
    new_obstacles = []
    new_obstacle_directions = []

    for i, obstacle in enumerate(obstacles):
        direction = obstacle_directions[i]
        new_position = (obstacle[0] + direction[0], obstacle[1] + direction[1])

        # Check if the new position is within the game bounds
        if 0 <= new_position[0] < ROWS and 0 <= new_position[1] < COLS:
            new_obstacles.append(new_position)
            new_obstacle_directions.append(direction)
        else:
            # Change direction if the obstacle hits a wall
            new_direction = (-direction[0], -direction[1])
            new_position = (obstacle[0] + new_direction[0], obstacle[1] + new_direction[1])
            new_obstacles.append(new_position)
            new_obstacle_directions.append(new_direction)

    obstacles = new_obstacles
    obstacle_directions = new_obstacle_directions

food = spawn_food()
obstacles = spawn_obstacles()

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

    # Update obstacle positions
    update_obstacle_positions()

    head = snake[-1]
    new_head = (head[0] + snake_dir[0], head[1] + snake_dir[1])

    if (
        new_head[0] < 0 or new_head[0] >= ROWS or
        new_head[1] < 0 or new_head[1] >= COLS or
        new_head in snake or new_head in obstacles
    ):
        break

    snake.append(new_head)

    if new_head == food:
        food = spawn_food()
        obstacles = spawn_obstacles()
    else:
        snake.pop(0)

    screen.fill(WHITE)

    for segment in snake:
        pygame.draw.rect(screen, GREEN, (segment[1] * CELL_SIZE, segment[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    pygame.draw.rect(screen, RED, (food[1] * CELL_SIZE, food[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Draw obstacles
    for obstacle in obstacles:
        pygame.draw.rect(screen, BLUE, (obstacle[1] * CELL_SIZE, obstacle[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Draw grid lines
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, (200, 200, 200), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, (200, 200, 200), (0, y), (WIDTH, y))

    draw_score(len(snake) - 3)
    pygame.display.flip()
    clock.tick(10)

