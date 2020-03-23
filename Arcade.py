#!usr/bin/env python3
# Galaxia by Spencer Mueller for CIS 343, Asssignemnt: Arcade Game in Python
# Simple Galaxia based game with 8 rows of 4 coumns of enemies that move side by side with a timer.
# Features include sound, a six bullet maximum, a 1up after 1000 points scored, and levels, not very
# exciting, but it should get harder with each level. There is a glitch in the middle so be careful
# and shoot those first, it has the potential to kill you no matter the live count for some reason

# import pygame for the game, random for some randomness and sys for the game
import pygame
import random
import sys


# Overlay class is a sprite that will define itself and create a 800 by 20 surface.
# It's rect will the the size of that surface and create a freesansbold font.
# It will then render the score lives and level.
class Overlay(pygame.sprite.Sprite):
    # initialize itself like a constructor
    def __init__(self):
        # create a new sprite that is itself
        pygame.sprite.Sprite.__init__(self)
        # create a new image that is an 800 by 20 pygame surface
        self.image = pygame.Surface((800, 20))
        # the rect is the size of the image
        self.rect = self.image.get_rect()
        # the font is freesans bold, 18 point
        self.font = pygame.font.Font('freesansbold.ttf', 18)
        # render the score lives and level
        self.render('Score: 0       Lives: 3      Level: 1')

    # render takes an overlay and a text and renders it on the screen
    def render(self, text):
        # the text is the text we input and I made it white
        self.text = self.font.render(text, True, (255, 255, 255))
        # blit will draw the image on the screen
        self.image.blit(self.text, self.rect)

    # draw takes in an overlay and a screen and draws it with blit
    def draw(self, screen):
        # draw the position with blit
        screen.blit(self.text, (0, 0))

    # update will update the score, lives, and level for the overlay
    def update(self, score, lives, level):
        # renders in the text Score, the actual score, Lives, the actual lives, and Level and the actual level
        self.render('Score: ' + str(score) + '     Lives: ' + str(lives) + '    Level: ' + str(level))


# Enemy class will create the enemies and load in their respective images
class Enemy(pygame.sprite.Sprite):
    # initializes itself
    def __init__(self):
        # Enemy is a sprite
        pygame.sprite.Sprite.__init__(self)
        # created 4 different possible images for the enemies
        self.imageNum = (random.randint(0, 3))
        # if the imagenum is 0, then load in the blue enemy
        if self.imageNum == 0:
            # image just loads in blue enemy
            self.image = pygame.image.load('Content\\enemyBlue1.png')
        # if the imagenum is 1, then load in the red enemy
        elif self.imageNum == 1:
            # image just loads in red enemy
            self.image = pygame.image.load('Content\\enemyRed1.png')
        # if the imagenum is 2, then load in the black enemy
        elif self.imageNum == 2:
            # image just loads in black enemy
            self.image = pygame.image.load('Content\\enemyBlack1.png')
        else:
            # image just loads in green enemy
            self.image = pygame.image.load('Content\\enemyGreen1.png')
        # the rect is equal to whatever the image is that was loaded in
        self.rect = self.image.get_rect()

    # draw will draw the enemy on the screen
    def draw(self, screen):
        # blit draws the image at the position rect
        screen.blit(self.image, self.rect)


