import pygame
import colours
import storage
import renderer
import gamemap
import entities

colourdict = colours.getcolours()
maroon = colourdict["maroon"]
rosybrown = colourdict["rosybrown"]
white = colourdict["white"]

invx = 20
invy = 15

spellsx = 20
spellsy = 15

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


def deathscreen():
    screen = pygame.display.get_surface()
    choice = False
    storage.clearstorage()
    titlefont = pygame.font.SysFont("times new roman", 100)
    buttonfont = pygame.font.SysFont("times new roman", 40)

    title = titlefont.render("YOU ARE DEAD", True, maroon)
    titlerect = title.get_rect(topleft=(200,10))

    quitgame = buttonfont.render("QUIT GAME", True, maroon)
    quitgamerect = quitgame.get_rect(topleft=(350,400))

    while choice == False:
        screen.blit(title,titlerect)
        screen.blit(quitgame,quitgamerect)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if quitgamerect.collidepoint(event.pos):
                    return 50
            if quitgamerect.collidepoint(pygame.mouse.get_pos()):
                quitgame = buttonfont.render("QUIT GAME", True, rosybrown)
            else:
                quitgame = buttonfont.render("QUIT GAME", True, maroon)

        pygame.display.update()


class invitem():
    def __init__(self,item,x,y):
        self.itemfont = pygame.font.SysFont("times new roman", 30)
        self.item = item
        self.itemobject = self.itemfont.render(item.char, True, item.colour)
        self.itemrect = self.itemobject.get_rect(topleft=(50*16+x*32, 42+y*32))
        self.selecting = False

class spellslot():
    def __init__(self,spell,x,y):
        self.spellfont = pygame.font.SysFont("times new roman", 30)
        self.spell = spell
        self.spellobject = self.spellfont.render(spell.char, True, spell.colour)
        self.spellrect = self.spellobject.get_rect(topleft=(50*16+x*32, 532+y*32))
        self.selecting = False

inv = [[None for x in range(invx)] for y in range(invy)]

def inventorymenu(screen):
    for y in range(invy):
        for x in range(invx):
            if inv[y][x] != None:
                screen.blit(inv[y][x].itemobject,inv[y][x].itemrect)
            if spells[y][x] != None:
                screen.blit(spells[y][x].spellobject,spells[y][x].spellrect)
    pygame.display.update()
    
def interface():
    if entities.getplayer().inventory == []:
        return 0
    screen = pygame.display.get_surface()
    print("hello! you're in the inventory interface now!")
    while True:
        event = pygame.event.get()
        for y in range(invy):
            for x in range(invx):
                if inv[y][x] != None:
                    mousepos = pygame.mouse.get_pos()
                    
                    if inv[y][x].itemrect.collidepoint(mousepos):               
                        if inv[y][x].selecting == False:
                            inv[y][x].itemobject = inv[y][x].itemfont.render(inv[y][x].item.char, True, rosybrown)
                            screen.blit(inv[y][x].itemobject,inv[y][x].itemrect)
                            tooltip = pygame.font.SysFont("times new roman", 16).render(inv[y][x].item.name + " " + inv[y][x].item.description, True, white)
                            screen.blit(tooltip, (mousepos[0]+20,mousepos[1]+20))
                            inv[y][x].selecting = True
                            pygame.display.update()

                    elif inv[y][x].selecting == True:
                        inv[y][x].itemobject = inv[y][x].itemfont.render(inv[y][x].item.char, True, inv[y][x].item.colour)
                        renderer.update(pygame.display.get_surface(), pygame.font.SysFont("times new roman", 16), gamemap.getwidth(), gamemap.getheight())
                        screen.blit(inv[y][x].itemobject,inv[y][x].itemrect)
                        pygame.display.update()
                        inv[y][x].selecting = False
                        
                        
                    for currentevent in event:
                        if currentevent.type == pygame.MOUSEBUTTONDOWN:
                            if inv[y][x].itemrect.collidepoint(currentevent.pos):
                                if currentevent.button == 1:
                                    inv[y][x].itemobject = inv[y][x].itemfont.render(inv[y][x].item.char, True, inv[y][x].item.colour)
                                    screen.blit(inv[y][x].itemobject,inv[y][x].itemrect)
                                    pygame.display.update()
                                    inv[y][x].item.use()
                                    return 1
                                elif currentevent.button == 3:
                                    inv[y][x].itemobject = inv[y][x].itemfont.render(inv[y][x].item.char, True, inv[y][x].item.colour)
                                    screen.blit(inv[y][x].itemobject,inv[y][x].itemrect)
                                    pygame.display.update()
                                    inv[y][x].item.drop()
                                    return 1

        if pygame.key.get_pressed()[pygame.K_KP_PERIOD]:
            for y in range(invy):
                for x in range(invx):
                    if inv[y][x] != None:
                        inv[y][x].itemobject = inv[y][x].itemfont.render(inv[y][x].item.char, True, inv[y][x].item.colour)
            renderer.update(pygame.display.get_surface(), pygame.font.SysFont("times new roman", 16), gamemap.getwidth(), gamemap.getheight())
            return 0

