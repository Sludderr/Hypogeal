import pygame
import sys
import entities

width = 1024
height = 896

white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0) 
blue = (0, 0, 130) 

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

pygame.display.flip()
pygame.display.set_caption('Test')
font = pygame.font.SysFont("timesnewroman", 16)
text = font.render('@', True, white)
pygame.display.flip()

player = entities.Entity("Player", 0, 0)


running = True

while running:

    pygame.time.delay(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_KP4]:
        player.x -= player.speed
        print("LEFT")
    if keys[pygame.K_KP6]:
        player.x += player.speed
        print("RIGHT")
    if keys[pygame.K_KP8]:
        player.y -= player.speed
        print("UP")
    if keys[pygame.K_KP2]:
        player.y += player.speed
        print("DOWN")
    if keys[pygame.K_KP7]:
        player.y -= player.speed
        player.x -= player.speed
        print("UP_LEFT")
    if keys[pygame.K_KP9]:
        player.y -= player.speed
        player.x += player.speed
        print("UP_LEFT")
    if keys[pygame.K_KP1]:
        player.y += player.speed
        player.x -= player.speed
        print("UP_LEFT")
    if keys[pygame.K_KP3]:
        player.y += player.speed
        player.x += player.speed
        print("UP_LEFT")
    

    playerpos = (player.x, player.y)

    screen.fill((0,0,0))
    screen.blit(text, playerpos)
    pygame.display.update()
pygame.quit()
