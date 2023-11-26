entitylist = []
import pygame
import gamemap
import state
import input_handler
import random
import colours
import renderer
import menu
import spells
import astar
import math
import procgeneration

# import colours
colourdict = colours.getcolours() 
red = colourdict["red"]
lightblue = colourdict["lightblue"]
green = colourdict["green"]
olivedrab = colourdict["olivedrab"]
grey = colourdict["lightgrey"]

# Global list "entitylist" holds all active entities. It will be looped through every tick to update the state of each entity

# Base class "Entity".
class Entity():
    def __init__(self, name, x, y, health, char, colour, description):
        self.name = name
        self.x = x
        self.y = y
        self.health = health
        self.maxhealth = health
        self.char = char
        self.colour = colour
        self.speed = 1
        self.blocking = False # whether they block passing on the map
        self.sentient = False # if not sentient, they will not have their turn processed
        self.pickupable = False
        self.description = description
        
    def take_action(self):
        return 0
        
    def move(self,xoffset,yoffset):
      Map = gamemap.getmap()
      if detectcollision(self.x+xoffset, self.y+yoffset,Map) != True:
        # move the entity by the offset values
        Map[self.y][self.x].occupants.remove(self)
        self.x += xoffset
        self.y += yoffset
        Map[self.y][self.x].occupants.append(self)
        # optimisation where i was reupdating for every movement- only need to update at the start of the player turn
        return 1
      else:
        return 0
    
    def attack(self, target, damage, col):
        # apply damage to target and "flash" the attack colour. This works as some primitive animation to show when attacks have taken place
        target.health -= damage
        renderer.flash(target,col)
        
        if target.health <= -2 and target.name != "Player's corpse":
            print(target.name, " is destroyed!")
            player = getplayer()
            entitylist.remove(target)
            Map = gamemap.getmap()
            Map[target.y][target.x].occupants.remove(target)
            # method inside target that places random loot when its corpse is destroyed
            target.loot()
            gamemap.setmap(state.update_visibility(Map, player.x, player.y, gamemap.getwidth(), gamemap.getheight(),player.viewrestrict))
            return 2
        
        if target.health <= 0 and target.name != "Player's corpse":
            print(target.name, " is dead!")
            target.name = target.name + "'s corpse"
            target.speed = 0
            target.initiative = 0
            target.ap = 0
            target.char = "%"
        else:
            print(target.name, "'s health is now ", target.health)

        renderer.update(pygame.display.get_surface(),pygame.font.SysFont("timesnewroman", 16),gamemap.getwidth(),gamemap.getheight())
        return 1
    
    def heal(self,amount):
        self.health = min(self.health+amount, self.maxhealth)

    def use(self):
        print("I got used!")
        
    def drop(self):
        player = getplayer()
        player.inventory.remove(self)
        self.x = player.x
        self.y = player.y
        entitylist.insert(0,self)
        Map = gamemap.getmap()
        Map[player.y][player.x].occupants.append(self)
        menu.removefrominv(self)
    def loot(self):
        return


class Enemy(Entity):
    def __init__(self, name, x, y, health, char, colour,initiative, description):
        Entity.__init__(self, name, x, y, health, char, colour, description)
        self.initiative = initiative
        self.ap = random.randint(0,initiative)
        self.sentient = True
        self.blocking = True

    def take_action(self):
        player = getplayer()
        Map = gamemap.getmap()
        if distance(self.x, self.y, player.x, player.y) > 10 or self.health <= 0:
            return 1
        found,route = astar.astar(Map[self.y][self.x], Map[player.y][player.x], Map)
        if found == True and len(route) > 1:
            Map[self.y][self.x].occupants.remove(self)
            self.y = route[-2].y
            self.x = route[-2].x
            Map[self.y][self.x].occupants.append(self)
        elif found == True and len(route) <= 1:
            self.attack(player, 4, red)
            if player.health <= 0:
                if menu.deathscreen() == 50:
                    return 50
            

        gamemap.setmap(state.update_visibility(Map, player.x, player.y, gamemap.getwidth(), gamemap.getheight(),player.viewrestrict))
        return 1
    
