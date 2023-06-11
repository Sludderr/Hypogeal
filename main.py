import pygame
import colours
import entities
import renderer
import gamemap
import input_handler
import random

width = 60
height = 60

screenwidth = width * 16
screenheight = height * 16

colourdict = colours.getcolours() 

white = colourdict["white"]
black = colourdict["black"]
green = colourdict["green"]

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((screenwidth, screenheight))
clock = pygame.time.Clock()

pygame.display.set_caption('Hypogeal')
font = pygame.font.SysFont("timesnewroman", 16)
pygame.display.flip()

startx = random.randint(10, width-10)
starty = random.randint(10, height-10)

player = entities.create_entity("Player", startx, starty, "@", white)
dummy = entities.create_entity("Dummy", 4, 4, "#", green)


Map = gamemap.setup(width, height, startx, starty)

running = True

while running:
    pygame.time.delay(100)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    input_handler.handle(player)
    
    renderer.update(screen, font, width, height)
    
pygame.quit()
