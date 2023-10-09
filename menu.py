import pygame
import colours
import storage
colourdict = colours.getcolours()
maroon = colourdict["maroon"]
rosybrown = colourdict["rosybrown"]

def mainmenu(screen):

    choice = False

    titlefont = pygame.font.SysFont("times new roman", 100)
    buttonfont = pygame.font.SysFont("times new roman", 40)

    title = titlefont.render("HYPOGEAL", True, maroon)
    titlerect = title.get_rect(topleft=(200,10))
    
    if storage.checkplayer() == True:
        loadgame = buttonfont.render("LOAD GAME", True, maroon)
        loadgamerect = loadgame.get_rect(topleft=(350,200))

    newgame = buttonfont.render("NEW GAME", True, maroon)
    newgamerect = newgame.get_rect(topleft=(350,300))
    
    quitgame = buttonfont.render("QUIT GAME", True, maroon)
    quitgamerect = quitgame.get_rect(topleft=(350,400))

    while choice == False:
        for event in pygame.event.get():
            screen.blit(title,titlerect)
            screen.blit(newgame,newgamerect)
            if storage.checkplayer():
                screen.blit(loadgame,loadgamerect)
            screen.blit(quitgame,quitgamerect)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if newgamerect.collidepoint(event.pos):
                    return "new"
                elif storage.checkplayer() and loadgamerect.collidepoint(event.pos):
                    return "load"
                elif quitgamerect.collidepoint(event.pos):
                    return "quit"
            
            if newgamerect.collidepoint(pygame.mouse.get_pos()):
                newgame = buttonfont.render("NEW GAME", True, rosybrown)
            else:
                newgame = buttonfont.render("NEW GAME", True, maroon)
            
            if storage.checkplayer() == True:
                if loadgamerect.collidepoint(pygame.mouse.get_pos()):
                    loadgame = buttonfont.render("LOAD GAME", True, rosybrown)
                else:
                    loadgame = buttonfont.render("LOAD GAME", True, maroon)
                
            if quitgamerect.collidepoint(pygame.mouse.get_pos()):
                quitgame = buttonfont.render("QUIT GAME", True, rosybrown)
            else:
                quitgame = buttonfont.render("QUIT GAME", True, maroon)

        pygame.display.update()