# Projectile is a sprite that will come from the ship, fire a blue laser with a shoot noise
# and when it hits the top of the screen or an invader, it will disappear or hit the invader
# and make the invaderkilled noise
class Projectile(pygame.sprite.Sprite):
    # initializes itself like a constructor
    def __init__(self):
        # Projectile is a sprite
        pygame.sprite.Sprite.__init__(self)
        # image will be loaded in from laserBlue06 picture
        self.image = pygame.image.load('Content\\laserBlue06.png')
        # rect will be the size of the image
        self.rect = self.image.get_rect()
        # pew_sound is the sound of shooting from the ship
        self.pew_sound = pygame.mixer.Sound('Content\\shoot.wav')
        #  lowered the volume because it was extremely loud
        pygame.mixer.Sound.set_volume(self.pew_sound, .2)
        # die_sound is the sound of the invader dying
        self.die_sound = pygame.mixer.Sound('Content\\invaderkilled.wav')
        # lowered the volume of this as well because it's superrrr loud
        pygame.mixer.Sound.set_volume(self.die_sound, .2)

    # draw will draw the projectile onto the screen
    def draw(self, screen):
        # blit will draw the image at postion rect
        screen.blit(self.image, self.rect)

    # update will take in a game, ship, and enemys and update based on what it hits
    def update(self, game, ship, enemys):
        # if it hits the top of the screen or 0
        if self.rect.y == 0:
            # remove it from the group
            game.projectiles.remove(self)
            # decrease the numProjs count for max amount of projectiles
            game.numProjs -= 1
        # hitObject detects if the projectile hit any enemies
        hitObject = pygame.sprite.spritecollideany(self, enemys)
        # if an enemy is hit
        if hitObject:
            # play the enemy dying sound
            self.die_sound.play()
            # kill the hit object
            hitObject.kill()
            # increase the game score by 50 points per kill
            game.score += 50
            # also remove the projectile from the group
            game.projectiles.remove(self)
            # decrease max number of projectiles
            game.numProjs -= 1
            # if the score is divisible by 1000, thus every 1000 points, post a 1up event
            if game.score % 1000 == 0:
                # post 1up event that will give the player a 1up powerup
                pygame.event.post(game.put_One_Up_event)


# Enemyprojectile is the enemy projectile class that creates their projectiles
# and the sounds they should make on ship death and when they shoot
class Enemyprojectile(pygame.sprite.Sprite):
    # initializes itself like a constructor
    def __init__(self):
        # Enemyprojectile is a sprite
        pygame.sprite.Sprite.__init__(self)
        # image is what is loaded from enemyProj image
        self.image = pygame.image.load('Content\\enemyProj.png')
        # rect is the size of the image
        self.rect = self.image.get_rect()
        # enemy_sound is the sound of the enemies shooting, will trigger once per batch of enemies
        self.enemy_sound = pygame.mixer.Sound('Content\\enemyshoot.wav')
        # turned this way up because it was hard to hear
        pygame.mixer.Sound.set_volume(self.enemy_sound, 5)
        # death_sound is the sound the ship makes when you hit a projectile
        self.death_sound = pygame.mixer.Sound('Content\\shipdeath.wav')
        # turned this sound down because the pac man death wav file was loud
        pygame.mixer.Sound.set_volume(self.death_sound, .3)

    # draw will draw the enemy projectiles onto the screen
    def draw(self, screen):
        # blit will draw the image at position rect
        screen.blit(self.image, self.rect)

    # update will update the game when it touches the bottom of the screen
    def update(self, game):
        # if an enemy projectile touches the bottom of the screen or 800
        if self.rect.y == 800:
            # remove it from the group
            game.enemyProjs.remove(self)


# Ship will draw the ship from the playerShip2_blue image and update it when it collects
# 1ups and when it hits an enemy projectile
class Ship(pygame.sprite.Sprite):
    # initializes itself like a constructor
    def __init__(self):
        # Ship is a sprite
        pygame.sprite.Sprite.__init__(self)
        # image is loaded from the blue ship image
        self.image = pygame.image.load('Content\\playerShip2_blue.png')
        # rect is the size of the image
        self.rect = self.image.get_rect()
        # set initial x position to 325 on screen
        self.rect.x = 325
        # set initial y position to 450 on screen aka center
        self.rect.y = 450

    # draw will draw the ship on the screen
    def draw(self, screen):
        # blit will draw image at position rect
        screen.blit(self.image, self.rect)

    # update will take in a game, oneUps group and enemyProjs group
    def update(self, game, oneUps, enemyProjs):
        # hitObject2 is when the ship grabs the oneUp
        hitObject2 = pygame.sprite.spritecollideany(self, oneUps)
        # when a oneUp is collected
        if hitObject2:
            # post a oneUp event to the game's event pool
            pygame.event.post(game.one_Up_event)
            # "kill" the oneUp aka get rid of it
            hitObject2.kill()
        # hitObject3 is when the ship hits an enemy projectile
        hitObject3 = pygame.sprite.spritecollideany(self, enemyProjs)
        # when an enemy projectile is hit
        if hitObject3:
            # remove the ship from the group
            game.ships.remove(self)
            # post a new life event to the game's event pool
            pygame.event.post(game.new_life_event)


