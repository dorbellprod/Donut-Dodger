import pygame
import time
import random
import math

pygame.init()
res = (500, 500)
screen = pygame.display.set_mode(res)
pygame.display.set_caption("you're mom")
run = True
clock = pygame.time.Clock()
donutSize = 35
playerSize = 50

iDonut = pygame.image.load("data/donut.png").convert_alpha()
iDonut = pygame.transform.scale(iDonut, (donutSize, donutSize))

iDing = pygame.image.load("data/ding.jpg").convert()
iDing = pygame.transform.scale(iDing, (playerSize, playerSize))

donuts = []

velInc = 1000
playerVel = 2000

sHit = pygame.mixer.Sound("data/hit.ogg")
sMusic = pygame.mixer.Sound("data/deez.ogg")

#GameOver
font = pygame.font.SysFont(("Futura", "Arial Black", "Arial", "Courier New"), 20)
class Donut:
    def __init__(self, x, y, vel):
        self.x = x
        self.y = y
        self.vel = vel
    def update():
        global dt
        global over
        global main
        for i in donuts:
            global dodgedDonuts
            if i.y > 480:
                donuts.remove(i)
                dodgedDonuts += 1
                continue
            for i in donuts:
                screen.blit(iDonut, (i.x, i.y))
            colliding = playerCollision(i)
            if colliding:
                print("COLLISION!!!!")
                over = True
                sHit.play()
                main = False
            i.y += i.vel * dt
                
                
    def spawn():
        rand = random.randint(0, res[0])
        newDonut = Donut(rand, -25, 250)
        donuts.append(newDonut)
class Player:
    def __init__(self, x, y, vel):
        self.x = x
        self.y = y
        self.vel = vel
        self.initVars = [x, y, vel]
    def reset(self):
        self.x = self.initVars[0]
        self.y = self.initVars[1]
        self.vel = self.initVars[2]
player = Player(250, 450, 0)

####################################
dt = 0
prevTime = time.time()
def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)
def deltaTime():
    global dt
    global prevTime
    now = time.time()
    dt = now - prevTime
    prevTime = now


def playerCollision(donut):
    global player
    newDonutCollider = [donut.x + 5, donut.x + donutSize - 5, donut.y + 5, donut.y + donutSize - 5]
    return player.x < newDonutCollider[1] and player.x + playerSize > newDonutCollider[0] and player.y < newDonutCollider[3] and player.y + playerSize > newDonutCollider[2]
####################################


#print(donuts)

main = False
over = False

pygame.mixer.music.load("data/deez.ogg")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)
while run:
    dodgedDonuts = 0
    print("Reset dodged donuts to 0 lol xD")
    player.reset()
    donutDelay = 0.33
    donutDelay_ = 0.33
    donuts = []
    while main:
        clock.tick(60)
        deltaTime()
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                main = False
        keys = pygame.key.get_pressed()
        if time.time() >= donutDelay_:
            donutDelay_ = time.time() + donutDelay
            Donut.spawn()

        if player.vel != 0:
            if player.vel > 0:
                player.vel -= velInc / 4 * dt
            elif player.vel < 0:
                player.vel += velInc / 4 * dt

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.vel -= int(velInc * dt)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.vel += int(velInc * dt)

        player.vel = clamp(player.vel, -playerVel, playerVel)
        player.x += player.vel * dt

        if player.x > res[0] - 25:
            player.x = res[0] - 25
            player.vel = 0
        elif player.x < 0:
            player.x = 0
            player.vel = 0

        
        #pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(player.x, player.y, 25, 25))
        Donut.update()
        screen.blit(iDing, (player.x, player.y))
        pygame.display.flip()
    while over:
        print("Game over")
        clock.tick(60)
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                over = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                main = True
                sHit.play()
                over = False
            
        text = f"u doged {dodgedDonuts} donut s"
        bruh = font.render(text, True, (255, 255, 255))
        screen.blit(bruh, (0 + bruh.get_width() / 2, 200))
        pygame.display.flip()
    
pygame.quit()