spells = [[None for x in range(spellsx)] for y in range(spellsy)]

def spellinterface():
    screen = pygame.display.get_surface()
    print("hello! you're in the spell interface now!")
    while True:
        event = pygame.event.get()
        for y in range(spellsy):
            for x in range(spellsx):
                if spells[y][x] != None:
                    mousepos = pygame.mouse.get_pos()
                    
                    if spells[y][x].spellrect.collidepoint(mousepos):               
                        if spells[y][x].selecting == False:
                            spells[y][x].spellobject = spells[y][x].spellfont.render(spells[y][x].spell.char, True, rosybrown)
                            screen.blit(spells[y][x].spellobject,spells[y][x].spellrect)
                            tooltip = pygame.font.SysFont("times new roman", 16).render(spells[y][x].spell.name + " cooldown:" + str(spells[y][x].spell.timer), True, white)
                            screen.blit(tooltip, (mousepos[0]+20,mousepos[1]+20))
                            spells[y][x].selecting = True
                            pygame.display.update()

                    elif spells[y][x].selecting == True:
                        if spells[y][x].spell.timer == 0:
                            spells[y][x].spellobject = spells[y][x].spellfont.render(spells[y][x].spell.char, True, spells[y][x].spell.colour)
                        else:
                            spells[y][x].spellobject = spells[y][x].spellfont.render(spells[y][x].spell.char, True, white)
                        renderer.update(pygame.display.get_surface(), pygame.font.SysFont("times new roman", 16), gamemap.getwidth(), gamemap.getheight())
                        screen.blit(spells[y][x].spellobject,spells[y][x].spellrect)
                        pygame.display.update()
                        spells[y][x].selecting = False
                        
                        
                    for currentevent in event:
                        if currentevent.type == pygame.MOUSEBUTTONDOWN:
                            if spells[y][x].spellrect.collidepoint(currentevent.pos):
                                if currentevent.button == 1:
                                    if spells[y][x].spell.use() == 1:
                                        spells[y][x].spellobject = spells[y][x].spellfont.render(spells[y][x].spell.char, True, white)
                                        return 1
                                    else:
                                        return exit()

        if pygame.key.get_pressed()[pygame.K_KP_PERIOD]:
            return exit()

def exit():
    for y in range(spellsy):
        for x in range(spellsx):
            if spells[y][x] != None:
                if spells[y][x].spell.timer == 0:
                    spells[y][x].spellobject = spells[y][x].spellfont.render(spells[y][x].spell.char, True, spells[y][x].spell.colour)
                else:
                    spells[y][x].spellobject = spells[y][x].spellfont.render(spells[y][x].spell.char, True, white)
    renderer.update(pygame.display.get_surface(), pygame.font.SysFont("times new roman", 16), gamemap.getwidth(), gamemap.getheight())
    return 0

def addtoinv(item):
    for y in range(invy):
        for x in range(invx):
            if inv[y][x] == None:
                inv[y][x] = invitem(item,x,y)
                return True
    return False

def removefrominv(item):
    for y in range(invy):
        for x in range(invx):
            if inv[y][x] != None and inv[y][x].item == item:
                inv[y][x] = None
                renderer.update(pygame.display.get_surface(), pygame.font.SysFont("times new roman", 16), gamemap.getwidth(), gamemap.getheight())
                return True
    return False

def addtospells(spell, timer):
    for y in range(spellsy):
        for x in range(spellsx):
            if spells[y][x] == None:
                spells[y][x] = spellslot(spell,x,y)
                if timer != 0:
                    spells[y][x].spellobject = spells[y][x].spellfont.render(spells[y][x].spell.char, True, white)
                return True
    return False

def removefromspells(spell):
    for y in range(spellsy):
        for x in range(spellsx):
            if spells[y][x] != None and spells[y][x].spell == spell:
                spells[y][x] = None
                renderer.update(pygame.display.get_surface(), pygame.font.SysFont("times new roman", 16), gamemap.getwidth(), gamemap.getheight())
                return True
    return False

def updatecolour(spell):
    for y in range(spellsy):
        for x in range(spellsx):
            if spells[y][x] != None and spells[y][x].spell == spell:
                spells[y][x].spellobject = spells[y][x].spellfont.render(spell.char, True, spell.colour)
                renderer.update(pygame.display.get_surface(), pygame.font.SysFont("times new roman", 16), gamemap.getwidth(), gamemap.getheight())
