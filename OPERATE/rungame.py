import pygame, time, sys, os
from datetime import datetime

# Global Variables
WHITE = (255, 255, 255)
RED = (232, 91, 81)
LIGHTBLUE = (173, 216, 230)

############
# Initiation
############

# Center the Game Application
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Initialize pygame + mixer for sound
pygame.init()
pygame.mixer.init()

# Initialize screen
size = (750, 750)
screen = pygame.display.set_mode(size)

# stores the width of the
# screen into a variable
width = screen.get_width()
  
# stores the height of the
# screen into a variable
height = screen.get_height()

pygame.display.set_caption("OPERATE!")

# Set background images
bg = pygame.image.load("./images/background_main.png").convert()
garbage_can = pygame.image.load("./images/garbage.png")

##########
# Objects
##########

# For Player Instance
class Tweezers(pygame.sprite.Sprite):    
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("./images/tweezers.png").convert_alpha()
        self.rect = self.image.get_rect()

# --- Movable Objects

# Parent Classes for Movable Objects
class Item(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

    def dispose(self):
        self.rect.x = 1500
        self.rect.y = 1500

class BrokenHeart(Item):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("./images/heart.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 325
        self.rect.y = 300

class Germ(Item):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("./images/germ.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 250
        self.rect.y = 100

class Butterfly(Item):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("./images/butterfly.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 325
        self.rect.y = 400

class Bone(Item):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("./images/bone.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 200
        self.rect.y = 275

# Menu Buttons
class PlayButton(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("./images/play.png")
        self.rect = self.image.get_rect()
        self.rect.x = 300
        self.rect.y = 300

class HelpButton(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("./images/help.png")
        self.rect = self.image.get_rect()
        self.rect.x = 300
        self.rect.y = 400

class ExitButton(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("./images/exit.png")
        self.rect = self.image.get_rect()
        self.rect.x = 635
        self.rect.y = 15

class QuitButton(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("./images/quit.png")
        self.rect = self.image.get_rect()
        self.rect.x = 300
        self.rect.y = 500

class RestartButton(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("./images/restart.png")
        self.rect = self.image.get_rect()
        self.rect.x = 300
        self.rect.y = 400

# set sprite groups
all_sprites_list = pygame.sprite.Group()
cavity_list = pygame.sprite.Group()
buttons_list = pygame.sprite.Group()

# Create + set objects
def setobject(object):
    obj = object()
    cavity_list.add(obj)
    all_sprites_list.add(obj)

# Create + set buttons
def setbutton(buttonobj):
    buttonobj = buttonobj()
    buttons_list.add(buttonobj)

    return buttonobj

play_button = setbutton(PlayButton)
help_button = setbutton(HelpButton)
exit_button = setbutton(ExitButton)
quit_button = setbutton(QuitButton)
restart_button = setbutton(RestartButton)

######
# Game
######

# Game states
main = 0
play = 1
rules = 2
quit = 3
restart_good = 4
restart_bad = 5

# Variables for game
done = False

clock = pygame.time.Clock()

def goodRestart(mouse, x, y):
    gamestate = restart_good
    pygame.mouse.set_visible(True)
    goodjob = pygame.image.load('./images/goodjob.png')
    screen.blit(goodjob, (150,25))

    screen.blit(restart_button.image, (restart_button.rect.x, restart_button.rect.y))

    screen.blit(quit_button.image, (quit_button.rect.x, quit_button.rect.y))

    # option to quit/restart
    if mouse == 1:
        if restart_button.rect.collidepoint(x, y) == True:
            gamestate = main
        elif quit_button.rect.collidepoint(x, y) == True:
            gamestate = quit
    
    return gamestate

def badRestart(mouse, x, y):
    gamestate = restart_bad
    pygame.mouse.set_visible(True)
    tryagain = pygame.image.load('./images/tryagain.png')
    screen.blit(tryagain, (150, 25))
    screen.blit(restart_button.image, (restart_button.rect.x, restart_button.rect.y))
    screen.blit(quit_button.image, (quit_button.rect.x, quit_button.rect.y))

    # option to quit/restart
    if mouse == 1:
        if restart_button.rect.collidepoint(x, y) == True:
            gamestate = main
        elif quit_button.rect.collidepoint(x, y) == True:
            gamestate = quit
    
    return gamestate


def playGame(bg, mouse, x, y):
    player = Tweezers()
    # Variables for game
    gamestate = play
    holding = False
    garbage = []
    total_health = 100
    health = 0
    running = True
    font = pygame.font.SysFont('Calibri', 20, True, False)

    # Items for game
    heart = setobject(BrokenHeart)
    germ = setobject(Germ)
    butterfly = setobject(Butterfly)
    bone = setobject(Bone)
    
    # Player instance
    pygame.mouse.set_visible(False)

    # Draw all sprites
    all_sprites_list.add(player)
    for x in all_sprites_list:
        print(x)
    print (len(cavity_list))
    print (len(all_sprites_list))
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
                sys.exit()
                
        # set background
        screen.fill(WHITE)
        screen.blit(bg,(0,0))
        screen.blit(garbage_can,(600,600))
        all_sprites_list.draw(screen)

        # Draw healthbar
        pygame.draw.rect(screen, RED, pygame.Rect(25, 25, total_health - health, 30))
        hp_heart = pygame.image.load('./images/health.png')
        screen.blit(hp_heart, (15, 15))

        # Decreasing health
        health += 0.01
        string = str(int(total_health - health))
        health_text = font.render(string,True,WHITE)
        screen.blit(health_text, (33, 35))

        # Set player   
        pos = pygame.mouse.get_pos()     
        player.rect.x = pos[0]
        player.rect.y = pos[1]

        blocks_hit_list = pygame.sprite.spritecollide(player, cavity_list, False)
                        
        # Logic to drag + drop single objects
        # Q to pick up, SPACE to drop
        for cavity in blocks_hit_list:
            if pygame.key.get_pressed()[pygame.K_q] and not holding:
                holding = True
                currentcavity = cavity

            if holding:
                currentcavity.rect.x = player.rect.x - 50
                currentcavity.rect.y = player.rect.y + 50
            
                if pygame.key.get_pressed()[pygame.K_SPACE]:
                    holding = False

                elif (currentcavity.rect.x in range(582,713)) and (currentcavity.rect.y in range(550,705)):
                    currentcavity.dispose()
                    garbage.append(currentcavity)
                    total_health += 10

                    check = pygame.image.load('./images/check.png')

                    text = font.render("+10",True,WHITE)

                    screen.blit(hp_heart, (15, 15))
                    screen.blit(text, (33, 35))

                    clock.tick(1)
                    screen.blit(check, (600,600))
                    pygame.display.update()
                    pygame.time.delay(1500)

                    holding = False

        if len(garbage) == len(cavity_list) and total_health - health > 0:
            #Stop counting
            total_health = 0
            
            bg_new = pygame.image.load('./images/background_success.png').convert()
            screen.blit(bg_new,(0,0))
            pygame.display.update()
            pygame.time.delay(1500)

            gamestate = restart_good

            # reset sprites for game restarts
            [cavity_list.remove(x) for x in cavity_list]
            [all_sprites_list.remove(y) for y in all_sprites_list]

            running = False

        elif (len(garbage) != len(cavity_list)) and total_health - health < 0:
            # remove remaining items
            for item in cavity_list:
                item.dispose()
            
            bg_new = pygame.image.load('./images/background_fail.png').convert()
            screen.blit(bg_new,(0,0))
            pygame.display.update()
            pygame.time.delay(1500)
            
            gamestate = restart_bad
            
            # reset lists for game restarts
            [cavity_list.remove(x) for x in cavity_list]
            [all_sprites_list.remove(y) for y in all_sprites_list]
                

            running = False
        
        pygame.display.flip()
        pygame.display.update()

    return gamestate

def helpMenu(mouse, mouseX, mouseY):
    gamestate = rules
    rules_sheet = pygame.image.load('./images/rules.png')
    screen.blit(rules_sheet, (0,0))
    
    # Exit button
    screen.blit(exit_button.image, (exit_button.rect.x, exit_button.rect.y))

    if mouse == 1:
        if exit_button.rect.collidepoint(mouseX, mouseY) == True:
            gamestate = main
    
    return gamestate

def mainMenu(mouse, mouseX, mouseY):  
    gamestate = main
    screen.fill(LIGHTBLUE)
    
    # Title
    title = pygame.image.load('./images/title.png')
    screen.blit(title, (150, 25))

    # Quit
    screen.blit(quit_button.image, (quit_button.rect.x, quit_button.rect.y))

    # Help
    screen.blit(help_button.image, (help_button.rect.x, help_button.rect.y))

    # Play
    screen.blit(play_button.image, (play_button.rect.x, play_button.rect.y))

    if mouse == 1:
        if play_button.rect.collidepoint(mouseX,mouseY) == True:        
            gamestate = play
        elif help_button.rect.collidepoint(mouseX,mouseY) == True:    
            gamestate = rules
        elif quit_button.rect.collidepoint(mouseX, mouseY) == True:
            pygame.quit()
            sys.exit()

    return gamestate

# Sound
#pygame.mixer.Sound.play(pygame.mixer.Sound("monitorsound.wav"), loops = -1)

gamestate = main
# Main Game Loop
while not done:
    pygame.init()
    mouse = x = y = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            done = True
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos          
            mouse = event.button
        
    if gamestate == main:   
        gamestate = mainMenu(mouse, x, y)
    elif gamestate == play:
        gamestate = playGame(bg, mouse, x, y)
    elif gamestate == rules:
        gamestate = helpMenu(mouse, x, y)
    elif gamestate == restart_good:
        gamestate = goodRestart(mouse, x, y)
    elif gamestate == restart_bad:
        gamestate = badRestart(mouse, x, y)
    else:
        pygame.quit()
        done = True
        sys.exit()

    pygame.display.flip()
    clock.tick(60) 
    pygame.display.update()

pygame.mixer.quit()
pygame.quit()

    