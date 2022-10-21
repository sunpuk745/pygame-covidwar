import random
import pygame

#setup
WIDTH = 600
HEIGHT = 800
FPS = 60
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Covid19War")
font = pygame.font.SysFont("Agency FB", 40, bold=True)
bg = pygame.image.load("bg.png")
bg_offset = bg.get_height()-HEIGHT
pygame.mixer.init()
boom_sound = pygame.mixer.Sound("boom.wav")
shoot_sound = pygame.mixer.Sound("shoot_cure.mp3") #shoot sound
reload_sound = pygame.mixer.Sound("Reload_Gun.mp3") #reload sound
covid_die_sound = pygame.mixer.Sound("covid_die.mp3") # Covid die sound
full_reload_sound = pygame.mixer.Sound("full_reload_sound.mp3") # full reload sound
shotgun_sound = pygame.mixer.Sound("shotgun_shot.mp3") # shotgun sound
rifle_sound = pygame.mixer.Sound("sniper_shot.mp3") # sniper rifle sound
reload_sound.set_volume(0.2)
boom_sound.set_volume(0.2)
shoot_sound.set_volume(0.1)
covid_die_sound.set_volume(0.2)
full_reload_sound.set_volume(0.2)
shotgun_sound.set_volume(0.05)
rifle_sound.set_volume(0.2)
clock = pygame.time.Clock()
running = 1
ultimate_modeTime = 5000 # ultimate mode time 8 seconds
reload_fullMagTime = 1800 # Time for reloading full magazine
current_time = pygame.time.get_ticks() # variable for get current time you pick up the item
ultimate_mode_endTime = current_time + ultimate_modeTime # variable for calculate ultimate mode time
reload_fullMag = current_time + reload_fullMagTime # variable for calculate reload time
reloading = False


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.playerImages = [pygame.image.load("JiJiSR1.png").convert_alpha(),
                         pygame.image.load("JiJiSR1L.png").convert_alpha(),
                         pygame.image.load("JiJiSR1R.png").convert_alpha()]
        self.image = self.playerImages[0]
        self.rect = self.image.get_rect()
        self.rect.midbottom = WIDTH/2, HEIGHT-50
        self.radius = 40
        self.speedx = 0
        self.lastSpeedx = self.speedx
        self.life = 100
        self.score = 0
        self.Normal = True # Normal Shooting Mode
        self.Shotgun = False # Shotgun Shooting Mode
        self.Pierce = False # Pierce Shooting Mode
        self.Unlimited = False # Unlimited Shooting Mode

    def update(self):
        self.rect.x += self.speedx
        if (self.speedx < 0 ) and (self.lastSpeedx != self.speedx):
            #print("left",self.lastSpeedx,self.speedx)
            self.image = self.playerImages[1]
        elif (self.speedx > 0 ) and (self.lastSpeedx != self.speedx):
            #print("right",self.lastSpeedx,self.speedx)
            self.image = self.playerImages[2]
        elif (self.speedx == 0)  and (self.lastSpeedx != self.speedx):
            #print("center",self.lastSpeedx,self.speedx)
            self.image = self.playerImages[0]
        self.lastSpeedx = self.speedx

        # Make player can't move out of the screen
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        if self.Normal == True:
            cure = Cure(self.rect.centerx, self.rect.top)
            cure.speedx = 0
            shoot_sound.play() # play shoot sound when shooting cure
            allsprites.add(cure)
            cures.add(cure)

        # Shoot in Shotgun Mode if Shotgun Mode is active
        elif self.Shotgun == True: 
            #print(Cure.special_cure_count)
            for i in range(7):
                cure = Cure(self.rect.centerx, self.rect.top)
                cure.speedx = random.randrange(-3, 3)
                shotgun_sound.play() # play shoot sound when shooting cure
                allsprites.add(cure)
                cures.add(cure)
            Cure.special_cure_count -= 1
            if Cure.special_cure_count == 0:
                self.Normal = True
                self.Shotgun = False

        # Shoot in Pierce Mode if Pierce Mode is active
        elif self.Pierce == True: 
            #print(Cure.special_cure_count)
            cure = Cure(self.rect.centerx, self.rect.top)
            cure.speedx = 0
            cure.cure_health = 20 # Pierce bullet have 20 HP
            allsprites.add(cure)
            cures.add(cure)
            Cure.special_cure_count -= 1
            if Cure.special_cure_count >= 0:
                rifle_sound.play()
            if Cure.special_cure_count == -1:
                self.Normal = True
                self.Pierce = False
                cure.cure_health = 1
                shoot_sound.play()
            
            