# Powerup will draw the 1up powerup from the 1up image and create the
# sound for collecting which is a mario 1up sound wav
class Powerup(pygame.sprite.Sprite):
    # initializes itself like a constructor
    def __init__(self):
        # Powerup is a sprite
        pygame.sprite.Sprite.__init__(self)
        # image is loaded from 1up image
        self.image = pygame.image.load('Content\\1up.png')
        # rect is the size of the image
        self.rect = self.image.get_rect()
        # initial x position is 100 due to only being able to move ship horizontal
        self.rect.x = 100
        # intial y position is 450 due to only being able to move ship horizontal
        self.rect.y = 450
        # oneUp_sound is loaded from 1up mario wav
        self.oneUp_sound = pygame.mixer.Sound('Content\\1up.wav')
        # turned the volume down because it was a tad loud
        pygame.mixer.Sound.set_volume(self.oneUp_sound, .5)

    # draw will draw the powerup on the screen
    def draw(self, screen):
        # blit will draw image at position rect
        screen.blit(self.image, self.rect)


# Game is the powerhouse and controls everything that happens and what to do if an event happens.
# It also calls almost all the defined functions and creates most of the background and background music.
class Game:
    # initializes itself like a constructor
    def __init__(self):
        # initializes pygame
        pygame.init()
        # pygame key is set on repeat
        pygame.key.set_repeat(50)
        # the mixer loads in my music loop wav
        pygame.mixer.music.load('Content\\musicloop.wav')
        # volume is turned down due to it being loud
        pygame.mixer.music.set_volume(.4)
        # it is also set on repeat for the duration of the game
        pygame.mixer.music.play(-1)
        # a timer is set so that every 800 milliseconds the enemies move side to side
        pygame.time.set_timer(pygame.USEREVENT + 2, 800)
        # a timer is also set for the enemies to shoot every 4.5 seconds
        pygame.time.set_timer(pygame.USEREVENT + 5, 4500)
        # self i for USEREVENT + 2
        self.i = 0
        # self j for the for loop to create enemies
        self.j = 0
        # self k also fro the for loop to create enemies
        self.k = 0
        # numProjs to make sure the max is 6 at a time
        self.numProjs = 0
        # starts the game clock
        self.clock = pygame.time.Clock()
        # screen is set to display a 800 by 600 box
        self.screen = pygame.display.set_mode((800, 600))
        # background is loaded in from my background image
        self.background = pygame.image.load('Content\\background.png')
        # caption is set to "Galaxia
        pygame.display.set_caption("Galaxia")
        # icon is set to a blue enemy
        self.icon = pygame.image.load('Content\\enemyBlue1.png')
        # display the icon on the program
        pygame.display.set_icon(self.icon)
        # create a new oneUp powerup
        self.oneUp = Powerup()
        # create a new projectile
        self.projectile = Projectile()
        # create a new enemy projectile
        self.enemyProj = Enemyprojectile()
        # create a new overlay
        self.overlay = Overlay()
        # set new life event to USEREVENT + 1
        self.new_life_event = pygame.event.Event(pygame.USEREVENT + 1)
        # set 1up event to USEREVENT + 3
        self.one_Up_event = pygame.event.Event(pygame.USEREVENT + 3)
        # set put 1up event event to USEREVENT + 4
        self.put_One_Up_event = pygame.event.Event(pygame.USEREVENT + 4)
        # the screen blit with the background
        self.screen.blit(self.background, (0, 0))
        # create a new ships group
        self.ships = pygame.sprite.Group()
        # add a new ship to the ships group
        self.ships.add(Ship())
        # create a new enemyProjs group
        self.enemyProjs = pygame.sprite.Group()
        # create a new enemys group
        self.enemys = pygame.sprite.Group()
        # create a new projectiles group
        self.projectiles = pygame.sprite.Group()
        # create a new oneUps group
        self.oneUps = pygame.sprite.Group()
        # set read to true for ship
        self.ready = True
        # set score to 0
        self.score = 0
        # set lives to 3
        self.lives = 3
        # set level to 1
        self.level = 1
        # create a row of 8 enemies
        for j in range(8):
            # make 4 columns of 8 enemies
            for k in range(4):
                # create a new enemy
                enemy = Enemy()
                # the enemy's x is positioned at j * 100 + an offset of 20 from the edge
                enemy.rect.x = j * 100 + 20
                # the enemy's y is positioned at k * 60 + an offset of 60 from the top
                enemy.rect.y = k * 60 + 60
                # add that enemy to the enemys group
                self.enemys.add(enemy)

    # run will then create the while loop that runs the game and continuously draws things on the screen
    # It also updates everything such as the ship or projectiles moving up, down, left, and right.
    def run(self):
        # done is set to false for the while loop
        self.done = False
        # while done is false
        while not self.done:
            # blit the background at 0, 0
            self.screen.blit(self.background, (0, 0))
            # if the enemys group is empty go to the next level
            if len(self.enemys) == 0:
                # increment the level
                self.level += 1
                # row of 8 enemies
                for j in range(8):
                    # 4 columns of 8 enemies
                    for k in range(4):
                        # create a new enemy
                        enemy = Enemy()
                        # the enemy's x is positioned at j * 100 + an offset of 20 from the edge
                        enemy.rect.x = j * 100 + 20
                        # the enemy's y is positioned at k * 60 + an offset of 60 from the top
                        enemy.rect.y = k * 60 + 60
                        # add that enemy to the enemys group
                        self.enemys.add(enemy)
            # for any such event gotten from the game
            for event in pygame.event.get():
                # if the event is USEREVENT + 5
                if event.type == pygame.USEREVENT + 5:
                    # play the enemy projectile sound
                    self.enemyProj.enemy_sound.play()
                    # for x in the enemys group
                    for x in self.enemys:
                        # selection is chosen by j times k mod 11
                        self.selection = ((self.j * self.k) % 11)
                        # this minus the level should create various difficulties of enemy projectiles
                        if (self.selection - self.level) == 0:
                            # create anew enemy projectile
                            enemyProj = Enemyprojectile()
                            # the x position is the enemy position + 18
                            enemyProj.rect.x = x.rect.x + 18
                            # the y position is the enemy position + 35
                            enemyProj.rect.y = x.rect.y + 35
                            # add that enemy projectile to the enemyProjs group
                            self.enemyProjs.add(enemyProj)
                        # if j is 5, set it back to 0
                        if self.j == 5:
                            # set j back to 0
                            self.j = 0
                        # if k is 4, set it back to 0 also
                        if self.k == 4:
                            # set k back to 0
                            self.k = 0
                        # increment j
                        self.j += 1
                        # increment k
                        self.k += 1

                #  if the event is a put a1up event
                if event.type == self.put_One_Up_event.type:
                    # create a new 1up
                    oneUp = Powerup()
                    # add it to the oneUps group
                    self.oneUps.add(oneUp)

                # if the event is a 1up event
                if event.type == self.one_Up_event.type:
                    # 1up is collected, increment lives by 1
                    self.lives += 1
                    # play the 1up sound
                    self.oneUp.oneUp_sound.play()

                # if the event is a new life event
                if event.type == self.new_life_event.type:
                    # play the ship death sound
                    self.enemyProj.death_sound.play()
                    # decrement the lives
                    self.lives -= 1
                    # if the lives are still above 0
                    if self.lives > 0:
                        # make a new ship
                        ship = Ship()
                        # add the ship to the Ships group
                        self.ships.add(ship)
                        # set ready to true for player to be ready for new life
                        self.ready = True
                    # if all out of lives
                    else:
                        # quit the game by calling the quit event
                        pygame.quit()
                        # exit the system gracefully
                        sys.exit(0)
                # if the event is quit
                if event.type == pygame.QUIT:
                    # end the while loop
                    self.done = True
                # if the event is a key press
                if event.type == pygame.KEYDOWN:
                    # if the key press is left
                    if event.key == pygame.K_LEFT:
                        # move the ship at sprite 0 left 10
                        self.ships.sprites()[0].rect.x -= 10
                        # if the ship is less than 0, move it back to 0
                        if self.ships.sprites()[0].rect.x <= 0:
                            # stop at edge if at the edge
                            self.ships.sprites()[0].rect.x= 0
                    # if the key press is right
                    if event.key == pygame.K_RIGHT:
                        # move the ship at sprite 0 right 10
                        self.ships.sprites()[0].rect.x += 10
                        # if the ship is greater tan 690, move it back to 690
                        if self.ships.sprites()[0].rect.x >= 690:
                            # stop at edge if at the edge
                            self.ships.sprites()[0].rect.x = 690
                    # if the key press is the space bar
                    if event.key == pygame.K_SPACE:
                        # if the number of projectiles is less than 6
                        if self.numProjs <= 5:
                            # create a new projectile
                            projectile = Projectile()
                            # increment the number of projectiles1
                            self.numProjs += 1
                            # projectile rect at x is the ship's rect at x + 50
                            projectile.rect.x = self.ships.sprites()[0].rect.x + 50
                            # projectile rect at y is the ship's rect at y + 50
                            projectile.rect.y = self.ships.sprites()[0].rect.y - 50
                            # play the pew pew sound
                            self.projectile.pew_sound.play()
                            # add that projectile to the projectiles group
                            self.projectiles.add(projectile)
                        # Otherwise let the user know they're at the max projectile count
                        else:
                            # print message to user
                            print("Can't have more than 6 projectiles at a time")
                # if the event is USEREVENT + 2 which is the 800 millisecond timer
                if event.type == pygame.USEREVENT + 2:
                    # if i is 0
                    if self.i == 0:
                        # move the enemies right 10
                        for x in self.enemys:
                            # move right 10
                            x.rect.x += 10
                    # if i is 1
                    if self.i == 1:
                        # move the enemies left 10
                        for x in self.enemys:
                            # move left 10
                            x.rect.x -= 10
                    # if is 2
                    if self.i == 2:
                        # move the enemies left 10
                        for x in self.enemys:
                            # move left 10
                            x.rect.x -= 10

                    # if i is 3
                    if self.i == 3:
                        # move the enemies right 10
                        for x in self.enemys:
                            # move right 10
                            x.rect.x += 10
                    # if i is 4
                    if self.i == 4:
                        # move the enemies right 10
                        for x in self.enemys:
                            # move right 10
                            x.rect.x += 10
                        # set i back to 0
                        self.i = 0
                    # increment i
                    self.i += 1
            # call update on enemyProjs group
            self.enemyProjs.update(self)
            # call update on projectiles group
            self.projectiles.update(self, self.ships, self.enemys)
            # call update on ships group
            self.ships.update(self, self.oneUps, self.enemyProjs)
            # call update on overlay
            self.overlay.update(self.score, self.lives, self.level)
            # draw each enemyProj in the enemyProjs group
            for w in self.enemyProjs:
                # draw w to the screen
                w.draw(self.screen)
                # enemy projectiles will travel down on the y axis
                w.rect.y += 1
            # draw each enemy in the enemys group
            for x in self.enemys:
                # draw x to the screen
                x.draw(self.screen)
            # draw each oneUp in the oneUps group
            for y in self.oneUps:
                # draw y to the screen
                y.draw(self.screen)
            # draw each enemy projectile in the projectiles group
            for z in self.projectiles:
                # draw z to the screen
                z.draw(self.screen)
                # projectiles will travel down on the y axis
                z.rect.y -= 1
            # draw the ships group to the screen
            self.ships.draw(self.screen)
            # draw the overlay to the screen
            self.overlay.draw(self.screen)
            # flip the display
            pygame.display.flip()
            # set the clock tick to 60
            self.clock.tick(60)


# if statement checks for the main function, which is true
if __name__ == "__main__":
    # creates a new game
    game = Game()
    # calls run and starts the game
    game.run()



