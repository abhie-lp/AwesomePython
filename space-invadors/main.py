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


def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)


# Player
class Player(pygame.sprite.Sprite):
    POWERUP_TIME = 5000

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 40))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 19
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.health = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_time = pygame.time.get_ticks()

    def die(self):
        self.health = 100
        self.lives -= 1
        self.power = 1
        self.POWERUP_TIME = 5000

    def powerup(self, power):
        if self.power != 1 and self.power == power:
            self.POWERUP_TIME += 5000
            return
        else:
            self.POWERUP_TIME = 5000
        self.power = power
        self.power_time = pygame.time.get_ticks()

    def update(self, *args):
        if self.power >= 2 and \
                pygame.time.get_ticks() - self.power_time > self.POWERUP_TIME:
            self.power = 1
            self.power_time = pygame.time.get_ticks()
            self.POWERUP_TIME = 5000
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH // 2
            self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        elif keystate[pygame.K_RIGHT]:
            self.speedx = 5
        if keystate[pygame.K_SPACE]:
            self.shoot()

        self.rect.x += self.speedx

        # Check if the player is out of bounds
        if self.rect.right >= WIDTH:
            self.rect.right = WIDTH
        elif self.rect.left <= 0:
            self.rect.left = 0

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
            elif self.power == 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
            elif self.power == 3:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                bullet3 = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                all_sprites.add(bullet3)
                bullets.add(bullet1)
                bullets.add(bullet2)
                bullets.add(bullet3)
            shoot_snd.play()

    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH // 2, HEIGHT + 200)


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
        self.speedx = random.choice([-6, -5, -4, -3, -2, 2, 3, 4, 5, 6])
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


# POWERUPS
class Powerup(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(["life", "2X", "3X"])
        self.image = powerup_imgs[self.type]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 5

    def update(self, *args):
        self.rect.y += self.speedy

        # Kill it if it goes off the screen
        if self.rect.top > HEIGHT:
            self.kill()


# EXPLOSION
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = expl_grphics[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 75

    def update(self, *args):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(expl_grphics[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = expl_grphics[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


# Load all the game graphics
background = pygame.image.load(
    os.path.join(img_dir, "img", "background.png")
).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(
    os.path.join(img_dir, "img", "playerShip3_blue.png")
).convert()
player_mini_img = pygame.transform.scale(player_img, (25, 18))
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

expl_grphics = {"lg": [], "sm": [], "player": []}
for i in range(9):
    filename = "regularExplosion0{}.png".format(i)
    img = pygame.image.load(os.path.join(img_dir, "img", filename))
    img_lg = pygame.transform.scale(img, (75, 75))
    expl_grphics["lg"].append(img_lg)
    img_sm = pygame.transform.scale(img, (25, 25))
    expl_grphics["sm"].append(img_sm)

    # Player explosion
    filename = "sonicExplosion0{}.png".format(i)
    img = pygame.image.load(os.path.join(img_dir, "img", filename))
    expl_grphics["player"].append(img)

powerup_imgs = {"life": pygame.image.load(os.path.join(img_dir,
                                                       "img",
                                                       "shield.png")),
                "2X": pygame.image.load(os.path.join(img_dir,
                                                     "img",
                                                     "gun.png")),
                "3X": pygame.image.load(os.path.join(img_dir,
                                                     "img",
                                                     "3X.png"))}

# Load all the game sounds
shoot_snd = pygame.mixer.Sound(os.path.join(snd_dir, "sound", "shoot.wav"))
expl_sounds = []
for snd in ["exp1.wav", "exp2.wav"]:
    expl_sounds.append(pygame.mixer.Sound(os.path.join(snd_dir, "sound", snd)))

pygame.mixer.music.load(os.path.join(snd_dir,
                                     "sound",
                                     "tgfcoder-FrozenJam-SeamlessLoop.mp3"))
player_death_sound = pygame.mixer.Sound(os.path.join(snd_dir,
                                                     "sound",
                                                     "rumble1.ogg"))
life_sound = pygame.mixer.Sound(os.path.join(snd_dir, "sound", "pow5.wav"))
gun_sound = pygame.mixer.Sound(os.path.join(snd_dir, "sound", "pow4.wav"))

# Intialising Sprites
player = Player()

all_sprites = pygame.sprite.Group()
asteroids = pygame.sprite.Group()
bullets = pygame.sprite.Group()
powerups = pygame.sprite.Group()

# Registering the sprites
all_sprites.add(player)
for i in range(8):
    create_new_asteroid()

score = 0

pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(0.3)
shoot_snd.set_volume(0.3)

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

    # Update
    all_sprites.update()

    # If BULLETS hits ASTEROIDS
    hits = pygame.sprite.groupcollide(asteroids, bullets, False, True)
    if hits:
        for hit in hits:
            big_asteroid = False
            if hit.radius < 8:
                score += 5
            elif hit.radius < 13:
                score += 4
            elif hit.radius < 20:
                score += 3
            else:
                if hit.damage <= 1:
                    score += 2
                else:
                    hit.damage -= 1
                    big_asteroid = True
                    expl = Explosion(hit.rect.center, "sm")
                    all_sprites.add(expl)
            if not big_asteroid:
                hit.kill()
                expl = Explosion(hit.rect.center, "lg")
                all_sprites.add(expl)
                random.choice(expl_sounds).play()
                create_new_asteroid()
                if random.random() > 0.9:
                    power = Powerup(hit.rect.center)
                    all_sprites.add(power)
                    powerups.add(power)

    # If ASTEROIDS hits the PLAYER
    hits = pygame.sprite.spritecollide(player,
                                       asteroids,
                                       True,
                                       pygame.sprite.collide_circle)
    for hit in hits:
        expl = Explosion(hit.rect.center, "sm")
        all_sprites.add(expl)
        if hit.radius < 8:
            player.health -= 23
        elif hit.radius < 13:
            player.health -= 28
        elif hit.radius < 20:
            player.health -= 35
        else:
            player.health -= 40

        if player.health < 0:
            player_death_sound.play()
            death_explosion = Explosion(player.rect.center, "player")
            all_sprites.add(death_explosion)
            player.die()
            player.hide()
        create_new_asteroid()

    # If POWERUPS hit the PLAYER
    hits = pygame.sprite.spritecollide(player, powerups, True)
    if hits:
        for hit in hits:
            if hit.type == "life":
                life_sound.play()
                player.health += random.randint(20, 30)
                if player.health > 100:
                    player.health = 10
            else:
                gun_sound.play()
                if hit.type == "2X":
                    player.powerup(2)
                elif hit.type == "3X":
                    player.powerup(3)

    #  If the player dies and the explosion is finished
    if player.lives == 0 and not death_explosion.alive():
        running = False

    # Draw / render
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH/2, 10)
    draw_health_bar(screen, 5, 5, player.health)
    draw_lives(screen, WIDTH-100, 5, player.lives, player_mini_img)

    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
sys.exit()
