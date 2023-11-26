import entities
import colours
import math
import random
import menu

colourdict = colours.getcolours()
red = colourdict["red"]
white = colourdict["white"]
lightblue = colourdict["lightblue"]
green = colourdict["green"]

spell_list = []

def distance(ax, ay, bx, by):
    xdist = ax - bx
    ydist = ay - by
    answer = math.sqrt((xdist ** 2) + (ydist ** 2))
    return answer


class spell():
    def __init__ (self, name, timer, cooldown, cost, char, colour):
        self.name = name
        self.timer = timer
        self.cooldown = cooldown
        self.cost = cost
        self.char = char
        self.colour = colour

    def use(self):
        return 0

class firewall(spell):
    def __init__(self, timer):
        spell.__init__(self, "firewall", timer, 10, 5, "*", red)

    def use(self):
        player = entities.getplayer()

        if player.mana < self.cost or self.timer > 0:
            return 0

        else:
            print("BANG")
            self.timer = self.cooldown
            player.mana -= self.cost
            entitylist = entities.getentities()
            i = 0
            while i < len(entitylist):
                if entitylist[i] != player and distance(entitylist[i].x,entitylist[i].y,player.x,player.y) < 1.9:
                    if player.attack(entitylist[i], random.randint(3, 10), red) == 2:
                        i -= 1
                i += 1
            return 1
        
class icewall(spell):
    def __init__(self, timer):
        spell.__init__(self, "icewall", timer, 10, 5, "*", lightblue)

    def use(self):
        player = entities.getplayer()

        if player.mana < self.cost or self.timer > 0:
            return 0

        else:
            print("WOOOSH")
            self.timer = self.cooldown
            player.mana -= self.cost
            entitylist = entities.getentities()
            i = 0
            while i < len(entitylist):
                if entitylist[i] != player and distance(entitylist[i].x,entitylist[i].y,player.x,player.y) < 1.9:
                    if player.attack(entitylist[i], random.randint(3, 10), lightblue) == 2:
                        i -= 1
                i += 1
            return 1

class healspell(spell):
    def __init__(self, timer):
        spell.__init__(self, "healspell", timer, 10, 10, "*", green)

    def use(self):
        player = entities.getplayer()
        if player.mana < self.cost or self.timer > 0:
            return 0
        else:
            print("shooo")
            self.timer = self.cooldown
            player.mana -= self.cost
            player.health = min(player.maxhealth, player.health + 5)

def givefirewall(timer):
    newspell = firewall(timer)
    spell_list.append(newspell)
    entities.getplayer().spell_list.append(newspell)
    menu.addtospells(newspell,timer)
    return newspell

def giveicewall(timer):
    newspell = icewall(timer)
    spell_list.append(newspell)
    entities.getplayer().spell_list.append(newspell)
    menu.addtospells(newspell,timer)
    return newspell

def givehealspell(timer):
    newspell = healspell(timer)
    spell_list.append(newspell)
    entities.getplayer().spell_list.append(newspell)
    menu.addtospells(newspell,timer)
    return newspell

def update_timers():
    for i in range(len(spell_list)):
        spell_list[i].timer = max(spell_list[i].timer-1, 0)
        if spell_list[i].timer == 0:
            menu.updatecolour(spell_list[i])

def check_spells(name):
    for i in range(len(spell_list)):
        if spell_list[i].name == name:
            return True
    return False
