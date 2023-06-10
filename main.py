import pygame
import entities
import renderer
import input_handler

width = 64
height = 56

screenwidth = width * 16
screenheight = height * 16

white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((screenwidth, screenheight))
clock = pygame.time.Clock()

pygame.display.set_caption('Test')
font = pygame.font.SysFont("timesnewroman", 16)
pygame.display.flip()

player = entities.create_entity("Player", 0, 0, "@", white)
dummy = entities.create_entity("Dummy", 4, 4, "#", green)

running = True

while running:
    pygame.time.delay(100)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    input_handler.handle(player)
    
    renderer.update(screen, font)
    
pygame.quit()
