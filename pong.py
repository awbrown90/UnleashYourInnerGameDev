import pygame
import sys

pygame.init()
pygame.font.init()
font = pygame.font.Font(None, 36)

# Game window settings
WIDTH, HEIGHT = 800, 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Paddle and ball
paddle_height = 100
paddle_width = 10
ball_size = 10

paddle_y = HEIGHT // 2 - paddle_height // 2
ball_x, ball_y = WIDTH // 2 - ball_size // 2, HEIGHT // 2 - ball_size // 2
ball_speed_x, ball_speed_y = 5, 5

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

def draw_score(score):
    font = pygame.font.Font(None, 36)
    score_text = "Speed: {:.3f}".format(score)
    text = font.render(score_text, True, WHITE)
    screen.blit(text, (10, 10))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        paddle_y -= 5
    if keys[pygame.K_DOWN]:
        paddle_y += 5

    # Clamp paddle position
    paddle_y = max(0, min(HEIGHT - paddle_height, paddle_y))

    # Update ball position
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Check for collisions
    if ball_y <= 0 or ball_y + ball_size >= HEIGHT:
        ball_speed_y = -ball_speed_y

    if ball_x <= paddle_width and (paddle_y <= ball_y <= paddle_y + paddle_height):
        ball_speed_x = -ball_speed_x

    # Bounce off the right wall and increase speed
    if ball_x + ball_size >= WIDTH:
        ball_speed_x = -ball_speed_x * 1.1
        ball_speed_y *= 1.1

    # Reset the ball position if it goes past the paddle
    if ball_x < 0:
        ball_x, ball_y = WIDTH // 2 - ball_size // 2, HEIGHT // 2 - ball_size // 2
        ball_speed_x, ball_speed_y = 5, 5

    # Draw the screen
    screen.fill(BLACK)

    # Draw the paddle
    pygame.draw.rect(screen, WHITE, (0, paddle_y, paddle_width, paddle_height))

    # Draw the ball
    pygame.draw.rect(screen, WHITE, (ball_x, ball_y, ball_size, ball_size))

    draw_score(abs(ball_speed_x))
    pygame.display.flip()
    clock.tick(60)