class Player(Entity):
    def __init__(self, name, x, y, health, char, colour, initiative):
        Entity.__init__(self, name, x, y, health, char, colour, "It's you!")
        self.mana = 20
        self.maxmana = 20
        self.initiative = initiative
        self.ap = 0
        self.viewrestrict = 10
        self.sentient = True
        self.blocking = True
        self.inventory = []
        self.spell_list = []
        self.pickaxe = False
        self.mindamage = 1
        self.maxdamage = 2
        
    def take_action(self):
        # update map to show the movements of enemies and entities
        gamemap.setmap(state.update_visibility(gamemap.getmap(), self.x, self.y, gamemap.getwidth(), gamemap.getheight(),self.viewrestrict))
        renderer.update(pygame.display.get_surface(),pygame.font.SysFont("timesnewroman", 16),gamemap.getwidth(),gamemap.getheight())
        action = False
        while action != True:
            pygame.time.delay(100)
            pygame.event.wait()
            returncode = input_handler.handle(self)
            if returncode == 1:
                action = True
            elif returncode == 2:
                return 2
            elif returncode == 50:
                return 50
        spells.update_timers()
        return 1
        
    def move(self,xoffset,yoffset):
        Map = gamemap.getmap()
        if detectcollision(self.x+xoffset, self.y+yoffset,Map) != True:
            Map[self.y][self.x].occupants.remove(self)
            self.x += xoffset*self.speed
            self.y += yoffset*self.speed
            Map[self.y][self.x].occupants.append(self)
            gamemap.setmap(state.update_visibility(Map, self.x, self.y, gamemap.getwidth(), gamemap.getheight(),self.viewrestrict))
            return 1

        elif Map[self.y+yoffset][self.x+xoffset].occupants != [] and self.health > 0:
            self.attack(Map[self.y+yoffset][self.x+xoffset].occupants[0], random.randint(self.mindamage,self.maxdamage), lightblue)
            return 1
        elif self.health > 0:
            if self.pickaxe == True:
                self.attackwall(Map,self.x+xoffset,self.y+yoffset)
                return 1
            return 0
        else:
            print("You are dead. Act like it.")

    def attackwall(self, Map, x, y):
        if Map[y][x].name == "wall":
            Map[y][x].health -= random.randint(self.mindamage,self.maxdamage)
            if Map[y][x].health <= 0:
                print("The wall crumbles.")
                Map[y][x] = gamemap.Tile_Floor("floor", x, y, Map[y][x].colour)
                gamemap.setmap(state.update_visibility(Map, self.x, self.y, gamemap.getwidth(), gamemap.getheight(),self.viewrestrict))
            
    def stair(self):
        Map = gamemap.getmap()
        width = gamemap.getwidth()
        height = gamemap.getheight()
        if Map[self.y][self.x].name == "stairs":
            self.x = random.randint(10, width-10)
            self.y = random.randint(10, height-10)
            global entitylist
            entitylist = [self]
            Map = gamemap.setup(width, height, self.x, self.y)
            Map[self.y][self.x].occupants.append(self)
            return 2
        else:
            print("You are not above a way down")
            return 0
            
    def pickup(self):
        Map = gamemap.getmap()
        for i in range(len(Map[self.y][self.x].occupants)):
            current = Map[self.y][self.x].occupants[i]
            if current.pickupable == True:
                if menu.addtoinv(current) == False:
                    print("Inventory full!")
                    return 0
                Map[self.y][self.x].occupants.pop(i)
                entitylist.remove(current)
                self.inventory.append(current)
                print("Picked up", current.name)
                if current.name == "pickaxe":
                    self.pickaxe = True
                gamemap.setmap(state.update_visibility(Map, self.x, self.y, gamemap.getwidth(), gamemap.getheight(),self.viewrestrict))
                return 1
        return 0

        def attack(self, target, damage, col):
            target.health -= damage
            renderer.flash(target,col)
            if target.health <= -2 and target.name != "Player's corpse":
                print(target.name, " is destroyed!")
                entitylist.remove(target)
                Map = gamemap.getmap()
                Map[target.y][target.x].occupants.remove(target)
                target.loot()
                gamemap.setmap(state.update_visibility(Map, self.x, self.y, gamemap.getwidth(), gamemap.getheight(),self.viewrestrict))
                return 2
            elif target.health <= 0 and target.name != "Player's corpse":
                print(target.name, " is dead!")
                target.name = target.name + "'s corpse"
                target.speed = 0
                target.initiative = 0
                target.ap = 0
                target.char = "%"
                
            else:
                print(target.name, "'s health is now ", target.health)
                if random.randint(1,10) == 1:
                    target.ap = 0