class Covid(pygame.sprite.Sprite):
    def __init__(self, speed, health, score, vertical_movement = False):
        pygame.sprite.Sprite.__init__(self)
        self.images = [pygame.image.load("covid19.png").convert_alpha(), 
                    pygame.image.load("speedy_covid19.png").convert_alpha(), 
                    pygame.image.load("big_covid19.png").convert_alpha()]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.score = score
        #self.radius = int(self.rect.width*.7/2)
        self.speedy = speed
        self.hp = health
        self.verticalmovement = vertical_movement # variable for determine if covid can move vertically
        self.covidType() # Set Covid Type by their stats 
        self.reSpawn()

    def reSpawn(self):
        self.rect.x = random.randrange(WIDTH-self.rect.width)
        self.rect.y = random.randrange(-200,-50)
        self.speedx = random.randint(3, 6)
        self.count = random.randrange(0, 100)

    # Function for determine covid type by their stats
    def covidType(self): 
        if self.speedy >= 5:
            self.image = self.images[1]
        elif self.speedy < 5 and self.hp <= 2:
            self.image = self.images[0]
        elif self.hp >= 10 and self.speedy <= 3:
            self.image = self.images[2]
            self.image = pygame.transform.smoothscale(self.image, (100, 100))
            self.rect = self.image.get_rect()

    def update(self):
        #self.rect.x += self.speedx
        #print(self.count)
        self.rect.y += self.speedy
        # Moving randomly in x axis
        if self.verticalmovement == True:
            if self.count <= 50:
                self.rect.x += self.speedx
                self.count += 2
            elif self.count > 50:
                self.rect.x -= self.speedx
                self.count += 2
                if self.count >= 100:
                    self.count = 0
        if self.rect.top > HEIGHT+10:
            self.reSpawn()
            player.score -= 100 # player lose 100 score point if let covid respawn
        
        # Make covid can't move out of the screen
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

