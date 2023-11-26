import pygame
import colours
import entities
import gamemap
import random
import turn_handler
import storage
import menu
import spells

width = 50
height = 50

screenwidth = width * 30
screenheight = height * 20

colourdict = colours.getcolours()
white = colourdict["white"]

# Initialise pygame and screen
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((screenwidth, screenheight))
pygame.display.set_icon(pygame.image.load("icon.png"))

pygame.display.set_caption('Hypogeal')
font = pygame.font.SysFont("timesnewroman", 16)
pygame.display.flip()

choice = menu.mainmenu(screen)

# Start player and procgen location

running = True

if choice == "new":
    # clear the storage and create new player, create new map
    storage.clearstorage()
    startx = random.randint(10, width-10)
    starty = random.randint(10, height-10)
    entities.deleteentities()
    player = entities.create_player("Player", startx, starty, 20, "@", white, 10)
    Map = gamemap.setup(width, height, startx, starty)
    Map[starty][startx].occupants.append(player)
    spells.givefirewall(0)

elif choice == "load":
    player = storage.loadall()
    if player.health > 0:
        startx = player.x
        starty = player.y
        Map = gamemap.getmap()
    Map[starty][startx].occupants.append(player)

elif choice == "quit":
    running = False

# Outer Gameloop. Always loops until game is entirely quit.
while running:
    # Call the turnhandler. This loops through every active entity and updates them.
    returncode = turn_handler.updateturns(entities.getentities())

    # Neatly closes pygame and process without crashing
    if returncode == 50:
        running = False

    pygame.time.delay(10)

# When gameloop ends quit pygame
pygame.quit()