class Goblin(Enemy):
    def __init__(self, x, y):
        Enemy.__init__(self, "Goblin", x, y, random.randint(3,6), "ȍ", olivedrab, 25, "Little green guy")


    def take_action(self):
        if self.health <= 0:
            return 1
        player = getplayer()
        if distance(self.x, self.y, player.x, player.y) > 8:
            self.move(random.randint(-1,1), random.randint(-1,1))
            return 1
        Map = gamemap.getmap()
        found,route = astar.astar(Map[self.y][self.x], Map[player.y][player.x], Map)
        if found == True and len(route) > 1:
            Map[self.y][self.x].occupants.remove(self)
            self.y = route[-2].y
            self.x = route[-2].x
            Map[self.y][self.x].occupants.append(self)
        elif found == True and len(route) <= 1:
            self.attack(player, random.randint(1,4), red)
            if player.health <= 0:
                if menu.deathscreen() == 50:
                    return 50
                if random.randint(1,10) == 1:
                    return 5

        gamemap.setmap(state.update_visibility(Map, player.x, player.y, gamemap.getwidth(), gamemap.getheight(),player.viewrestrict))
        return 1
    
    def loot(self):
        Map = gamemap.getmap()
        Map[self.y][self.x].occupants.append(procgeneration.common_loot(self.x,self.y))

class Rat(Enemy):
    def __init__(self, x, y):
        Enemy.__init__(self, "Rat", x, y, random.randint(1,3), "r", grey, 23, "Little grey guy")

    def take_action(self):
        if self.health <= 0:
            return 1
        player = getplayer()
        if distance(self.x, self.y, player.x, player.y) > 15:
            self.move(random.randint(-1,1), random.randint(-1,1))
            return 1
        Map = gamemap.getmap()
        found,route = astar.astar(Map[self.y][self.x], Map[player.y][player.x], Map)
        if found == True and len(route) > 1:
            Map[self.y][self.x].occupants.remove(self)
            self.y = route[-2].y
            self.x = route[-2].x
            Map[self.y][self.x].occupants.append(self)
        elif found == True and len(route) <= 1:
            self.attack(player, random.randint(1,2), red)
            if player.health <= 0:
                if menu.deathscreen() == 50:
                    return 50
            

        gamemap.setmap(state.update_visibility(Map, player.x, player.y, gamemap.getwidth(), gamemap.getheight(),player.viewrestrict))
        return 1

class Orc(Enemy):
    def __init__(self, x, y):
        Enemy.__init__(self, "Orc", x, y, random.randint(8,12), "Ȍ", olivedrab, 30, "Big green guy")


    def take_action(self):
        if self.health <= 0:
            return 1
        player = getplayer()
        if distance(self.x, self.y, player.x, player.y) > 5:
            self.move(random.randint(-1,1), random.randint(-1,1))
            return 1
        Map = gamemap.getmap()
        found,route = astar.astar(Map[self.y][self.x], Map[player.y][player.x], Map)
        if found == True and len(route) > 1:
            Map[self.y][self.x].occupants.remove(self)
            self.y = route[-2].y
            self.x = route[-2].x
            Map[self.y][self.x].occupants.append(self)
        elif found == True and len(route) <= 1:
            self.attack(player, random.randint(3,5), red)
            if player.health <= 0:
                if menu.deathscreen() == 50:
                    return 50
                if random.randint(1,10) == 1:
                    return 5

        gamemap.setmap(state.update_visibility(Map, player.x, player.y, gamemap.getwidth(), gamemap.getheight(),player.viewrestrict))
        return 1

    def loot(self):
        Map = gamemap.getmap()
        rand = random.randint(1,100)
        if rand <= 10:
            Map[self.y][self.x].occupants.append(procgeneration.common_loot(self.x,self.y))
        elif rand <= 90:
            Map[self.y][self.x].occupants.append(procgeneration.uncommon_loot(self.x,self.y))
        else:
            Map[self.y][self.x].occupants.append(procgeneration.rare_loot(self.x,self.y))