class Cure(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("cure.png").convert_alpha()
        self.image_orig = self.image
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.speedx = random.randrange(-2, 2) # Speed of cure cure in X axis
        self.last_update = pygame.time.get_ticks()
        self.cure_health = 1 # cure hp
        self.special_cure_count = 0 # variable for counting special cure usage

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx # Rotate cure from random value
        self.rotate()
        if self.rect.bottom < 0:
            self.kill()
        

    def rotate(self):
        now = pygame.time.get_ticks()
        # Make Pierce cure bigger
        if player.Pierce == True:
            self.image = pygame.transform.scale(self.image, (36, 68))
            old_center = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = old_center
        else:
            if now - self.last_update > 50:
                self.last_update = now
                self.rot = (self.rot + self.rot_speed) % 360
                new_image = pygame.transform.rotate(self.image_orig, self.rot)
                old_center = self.rect.center
                self.image = new_image
                self.rect = self.image.get_rect()
                self.rect.center = old_center
                #print("rotate")

# Class for collectible items
class Items(pygame.sprite.Sprite):
    def __init__(self, speed, itemNum):
        pygame.sprite.Sprite.__init__(self)
        self.images = [pygame.image.load("shotgun_box.png").convert_alpha(),
                    pygame.image.load("sniper_rifle_box.png").convert_alpha(),
                    pygame.image.load("star_box.png").convert_alpha(),
                    pygame.image.load("vaccine_box.png")]
        self.ItemNum = itemNum
        self.image = self.images[0]
        self.chooseimage()
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect()
        self.speedy = speed
        self.reSpawn()

    # Determine item type
    def chooseimage(self):
        if self.ItemNum == 1:
            self.image = self.images[0]
        elif self.ItemNum == 2:
            self.image = self.images[1]
        elif self.ItemNum == 3:
            self.image = self.images[2]
        elif self.ItemNum == 4:
            self.image = self.images[3]

    # Effect for each collectible items
    def collected_item(self):
        if self.ItemNum == 1:
            player.Normal = False
            player.Pierce = False
            player.Shotgun = True
            Cure.special_cure_count = 3
        elif self.ItemNum == 2:
            player.Normal = False
            player.Shotgun = False
            player.Pierce = True
            Cure.special_cure_count = 2
        elif self.ItemNum == 3:
            player.Unlimited = True
            player.Normal = True
            player.Shotgun = False
            player.Pierce = False
        elif self.ItemNum == 4:
            if player.life <= 80:
                player.life += 20
            if player.life == 90:
                player.life += 10

    def reSpawn(self):
        self.rect.x = random.randrange(WIDTH-self.rect.width)
        self.rect.y = random.randrange(-200,-50)
        self.speedx = random.randint(1, 5)
        self.count = random.randrange(0, 100)      

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT+10:
            self.reSpawn()

allsprites = pygame.sprite.Group()
covids = pygame.sprite.Group()
cures = pygame.sprite.Group()
items = pygame.sprite.Group()

cure_reload_timer = 0 # Time counter for reload 1 cure in to the magazine
max_cure_in_magazine = 15 # Max cure in the magazine
cure_in_magazine = max_cure_in_magazine # set cure in magazine to max before game start

player = Player()
allsprites.add(player)
global stage_level
stage_level = 0 

def stage():
    global stage_level
    global percentage
    if stage_level == 0:
        allsprites.empty()
        covids.empty()
        cures.empty()
        allsprites.add(player)
    if len(covids) == 0 and stage_level < 10: # if all the covids are killed increase stage level
        covids.empty()
        cures.empty()
        for item in items: # delete all the items when change stage to prevent player from stacking items
            item.kill()
        items.empty()
        stage_level += 1
        # Item distribution section randomize items for each stages and have a percentage for drop chances shotgun have 40% drop chnace, sniper 40%, ultimate_mode 20%
        if stage_level <= 5: # stage 1-5 only have 1 item per stage random
            percentage = random.randint(1, 100)
            if (percentage >= 1) and (percentage < 40):
                item = Items(3, 1)
                allsprites.add(item)
                items.add(item)
            elif (percentage >= 40) and (percentage < 80):
                item = Items(3, 2)
                allsprites.add(item)
                items.add(item)
            elif (percentage >= 80) and (percentage <= 100):
                item = Items(3, 3)
                allsprites.add(item)
                items.add(item)
        elif stage_level > 5 and stage_level < 10: # stage 6-9 have 2 items random
            for i in range(2):
                percentage = random.randint(1, 100)
                if (percentage >= 1) and (percentage < 40):
                    item = Items(3, 1)
                    allsprites.add(item)
                    items.add(item)
                elif (percentage >= 40) and (percentage < 80):
                    item = Items(3, 2)
                    allsprites.add(item)
                    items.add(item)
                elif (percentage >= 80) and (percentage <= 100):
                    item = Items(3, 3)
                    allsprites.add(item)
                    items.add(item)
        elif stage_level == 10: # last stage have 3 items random
            for i in range(3):
                percentage = random.randint(1, 100)
                if (percentage >= 1) and (percentage < 40):
                    item = Items(3, 1)
                    allsprites.add(item)
                    items.add(item)
                elif (percentage >= 40) and (percentage < 80):
                    item = Items(3, 2)
                    allsprites.add(item)
                    items.add(item)
                elif (percentage >= 80) and (percentage <= 100):
                    item = Items(3, 3)
                    allsprites.add(item)
                    items.add(item)
        # Item handler for vaccine that increase player hp every 2 stages
        if stage_level % 2 == 0:
            item = Items(3, 4)
            allsprites.add(item)
            items.add(item)
        # Stages handler for managing covids in each stages
        if stage_level == 1:
            for i in range(10):
                c = Covid(random.randrange(1, 3), 2, 100)
                allsprites.add(c)
                covids.add(c)
        elif stage_level == 2:
            for i in range(15):
                c = Covid(random.randrange(1, 3), 2, 100)
                allsprites.add(c)
                covids.add(c)
        elif stage_level == 3:
            for i in range(10):
                c = Covid(random.randrange(1, 3), 2, 100)
                allsprites.add(c)
                covids.add(c)
            for i in range(3):
                c = Covid(5, 1, 200, True)
                allsprites.add(c)
                covids.add(c)
        elif stage_level == 4:
            for i in range(5):
                c = Covid(random.randrange(5, 8), 1, 200, True)
                allsprites.add(c)
                covids.add(c)
        elif stage_level == 5:
            for i in range(1):
                c = Covid(1, 20, 500)
                allsprites.add(c)
                covids.add(c)
        elif stage_level == 6:
            for i in range(5):
                c = Covid(random.randrange(1, 3), 2, 100)
                allsprites.add(c)
                covids.add(c)
            for i in range(5):
                c = Covid(random.randrange(5, 8), 1, 200, True)
                allsprites.add(c)
                covids.add(c)
            for i in range(1):
                c = Covid(1, 20, 500)
                allsprites.add(c)
                covids.add(c)
        elif stage_level == 7:
            for i in range(8):
                c = Covid(random.randrange(5, 8), 1, 200, True)
                allsprites.add(c)
                covids.add(c)
            for i in range(2):
                c = Covid(1, 20, 500)
                allsprites.add(c)
                covids.add(c)
        elif stage_level == 8:
            for i in range(12):
                c = Covid(random.randrange(5, 8), 1, 200, True)
                allsprites.add(c)
                covids.add(c)
        elif stage_level == 9:
            for i in range(5):
                c = Covid(1, 20, 500)
                allsprites.add(c)
                covids.add(c)
        elif stage_level == 10:
            for i in range(20):
                c = Covid(15, 1, 300, True)
                allsprites.add(c)
                covids.add(c)
            for i in range(1):
                c = Covid(1, 100, 5000)
                allsprites.add(c)
                covids.add(c)
        

time_cnt = 600


while running:
    clock.tick(FPS)
    stage()
    #print(len(covids))

    current_time = pygame.time.get_ticks() # check current time
    # unable unlimit mode if unlimit mode time is out
    if current_time >= ultimate_mode_endTime:
        player.Unlimited = False
    
    # reload full magazine
    if current_time >= reload_fullMag and reloading == True:
        cure_in_magazine += 15
        reload_sound.play()
        reloading = False

#input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = 0
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.speedx = -6
            if event.key == pygame.K_RIGHT:
                player.speedx = 6
            if (event.key == pygame.K_SPACE) and (player.life > 0) and (cure_in_magazine > 0):
                player.shoot()
                cure_in_magazine -= 1
                # unlimit mode
                if player.Unlimited == True:
                    cure_in_magazine += 1
                # full reload when cure in magazine = 0
                if cure_in_magazine == 0 and reloading == False:
                    reloading = True
                    full_reload_sound.play()
                    reload_fullMag = current_time + reload_fullMagTime
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.speedx = 0
            if event.key == pygame.K_RIGHT:
                player.speedx = 0
            if (event.key == pygame.K_RETURN) and (player.life <= 0):
                player.life = 100
                player.score = 0
                stage_level = 0
                stage()


    # Loop for reloading cure in to the magazine
    if cure_in_magazine < max_cure_in_magazine and cure_in_magazine != 0:
        cure_reload_timer += 2
        #print(cure_reload_timer)
        if cure_reload_timer >= 100:
            cure_in_magazine += 1
            reload_sound.play()
            cure_reload_timer = 0

#process
    allsprites.update()

    player_hit = pygame.sprite.spritecollide(player,covids, True, pygame.sprite.collide_circle)
    if player_hit: 
        player.life -= 10 # player lose 10 health when hit by covid
        boom_sound.play()
    for covid in covids:
        for cure in cures:
            cures_hits = pygame.sprite.collide_rect(covid, cure)
            if cures_hits:
                # print(covid.hp)
                cure.cure_health -= 1 # cure lose 1 hp if hit covid
                covid.hp -= 1 # covid lose 1 hp if cure hit
                if cure.cure_health <= 0:
                    # remove cure from the list if cure hp = 0
                    cure.kill()
        for covid in covids:
            if covid.hp <= 0:
                # remove covid from the list if covid hp = 0
                covid.kill()
                covid_die_sound.play()
                #Score handler
                player.score += covid.score

    # Collider for items
    for item in items:
        collect_item = pygame.sprite.collide_rect(item, player)
        if collect_item:
            item.collected_item()
            item.kill()
        if player.Unlimited == False:
            ultimate_mode_endTime = current_time + ultimate_modeTime

    if time_cnt > 0:
        time_cnt -= 1
    elif bg_offset > 0:
        time_cnt = 120
        bg_offset -= 1

#output
    #screen.fill((0,0,0))
    screen.blit(bg,(-0,-bg_offset))
    allsprites.draw(screen)
    for covid in covids:
        for cure in cures:
            cures_hit = pygame.sprite.collide_rect(covid, cure)
            if cures_hit:
                pygame.draw.circle(screen,(255,255,255),covid.rect.center,40)
    pygame.draw.rect(screen,(255, 0, 0),(10, 750, 100, 20)) # red bar behind player health
    pygame.draw.rect(screen,(0, 255, 0),(10, 750, player.life, 20)) # player health
    textScore = font.render("Score " + str(player.score), True, (0,255,255))
    cureInMagazineText = font.render(str(cure_in_magazine), True, (0, 255, 255)) # text for cure in magazine
    stage_levelText = font.render("Level " + str(stage_level), True, (0, 255, 255)) # show stage level
    if cure_in_magazine == 15:
        pygame.draw.rect(screen, (0, 255, 255), (480, 750, 100, 20)) # grey bar behind reload timer
    else:
        pygame.draw.rect(screen, (211, 211, 211), (480, 750, 100, 20)) # grey bar behind reload timer
    pygame.draw.rect(screen,(0, 255, 255), (480, 750, cure_reload_timer, 20)) # reload timer visualizer
    screen.blit(cureInMagazineText, (520, 700))
    screen.blit(textScore,((WIDTH-textScore.get_width())/2, 10))
    screen.blit(stage_levelText,(WIDTH - 120, 10))
    if player.life <= 0:
        textOver = font.render("Game Over ", True, (0,255,255))
        screen.blit(textOver,((WIDTH-textOver.get_width())/2, HEIGHT/2-50))
        textOver = font.render("Press Enter to try again", True, (0,255,255))
        screen.blit(textOver,((WIDTH-textOver.get_width())/2, HEIGHT/2))
    pygame.display.flip()

pygame.quit()
