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
sSelect = pygame.mixer.Sound("data/select.ogg")
sMusic = pygame.mixer.Sound("data/deez.ogg")

#GameOver
font = pygame.font.SysFont(("Futura", "Arial Black", "Arial", "Courier New"), 20)
bigFont = pygame.font.SysFont(("Futura", "Arial Black", "Arial", "Courier New"), 40)
class Donut:
    def __init__(self, x, y, vel):
        self.x = x
        self.y = y
        self.vel = vel
    def update():
        global dt
        global over
        global main
        global donuts
        global dodgedDonuts
        global donutVelMult
        global pooled
        if len(donuts) == 0: return
        for i in donuts:
            if i.y > 490:
                if not pooled: pooled = True
                dodgedDonuts += 1
                rand = random.randint(0, res[0])
                i.y = -50
                i.x = rand
                continue
            
            colliding = playerCollision(i)
            if colliding:
                print("COLLISION!!!!")
                over = True
                sHit.play()
                main = False
            i.y += i.vel * donutVelMult * dt
            
                
                
    def spawn():
        rand = random.randint(0, res[0])
        newDonut = Donut(rand, -50, 250)
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

##EXTRA STUFF############################
def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)
dt = 0
prevTime = time.time()
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
menu = True

pygame.mixer.music.load("data/deez.ogg")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

sHit.set_volume(0.7)

#STATS ETC
dodgedDonuts = 0
donutDelay = 0.33
donutDelay_ = 0.33

diff = 1
diffs = ["Easy", "Normal", "Hard"]
while run:
    poopy = time.time() + 1.5 / 0.352945328
    poopIndex = 0
    texts = [f"Press [Space]", "Live, laugh, eat donuts", "Long live the donut", "Did I mention donuts?"]
    texts2 = f"[<] {diffs[diff % len(diffs)]} [>]"
    textss = ["Easy", "Medium", "Hard"]
    poopyLength = len(texts)

    #FPS
    fps_choice = 2
    fps_choices = [15, 30, 60, 120, 144, 165, 240, 999]
    fps_cap = 60
    fps_length = len(fps_choices)
    while menu:
        clock.tick(fps_cap)
        deltaTime()
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                menu = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main = True
                    sHit.play()
                    menu = False
                if event.key == pygame.K_f:
                    fps_choice += 1
                    fps_cap = fps_choices[fps_choice % fps_length]
                    print(f"FPS IS NOW {fps_cap}")
                if event.key == pygame.K_LEFT:
                    if diff > 0:
                        diff -= 1
                        texts2 = f"[<] {diffs[diff % len(diffs)]} [>]"
                        sSelect.play()
                    else:
                        sHit.play()
                if event.key == pygame.K_RIGHT:
                    if diff < 2:
                        diff += 1
                        texts2 =  f"[<] {diffs[diff % len(diffs)]} [>]"
                        sSelect.play()
                    else:
                        sHit.play()
            
        if time.time() >= poopy:
            poopy = time.time() + 1.5 / 0.352945328
            poopIndex += 1

        text = texts[poopIndex % poopyLength]
        bruh = font.render(text, True, (0, 0, 0))
        bruh2 = font.render(texts2, True, (0, 0, 0))
        title = bigFont.render("DONUT DODGER PY", True, (0, 0, 0))
        screen.blit(title, (res[0] / 2 - title.get_width() / 2, 40))
        screen.blit(bruh, (res[0] / 2 - bruh.get_width() / 2, 200 - 2 *math.fabs(math.sin(time.time() / 0.352945328) * 10)))
        screen.blit(bruh2, (res[0] / 2 - bruh2.get_width() / 2, 250 - 2 *math.fabs(math.sin(time.time() / 0.352945328) * 10)))
        pygame.display.flip()

    donutVelMult = (diff % len(diffs) + 1) * 0.75
    dodgedDonuts = 0
    donutDelay = 0.2
    donutDelay_ = time.time() + donutDelay
    donuts = []
    player.reset()

    #POOLING
    pooled = False

    while main:
        clock.tick(fps_cap)
        deltaTime()
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                main = False
        keys = pygame.key.get_pressed()
        if not pooled:
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
        print(dt)

        if player.x > res[0] - 50:
            player.x = res[0] - 50
            player.vel = 0
        elif player.x < 0:
            player.x = 0
            player.vel = 0

        
        #pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(player.x, player.y, 25, 25))
        Donut.update()
        screen.blit(iDing, (player.x, player.y))
        for i in donuts:
            screen.blit(iDonut, (i.x, i.y))
        pygame.display.flip()
    
    ###################################GAME OVER#########################################

    while over:
        clock.tick(fps_cap)
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                over = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                menu = True
                sHit.play()
                over = False
        text = f"u doged {dodgedDonuts} donut s on {diffs[diff]} mod e."
        bruh = font.render(text, True, (255, 255, 255))
        screen.blit(bruh, (0 + 25, 200))
        pygame.display.flip()
    
pygame.quit()