class Orc_Chief(Enemy):
    def __init__(self, x, y):
        Enemy.__init__(self, "Orc Cheif", x, y, random.randint(15,25), "Ψ", red, 25, "Big green guy")
    def take_action(self):
        if self.health <= 0:
            return 1
        player = getplayer()
        if distance(self.x, self.y, player.x, player.y) > 8:
            self.move(random.randint(-1,1), random.randint(-1,1))
            return 1
        Map = gamemap.getmap()
        found,route = astar.astar(Map[self.y][self.x], Map[player.y][player.x], Map)
        if found == True and len(route) > 1:
            Map[self.y][self.x].occupants.remove(self)
            self.y = route[-2].y
            self.x = route[-2].x
            Map[self.y][self.x].occupants.append(self)
        elif found == True and len(route) <= 1:
            self.attack(player, random.randint(4,8), red)
            if player.health <= 0:
                if menu.deathscreen() == 50:
                    return 50
            if random.randint(1,3) == 1:
                gamemap.setmap(state.update_visibility(Map, player.x, player.y, gamemap.getwidth(), gamemap.getheight(),player.viewrestrict))
                return 5
            

        gamemap.setmap(state.update_visibility(Map, player.x, player.y, gamemap.getwidth(), gamemap.getheight(),player.viewrestrict))
        return 1
    
    def loot(self):
        Map = gamemap.getmap()
        Map[self.y][self.x].occupants.append(create_strengthessence("strengthessence",self.x,self.y,5,"†",red,False,1))
    
class Health_Potion(Entity):
    def __init__(self, name, x, y, health, char, colour, healamount):
        Entity.__init__(self, name, x, y, health, char, colour, "Heals you by "+str(healamount))
        self.healamount = healamount
    
    def use(self):
        player = getplayer()
        player.health = min(player.health+self.healamount,player.maxhealth)
        player.inventory.remove(self)
        menu.removefrominv(self)

class Ancient_Flower(Entity):
    def __init__(self, name, x, y, health, char, colour, manaamount):
        Entity.__init__(self, name, x, y, health, char, colour, "Regenerates mana by "+str(manaamount))
        self.manaamount = manaamount
    
    def use(self):
        player = getplayer()
        player.mana = min(player.mana+self.manaamount,player.maxmana)
        player.inventory.remove(self)
        menu.removefrominv(self)

class Pickaxe(Entity):
    def __init__(self, name, x, y, health, char, colour):
        Entity.__init__(self, name, x, y, health, char, colour, "Lets you dig through walls")

    def drop(self):
        player = getplayer()
        player.inventory.remove(self)
        self.x = player.x
        self.y = player.y
        entitylist.insert(0,self)
        Map = gamemap.getmap()
        Map[player.y][player.x].occupants.append(self)
        menu.removefrominv(self)
        player.pickaxe = False
        for i in range(len(player.inventory)):
            if player.inventory[i].name == "pickaxe":
                player.pickaxe = True

class Health_Crystal(Entity):
    def __init__(self, name, x, y, health, char, colour, healamount):
        Entity.__init__(self, name, x, y, health, char, colour, "Permanently increases your health by "+str(healamount))
        self.healamount = healamount
    
    def use(self):
        player = getplayer()
        player.maxhealth = player.maxhealth + self.healamount
        player.health += self.healamount
        player.inventory.remove(self)
        menu.removefrominv(self)

class Strength_Essence(Entity):
    def __init__(self, name, x, y, health, char, colour, strengthamount):
        Entity.__init__(self, name, x, y, health, char, colour, "Permanently increases your strength by "+str(strengthamount))
        self.strengthamount = strengthamount
    
    def use(self):
        player = getplayer()
        player.maxdamage += self.strengthamount
        player.mindamage = player.maxdamage // 3
        player.inventory.remove(self)
        menu.removefrominv(self)

