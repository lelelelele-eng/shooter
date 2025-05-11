#Создай собственный Шутер!

from pygame import *
from random import randint

window = display.set_mode((700,500))
display.set_caption('Шутер')
background = transform.scale(image.load('galaxy.jpg'), (700,500))
lost = 0

       
class GameSprite(sprite.Sprite):
    def __init__(self,player_image, player_x, player_y,size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(size_x,size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 720:
            self.rect.x += self.speed
    def fire(self):   
        bullet = Bullet('bullet.png',self.rect.centerx, self.rect.top, 15,20,15)
        bullets.add(bullet)
player = Player('rocket.png', 100, 400, 65 , 65, 5)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.x = randint(80,620)
            self.rect.y = 0
            lost += 1
    speed = randint(1,3)
    
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

class Asteroid(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

font.init()
font1 = font.SysFont('Arial',36)
font2 = font.SysFont('Arial',36)

bullets = sprite.Group()

mixer.init()
fire_sound = mixer.Sound('fire.ogg')
mixer.music.load('space.ogg')
mixer.music.play()


monsters = sprite.Group()
for i in range(1,6):
    monster = Enemy('ufo.png',randint(80,620),0,65,65,randint(1,3))
    monsters.add(monster)
asteroids = sprite.Group()
for i in range(1,3):
    asteroid = Enemy('asteroid.png',randint(80,600),0,65,65,randint(1,3))
    asteroids.add(asteroid)
game = True
while game:
    window.blit(background,(0,0))
    player.reset()
    player.update()
    bullets.draw(window)
    bullets.update()
    monsters.draw(window)
    monsters.update()
    asteroids.draw(window)
    asteroids.update()
    text_lose = font1.render("Пропущено" + str(lost),1,(255,255,255))
    window.blit(text_lose,(10,50))
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                player.fire()

    
    display.update()