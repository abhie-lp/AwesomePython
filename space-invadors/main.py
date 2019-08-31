# Space invadors
import os
import random
import sys
import pygame

img_dir = os.path.dirname(__file__)

WIDTH = 480
HEIGHT = 600
FPS = 60

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Initialise pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invadors")
clock = pygame.time.Clock()


def create_new_asteroid():
    a = Asteroids()
    all_sprites.add(a)
    asteroids.add(a)


# Player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 40))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 18
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0

    def update(self, *args):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        elif keystate[pygame.K_RIGHT]:
            self.speedx = 5
        self.rect.x += self.speedx

        # Check if the player is out of bounds
        if self.rect.right >= WIDTH:
            self.rect.right = WIDTH
        elif self.rect.left <= 0:
            self.rect.left = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)


# Asteroids
class Asteroids(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = asteroid_img
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .9 // 2)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, 100)
        self.speedy = random.randint(1, 8)
        self.speedx = random.choice([-7, -6, -5, -4, -3, -2, 2, 3, 4, 5, 6, 7])
        self.rot = 0
        self.rot_speed = random.randint(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig,
                                                self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center
            self.last_update = now

    def update(self, *args):
        self.rotate()
        if self.rect.left < 0:
            self.speedx *= -1
        elif self.rect.right > WIDTH:
            self.speedx *= -1

        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.top > HEIGHT + 10:
            self.kill()
            create_new_asteroid()


# BULLETS
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self, *args):
        self.rect.y += self.speedy

        if self.rect.bottom < 0:
            self.kill()


# Load all the game graphics
background = pygame.image.load(
    os.path.join(img_dir, "img", "background.png")
).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(
    os.path.join(img_dir, "img", "playerShip3_blue.png")
).convert()
asteroid_img = pygame.image.load(
    os.path.join(img_dir, "img", "meteorBrown_med3.png")
).convert()
bullet_img = pygame.image.load(
    os.path.join(img_dir, "img", "laserRed16.png")
).convert()

# Intialising Sprites
player = Player()

all_sprites = pygame.sprite.Group()
asteroids = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Registering the sprites
all_sprites.add(player)
for i in range(8):
    m = Asteroids()
    all_sprites.add(m)
    asteroids.add(m)

# Game loop
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)

    # Process input
    for event in pygame.event.get():
        # check for closing the window
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # Update
    all_sprites.update()

    # If BULLETS hits ASTEROIDS
    hits = pygame.sprite.groupcollide(asteroids, bullets, True, True)
    if hits:
        for hit in hits:
            m = Asteroids()
            all_sprites.add(m)
            asteroids.add(m)

    # If ASTEROIDS hits the PLAYER
    hits = pygame.sprite.spritecollide(player,
                                       asteroids,
                                       False,
                                       pygame.sprite.collide_circle)
    if hits:
        running = False

    # Draw / render
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)

    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
sys.exit()