class Mana_Crystal(Entity):
    def __init__(self, name, x, y, health, char, colour, manaamount):
        Entity.__init__(self, name, x, y, health, char, colour, "Permanently increases your mana by "+str(manaamount))
        self.manaamount = manaamount
    
    def use(self):
        player = getplayer()
        player.maxmana = player.maxmana + self.manaamount
        player.mana += self.manaamount
        player.inventory.remove(self)
        menu.removefrominv(self)

        
class Generic_Item(Entity):
    def __init__(self, name, x, y, health, char, colour, description):
        Entity.__init__(self, name, x, y, health, char, colour, description)

class IceWall_Spellbook(Entity):
    def __init__(self, name, x, y, health, char, colour):
        Entity.__init__(self, name, x, y, health, char, colour, "Lets you learn the icewall spell")

    def use(self):
        player = getplayer()
        player.inventory.remove(self)
        menu.removefrominv(self)
        if spells.check_spells("icewall") != True:
            spells.giveicewall(0)

class FireWall_Spellbook(Entity):
    def __init__(self, name, x, y, health, char, colour):
        Entity.__init__(self, name, x, y, health, char, colour, "Lets you learn the firewall spell")

    def use(self):
        player = getplayer()
        player.inventory.remove(self)
        menu.removefrominv(self)
        if spells.check_spells("firewall") != True:
            spells.givefirewall(0)

class HealSpell_Spellbook(Entity):
    def __init__(self, name, x, y, health, char, colour):
        Entity.__init__(self, name, x, y, health, char, colour, "Lets you learn how to use magic to heal yourself")

    def use(self):
        player = getplayer()
        player.inventory.remove(self)
        menu.removefrominv(self)
        if spells.check_spells("healspell") != True:
            spells.givehealspell(0)


def create_entity(name: str, x: int, y: int, health: int, char: str, colour, item,description):
    global entitylist
    newEntity = Entity(name, x, y, health, char, colour,description)
    if item == False:
        entitylist.insert(0,newEntity)
    return newEntity

def create_enemy(name: str, x: int, y: int, health: int, char: str, colour, initiative, description):
    global entitylist
    newEnemy = Enemy(name, x, y, health, char, colour, initiative, description)
    entitylist.insert(0,newEnemy)
    return newEnemy

def create_goblin(x,y):
    global entitylist
    newEnemy = Goblin(x,y)
    entitylist.insert(0,newEnemy)
    return newEnemy

def create_orc(x,y):
    global entitylist
    newEnemy = Orc(x,y)
    entitylist.insert(0,newEnemy)
    return newEnemy

def create_orc_cheif(x,y):
    global entitylist
    newEnemy = Orc_Chief(x, y)
    entitylist.insert(0,newEnemy)
    return newEnemy

def create_rat(x,y):
    global entitylist
    newEnemy = Rat(x,y)
    entitylist.insert(0,newEnemy)
    return newEnemy

def create_player(name: str, x: int, y: int, health: int, char: str, colour, initiative):
    global entitylist
    newPlayer = Player(name, x, y, health, char, colour, initiative)
    entitylist.append(newPlayer)
    return newPlayer

def create_healthpotion(name: str, x: int, y: int, health: int, char: str, colour, item, healamount):
    global entitylist
    newEntity = Health_Potion(name, x, y, health, char, colour, healamount)
    newEntity.pickupable = True
    if item == False:
        entitylist.insert(0,newEntity)
    return newEntity

def create_healthcrystal(name: str, x: int, y: int, health: int, char: str, colour, item, healamount):
    global entitylist
    newEntity = Health_Crystal(name, x, y, health, char, colour, healamount)
    newEntity.pickupable = True
    if item == False:
        entitylist.insert(0,newEntity)
    return newEntity

def create_strengthessence(name: str, x: int, y: int, health: int, char: str, colour, item, strengthamount):
    global entitylist
    newEntity = Strength_Essence(name, x, y, health, char, colour, strengthamount)
    newEntity.pickupable = True
    if item == False:
        entitylist.insert(0,newEntity)
    return newEntity

