#Створи власний Шутер
from pygame import *
from random import randint
mixer.init()
mixer.music.load("space.ogg")
from time import time as timer 

fire_sound = mixer.Sound("fire.ogg")

img_back ="galaxy.jpg"
img_rocket = "rocket.png"
life = 3
font.init()
font1 = font.SysFont("Arial", 80)
font2 = font.SysFont("Arial", 40)
win = font1.render("You win", True, (255,4,66))
lose = font1.render("You lose", True, (255,255,255))
score = 0
goal = 10
lost = 0
max_lost = 3
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y,size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update (self):
        k = key.get_pressed()
        if k [K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if k [K_RIGHT] and self.rect.x < 620:
            self.rect.x += self.speed
    def fire (self):
        bullet = Bullet("bullet.png", self.rect.centerx,self.rect.top,15,20,-15)
        bullets.add(bullet)

class Enemy (GameSprite):
    def update (self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.x = randint(80, 620)
            self.rect.y = 0
            lost = lost + 1
class Bullet (GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back),(win_width, win_height))
ship = Player ("rocket.png", 5, 400,80, 100, 15)
run = True
finish = False
rel_time = False
font.init()
num_fire = 0
monsters = sprite.Group()
bullets  = sprite.Group()
asteroids = sprite.Group()
for i in range(1,6):
    monster = Enemy("ufo.png",randint(80, 620),-40,80, 50, randint(1,5))
    monsters.add(monster)
    asteroid = Enemy("asteroid.png",randint(80, 620),-40,40, 40, randint(5,20))
    asteroids.add(asteroid)


while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    fire_sound.play()
                    ship.fire()
                if num_fire >= 5 and rel_time == False:
                    rel_time = True
                    last_time = timer( )

    if not finish:
        window.blit(background, (0, 0))
        ship.update()
        ship.reset()
        monsters.update()
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)
        asteroids.update()
        asteroids.draw(window)

        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font2.render("Wait...reload", 1, (150,0,0))
                window.blit (reload, (260, 460))
            else:
                num_fire  = 0
                rel_time = False

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score +1
            monster = Enemy(img_enemy,randint(80, 620),-40,80, 50, randint(1,5))
            monsters.add(monster)
        if sprite.spritecollide(ship,monsters,False) or sprite.spritecollide(ship, asteroids, False) :
            sprire.spritecollide(ship, monsters, True)
            sprire.spritecollide(ship, asteroids, True)
            life = life - 1
        if life == 0 or lost >= max_lost:
            finish = True
            window .blit(lose, (200,200))
        if score >= goal:
            finish = True
            window.blit(win, (200,200))
        color1 = (0,150,0)
        color2 = (100,150,0)
        color3 = (150,0,0)
        if life == 3:
            color_life = (0,150,0)
        if life == 2:
            color_life = (100,150,0)
        if life == 1:
            color_life = (150,0,0)
        text_life = font1.render("life"+str(life), 1, color_life)
        window.blit(text_life, (550,10))
        texy_lose = font2.render("Пропущено"+str(lost),1, (255,255,255))
        window.blit(text_lose,(10,50))
        score_text = font2.render("Score"+str(score),1,(255,255, 0))
        window.blit(score_text, (10,20))
        display.update()
    else:
        finish = False
        score = 0
        lost = 0
        life = 3
        num_fire = 0
        for m in monsters:
            m.kill()
        for a in asteroids:
            a.kill()
        for i in range(1,6):
            monster = Enemy("ufo.png",randint(80, 620),-40,80, 50, randint(1,5))
            monsters.add(monster)
        for i in range (1,3):
            asteroid = Enemy("asteroid.png",randint(80, 620),-40,40, 40, randint(5,20))
            asteroids.add(asteroid)
        time.delay(3000)
    time.delay(50)



