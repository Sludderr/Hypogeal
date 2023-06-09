import pygame
import sys

width = 512
height = 448

white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0) 
blue = (0, 0, 130) 


playerposx = 0
playerposy = 0
playerpos = (playerposx, playerposy)
playervel = 16

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

pygame.display.flip()
pygame.display.set_caption('Test')
font = pygame.font.SysFont("timesnewroman", 16)
text = font.render('@', True, white)
pygame.display.flip()

running = True

while running:

    pygame.time.delay(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_KP4]:
        playerposx -= playervel
        print("LEFT")
    if keys[pygame.K_KP6]:
        playerposx += playervel
        print("RIGHT")
    if keys[pygame.K_KP8]:
        playerposy -= playervel
        print("UP")
    if keys[pygame.K_KP2]:
        playerposy += playervel
        print("DOWN")
    if keys[pygame.K_KP7]:
        playerposy -= playervel
        playerposx -= playervel
        print("UP_LEFT")
    if keys[pygame.K_KP9]:
        playerposy -= playervel
        playerposx += playervel
        print("UP_LEFT")
    if keys[pygame.K_KP1]:
        playerposy += playervel
        playerposx -= playervel
        print("UP_LEFT")
    if keys[pygame.K_KP3]:
        playerposy += playervel
        playerposx += playervel
        print("UP_LEFT")
    

    playerpos = (playerposx, playerposy)

    screen.fill((0,0,0))
    screen.blit(text, playerpos)
    pygame.display.update()
pygame.quit()