def create_manacrystal(name: str, x: int, y: int, health: int, char: str, colour, item, manaamount):
    global entitylist
    newEntity = Mana_Crystal(name, x, y, health, char, colour, manaamount)
    newEntity.pickupable = True
    if item == False:
        entitylist.insert(0,newEntity)
    return newEntity

def create_ancientflower(name: str, x: int, y: int, health: int, char: str, colour, item, manaamount):
    global entitylist
    newEntity = Ancient_Flower(name, x, y, health, char, colour, manaamount)
    newEntity.pickupable = True
    if item == False:
        entitylist.insert(0,newEntity)
    return newEntity

def create_pickaxe(name: str, x: int, y: int, health: int, char: str, colour, item):
    global entitylist
    newEntity = Pickaxe(name, x, y, health, char, colour)
    newEntity.pickupable = True
    if item == False:
        entitylist.insert(0,newEntity)
    return newEntity

def create_generic_item(name: str, x: int, y: int, health: int, char: str, colour, item, description):
    global entitylist
    newEntity = Generic_Item(name, x, y, health, char, colour, description)
    newEntity.pickupable = True
    if item == False:
        entitylist.insert(0,newEntity)
    return newEntity

def create_IceWall_Spellbook(name: str, x: int, y: int, health: int, char: str, colour, item):
    global entitylist
    newEntity = IceWall_Spellbook(name, x, y, health, char, colour)
    newEntity.pickupable = True
    if item == False:
        entitylist.insert(0,newEntity)
    return newEntity

def create_HealSpell_Spellbook(name: str, x: int, y: int, health: int, char: str, colour, item):
    global entitylist
    newEntity = HealSpell_Spellbook(name, x, y, health, char, colour)
    newEntity.pickupable = True
    if item == False:
        entitylist.insert(0,newEntity)
    return newEntity

def create_FireWall_Spellbook(name: str, x: int, y: int, health: int, char: str, colour, item):
    global entitylist
    newEntity = FireWall_Spellbook(name, x, y, health, char, colour)
    newEntity.pickupable = True
    if item == False:
        entitylist.insert(0,newEntity)
    return newEntity

def getentities():
    return entitylist

def getplayer():
    return entitylist[len(entitylist)-1]

def deleteentities():
    global entitylist
    entitylist = []
    return entitylist

def detectcollision(x,y,Map):
    if Map[y][x].walkable == True:
        if Map[y][x].occupants != []:
            for i in range(len(Map[y][x].occupants)):
                if Map[y][x].occupants[i].blocking == True:
                    return True
        return False
    return True

def direction(startx, starty, destx, desty):
    ndist = distance(startx, starty-1, destx, desty)
    nedist = distance(startx+1, starty-1, destx, desty)
    edist = distance(startx+1, starty, destx, desty)
    sedist = distance(startx+1, starty+1, destx, desty)
    sdist = distance(startx, starty+1, destx, desty)
    swdist = distance(startx-1, starty+1, destx, desty)
    wdist = distance(startx-1, starty, destx, desty)
    nwdist = distance(startx-1, starty-1, destx, desty)

    # If North is closest, go North
    if ndist < nedist and ndist < edist and ndist < sedist and ndist < sdist and ndist < swdist and ndist < wdist and ndist < nwdist:
        return 0,-1
    # If North-East is closest, go North-East
    elif nedist < edist and nedist < sedist and nedist < sdist and nedist < swdist and nedist < wdist and nedist < nwdist:
        return 1,-1
    # If East is closest, go East
    elif edist < sedist and edist < sdist and edist < swdist and edist < wdist and edist < nwdist:
        return 1,0
    # If South-East is closest, go South-East
    elif sedist < sdist and sedist < swdist and sedist < wdist and sedist < nwdist:
        return 1,1
    # If South is closest, go South
    elif sdist < swdist and sdist < wdist and sdist < nwdist:
        return 0,1
    # If South-West is closest, go South-West
    elif swdist < wdist and swdist < nwdist:
        return -1,1
    # If West is closest, go West
    elif wdist < nwdist:
        return -1,0
    # If North-West is closes, go West
    else:
        return -1,-1
    
def distance(ax, ay, bx, by):
    xdist = ax - bx
    ydist = ay - by
    answer = math.sqrt((xdist ** 2) + (ydist ** 2))
    return answer
