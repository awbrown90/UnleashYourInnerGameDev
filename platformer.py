import pygame
import sys

pygame.init()

# Game window settings
WIDTH, HEIGHT = 800, 600

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

class Character(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image_data = [
            "  BBB  ",
            "   B   ",
            "BBBKBBB",
            "B BBB B",
            "  BBB  ",
            " BB BB ",
            "B     B",
            "RR   RR"
        ]
        self.image = self.create_image()
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH // 2
        self.rect.y = HEIGHT - self.image.get_height() - 55  # Subtract the character height and ground height
        self.speed_x = 0
        self.speed_y = 0
        self.jumping = False
        self.on_ground = False
    
    def create_image(self):
        unscaled_image = pygame.Surface((len(self.image_data[0]), len(self.image_data)), pygame.SRCALPHA)
        for y, row in enumerate(self.image_data):
            for x, color_code in enumerate(row):
                if color_code == "B":
                    color = BLUE
                elif color_code == "R":
                    color = RED
                elif color_code == "W":
                    color = WHITE
                elif color_code == "K":
                    color = BLACK
                else:
                    color = None

                if color:
                    unscaled_image.set_at((x, y), color)

        scaled_width = unscaled_image.get_width() * 6
        scaled_height = unscaled_image.get_height() * 6
        image = pygame.transform.scale(unscaled_image, (scaled_width, scaled_height))

        return image
    
    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Gravity
        if not self.on_ground:
            self.speed_y += 1

        self.on_ground = False
        # Check for ground collision
        if self.rect.y >= HEIGHT - 100 and not self.on_ground:
            self.speed_y = 0
            self.rect.y = HEIGHT - 100
            self.on_ground = True

        # Check for platform collisions
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.speed_y > 0:  # Falling
                    self.rect.y = platform.rect.y - self.rect.height
                    self.speed_y = 0
                    self.on_ground = True
                elif self.speed_y < 0:  # Jumping
                    self.rect.y = platform.rect.y + platform.rect.height
                    self.speed_y = 0
            else:
                # Check if the character is standing on any platform
                for platform in platforms:
                    standing_rect = self.rect.copy()
                    standing_rect = standing_rect.move(0, 1)  # Move the rectangle down by 1 pixel
                    if standing_rect.colliderect(platform.rect):
                        self.on_ground = True
                        break

    def jump(self):
        if self.on_ground:
            self.jumping = True
            self.on_ground = False
            self.speed_y = -20

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Create some platforms
platforms = [
    Platform(100, 400, 200, 20),
    Platform(400, 300, 200, 20),
    Platform(650, 200, 100, 20)
]

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
    pygame.draw.rect(screen, BLUE, (0, HEIGHT - 55, WIDTH, 55))

    for platform in platforms:
        screen.blit(platform.image, platform.rect)

    pygame.display.flip()
    clock.tick(60)