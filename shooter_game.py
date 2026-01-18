#Create your own shooter

from pygame import *
from random import randint

img_pilot = "rocket.png"
img_back = "galaxy.jpg"
img_enemy = "ufo.png"
img_asteroid = "asteroid.png"
img_bullet = "bullet.png"

win_width = 700
win_height = 500
display.set_caption("Space Invaders")
window = display.set_mode((win_width,win_height))
background = transform.scale(image.load(img_back),(win_width,win_height))

mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
fire_sfx = mixer.Sound("fire.ogg")

font.init()
font2 = font.SysFont('Arial',36)

score = 0
lost = 0
lives = 5
wave = 1
win_cond = 10
alien_limit = 6
asteroid_limit = 3

class GameSprite(sprite.Sprite):
    def __init__(self,player_img,player_x,player_y,size_x,size_y,player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_img),(size_x,size_y))
        self.step = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

class Player(GameSprite):
    def move(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.step
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.step
    
    def fire(self):
        bullet = Bullet(img_bullet,self.rect.centerx,self.rect.top,15,20,-15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.step
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80,win_width-80)
            self.rect.y = 0
            lost += 1

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.step
        if self.rect.y > win_height:
            self.rect.x = randint(80,win_width-80)
            self.rect.y = 0

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.step
        if self.rect.y < 0:
            self.kill()

ship = Player(img_pilot,5,win_height-100,80,100,10)
bullets = sprite.Group()
win_txt = font2.render('YOU WIN!', True, (255, 215, 0))
lose_txt = font2.render('YOU LOSE!', True, (180, 0, 0))

aliens = sprite.Group()
for i in range(1,alien_limit+1):
    alien = Enemy(img_enemy,randint(80,win_width-80),-40,80,50,randint(1,5))
    aliens.add(alien)

asteroids = sprite.Group()
for i in range(1,asteroid_limit+1):
    asteroid = Asteroid(img_asteroid,randint(80,win_width-80),-40,80,50,randint(1,5))
    asteroids.add(asteroid)

finish = False
run = True

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
            finish = True
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                ship.fire()
                fire_sfx.play()

    if not finish:
        window.blit(background,(0,0))

        text_score = font2.render("Score: "+str(score),1,(255,255,255))
        window.blit(text_score,(10,20))

        text_lost = font2.render("Missed: "+str(lost),1,(255,255,255))
        window.blit(text_lost,(10,50))

        text_life = font2.render("Hp: "+str(lives),1,(255,255,255))
        window.blit(text_life,(10,80))

        text_wave = font2.render("Wave: "+str(wave),1,(255,255,255))
        window.blit(text_wave,(10,110))

        collisions = sprite.groupcollide(bullets,aliens,True,True)
        for c in collisions:
            score += 1
            alien = Enemy(img_enemy,randint(80,win_width-80),-40,80,50,randint(1,5))
            aliens.add(alien)
        
        if sprite.spritecollide(ship,aliens,True) or sprite.spritecollide(ship,asteroids,True):
            lives -= 1

        if  lives <= 0 or lost >= 3:
            finish = True
            window.blit(lose_txt,(250,250))
            lives = 5
            win_cond = 10
            alien_limit = 5
            asteroid_limit = 3
        
        if score == win_cond:
            wave += 1
            finish = True
            window.blit(win_txt,(250,250))
            win_cond += 15
            alien_limit += 3
            asteroid_limit += 1

        ship.move()
        aliens.update()
        asteroids.update()
        bullets.update()
        ship.reset()
        aliens.draw(window)
        asteroids.draw(window)
        bullets.draw(window)

        win_txt = font2.render('YOU WIN!', True, (255, 215, 0))
        lose_txt = font2.render('YOU LOSE!', True, (180, 0, 0))

        display.update()
    else:
        time.delay(5000)
        finish = False
        lost = 0
        score = 0
        for b in bullets:
            b.kill()
        for a in aliens:
            a.kill()
        for i in asteroids:
            i.kill()
        
        for i in range(1,alien_limit+1):
            alien = Enemy(img_enemy,randint(80,win_width-80),-40,80,50,randint(1,5))
            aliens.add(alien)

        for i in range(1,asteroid_limit+1):
            asteroid = Asteroid(img_asteroid,randint(80,win_width-80),-40,80,50,randint(1,5))
            asteroids.add(asteroid)

    time.delay(50)