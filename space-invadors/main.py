# Space invadors
import os
import random
import sys
import pygame

img_dir = os.path.dirname(__file__)
snd_dir = os.path.dirname(__file__)

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
font_name = pygame.font.match_font("arial")


def create_new_asteroid():
    a = Asteroids()
    all_sprites.add(a)
    asteroids.add(a)


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def draw_health_bar(surf, x, y, value):
    if value < 0:
        value = 0
    bar_length = 100
    bar_height = 10
    pct = (value / 100) * bar_length
    outline_rect = pygame.Rect(x, y, bar_length, bar_height)
    inside_rect = pygame.Rect(x, y, pct, bar_height)
    pygame.draw.rect(surf, GREEN, inside_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)


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
        self.health = 100

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
        shoot_snd.play()


# Asteroids
class Asteroids(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(asteroid_imgs)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 // 2)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, 100)
        self.speedy = random.randint(1, 8)
        self.speedx = random.choice([-7, -6, -5, -4, -3, -2, 2, 3, 4, 5, 6, 7])
        self.rot = 0
        self.rot_speed = random.randint(-8, 8)
        self.last_update = pygame.time.get_ticks()
        self.damage = 2

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
bullet_img = pygame.image.load(
    os.path.join(img_dir, "img", "laserRed16.png")
).convert()

asteroid_imgs = []
asteroid_list = ["meteorBrown_big2.png", "meteorBrown_big4.png",
                 "meteorBrown_med1.png", "meteorBrown_med3.png",
                 "meteorBrown_small1.png", "meteorBrown_small2.png",
                 "meteorGrey_tiny1.png", "meteorGrey_tiny2.png"]

for img in asteroid_list:
    asteroid_imgs.append(pygame.image.load(
        os.path.join(img_dir, "img", img)
    ))

# Load all the game sounds
shoot_snd = pygame.mixer.Sound(os.path.join(snd_dir, "sound", "shoot.wav"))
expl_sounds = []
for snd in ["exp1.wav", "exp2.wav"]:
    expl_sounds.append(pygame.mixer.Sound(os.path.join(snd_dir, "sound", snd)))

pygame.mixer.music.load(os.path.join(snd_dir,
                                     "sound",
                                     "tgfcoder-FrozenJam-SeamlessLoop.mp3"))

# Intialising Sprites
player = Player()

all_sprites = pygame.sprite.Group()
asteroids = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Registering the sprites
all_sprites.add(player)
for i in range(8):
    create_new_asteroid()

score = 0

# Game loop
running = True
pygame.mixer.music.play(loops=-1)
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
    hits = pygame.sprite.groupcollide(asteroids, bullets, False, True)
    if hits:
        for hit in hits:
            if hit.radius < 8:
                score += 5
            elif hit.radius < 13:
                score += 4
            elif hit.radius < 20:
                score += 3
            else:
                if hit.damage == 0:
                    score += 2
                else:
                    hit.damage -= 1
                    continue
            hit.kill()
            random.choice(expl_sounds).play()
            create_new_asteroid()

    # If ASTEROIDS hits the PLAYER
    hits = pygame.sprite.spritecollide(player,
                                       asteroids,
                                       True,
                                       pygame.sprite.collide_circle)
    for hit in hits:
        if hit.radius < 8:
            player.health -= 23
        elif hit.radius < 13:
            player.health -= 28
        elif hit.radius < 20:
            player.health -= 35
        else:
            player.health -= 40
        if player.health < 0:
            running = False
        create_new_asteroid()

    # Draw / render
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH/2, 10)
    draw_health_bar(screen, 5, 5, player.health)

    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
sys.exit()
