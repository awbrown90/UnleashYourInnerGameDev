import pygame
import sys

pygame.init()

# Game window settings
WIDTH, HEIGHT = 800, 600

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

class Character(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH // 2
        self.rect.y = HEIGHT - 100
        self.speed_x = 0
        self.speed_y = 0
        self.jumping = False
        self.on_ground = False

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Gravity
        if not self.on_ground:
            self.speed_y += 1

        # Check for ground collision
        if self.rect.y >= HEIGHT - 100 and not self.on_ground:
            self.speed_y = 0
            self.rect.y = HEIGHT - 100
            self.on_ground = True

    def jump(self):
        if self.on_ground:
            self.jumping = True
            self.on_ground = False
            self.speed_y = -20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

character = Character()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        character.speed_x = -5
    elif keys[pygame.K_RIGHT]:
        character.speed_x = 5
    else:
        character.speed_x = 0

    if keys[pygame.K_SPACE]:
        character.jump()

    character.update()

    screen.fill(WHITE)

    # Draw the character
    screen.blit(character.image, character.rect)

    # Draw the ground
    pygame.draw.rect(screen, BLUE, (0, HEIGHT - 50, WIDTH, 50))

    pygame.display.flip()
    clock.tick(60)
