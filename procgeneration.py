import gamemap
import colours
import random
import entities
import math

colourdict = colours.getcolours() 

white = colourdict["white"]
mint = colourdict["mint"]
green = colourdict["green"]
camel = colourdict["camel"]
maroon = colourdict["maroon"]
red = colourdict["red"]
slate = colourdict["slate"]
lightblue = colourdict["lightblue"]

def checkadjacent(Map, width, height, x, y, nametag, altnametag):
    count = 0

    # Check cardinal directions
    
    # North
    if y != 0 and (Map[y-1][x].name == nametag or Map[y-1][x].name == altnametag):
        count += 1
    # North-East
    if y != 0 and x != width-1 and (Map[y-1][x+1].name == nametag or Map[y-1][x+1].name == altnametag):
        count += 1
    # East
    if x != width-1 and (Map[y][x+1].name == nametag or Map[y][x+1].name == altnametag):
        count += 1
    # South-East
    if x != width-1 and y != height-1 and (Map[y+1][x+1].name == nametag or Map[y+1][x+1].name == altnametag):
        count += 1
    # South
    if y != height-1 and (Map[y+1][x].name == nametag or Map[y+1][x].name == altnametag):
        count += 1
    # South-West
    if y != height-1 and x != 0 and (Map[y+1][x-1].name == nametag or Map[y+1][x-1].name == altnametag):
        count += 1
    # West
    if x != 0 and (Map[y][x-1].name == nametag or Map[y][x-1].name == altnametag):
        count += 1
    # North-West
    if y != 0 and x != 0 and (Map[y-1][x-1].name == nametag or Map[y-1][x-1].name == altnametag):
        count += 1
    
    return count
    
def choosecolour():
    colourlist = [colourdict["maroon"],colourdict["mint"],colourdict["slate"],colourdict["gray"],colourdict["sandybrown"],colourdict["goldenrod"],colourdict["rosybrown"],colourdict["chocolate"],colourdict["pink"],colourdict["paleviolet"],colourdict["salmon"],colourdict["purple"],colourdict["indigo"],colourdict["mediumpurple"],colourdict["darkaquamarine"],colourdict["teal"],colourdict["crimson"],colourdict["olive"]]
    return colourlist[random.randint(0,len(colourlist)-1)]

def drunkardwalk(Map, width, height, startx, starty):
    # Iterate through each tile of the Map
    colour = choosecolour()
    for y in range(height):
        for x in range(width):
            Map[y][x] = gamemap.Tile_Wall("wall",x,y,(random.randint(max(colour[0]-20,0),min(colour[0]+20,255)), random.randint(max(colour[1]-20,0),min(colour[1]+20,255)), random.randint(max(colour[2]-20,0),min(colour[2]+20,255))))
            # Set every tile to a wall
    drunkx = startx
    drunky = starty
    # Number of tiles placed
    total = 0
    limit = random.randint(400,1000)
    # Random border width
    border = random.randint(3, 8)
    # Until the number of tiles placed meets the random total (creates variety in the types of map)
    while total <= limit:
        if Map[drunky][drunkx].name == "wall":
            Map[drunky][drunkx] = gamemap.Tile_Floor("floor",drunkx,drunky,camel)
            total += 1
        # Choose a random direction
        rand = random.randint(1,4)
        if rand == 1 and drunky > border and drunkx < width-(border+1) and drunkx > border:
            # Go North
            drunky -= 1
        if rand == 2 and drunkx < width-(border+1) and drunky > border and drunky < height-(border+1):
            # Go East
            drunkx += 1
        if rand == 3 and drunky < height-(border+1) and drunkx < width-(border+1) and drunkx > border:
            # Go South
            drunky += 1
        if rand == 4 and drunkx > border and drunky > border and drunky < height-(border+1):
            # Go West
            drunkx -= 1
    for y in range(height):
        for x in range(width):
            surrounding = checkadjacent(Map, width, height, x, y, "wall", "")
            
            if surrounding <= random.randint(0,2):
                # Cull small groups of tiles
                Map[y][x] = gamemap.Tile_Floor("floor",x,y,camel)
            elif surrounding == 8:
                # black out totally invisible tiles (surrounded on all sides)
                Map[y][x].visible = False
    return Map


def populate(Map, width, height, startx,starty):
    curx = 0
    cury = 0
    while Map[cury][curx].walkable != True or distance(curx,cury,startx,starty) < 10:
        curx = random.randint(3,width-3)
        cury = random.randint(3,height-3)
    stairs = gamemap.Tile("stairs",curx,cury,"H",mint,True,True,False)
    Map[cury][curx] = stairs

    curx = 0
    cury = 0
    for i in range(random.randint(1,5)):
        while Map[cury][curx].walkable != True or distance(curx,cury,startx,starty) < 10 or Map[cury][curx].name == "stairs" or Map[cury][curx].occupants != []:
            curx = random.randint(3,width-3)
            cury = random.randint(3,height-3)
        newitem = loot_table(curx,cury)
        Map[cury][curx].occupants.append(newitem)
    
    total = 0
    limit = random.randint(5, 10)
    while total < limit:
        curx = random.randint(3,width-3)
        cury = random.randint(3,height-3)
        if Map[cury][curx].walkable == True and Map[cury][curx].name != "stairs" and distance(curx, cury, startx,starty) > 3:
            total += 1
            spawntable(curx,cury,Map)
    return Map
# entities.create_enemy("Dummy", x, y, 3, "$", red, 30, "AHH CAPTALISM")
def spawntable(x,y,Map):
    rand = random.randint(1,100)
    if rand <= 10:
        Map[y][x].occupants.append(entities.create_orc(x,y))
    elif rand <= 15:
        Map[y][x].occupants.append(entities.create_orc_cheif(x,y))
    elif rand <= 50:
        Map[y][x].occupants.append(entities.create_rat(x,y))
    else:
        Map[y][x].occupants.append(entities.create_goblin(x,y))

def loot_table(x,y):
    rand = random.randint(1,100)
    
    if rand <= 45:
        return common_loot(x,y)
    
    elif rand <= 75:
        return uncommon_loot(x,y)
    
    else:
        return rare_loot(x,y)
    
def common_loot(x,y):
    rand = random.randint(1,100)
    if rand <= 10:
        return entities.create_healthpotion("healthpotion",x,y,5,"p",mint, False, 5)
    elif rand <= 20:
        return entities.create_ancientflower("manaflower",x,y,5,"ΐ",lightblue,False,5)
    elif rand <= 70:
        return entities.create_generic_item("rock",x,y,1,"o",slate, False, "")
    else:
        return entities.create_generic_item("scrap",x,y,1,"&",white, False, "")
    
    
def uncommon_loot(x,y):
    rand = random.randint(1,100)
    if rand <= 10:
        return entities.create_pickaxe("pickaxe",x,y,5,"⸕",white, False)
    elif rand <= 20:
        return entities.create_healthpotion("greaterhealthpotion",x,y,5,"P",mint,False, 10)
    elif rand <= 30:
        return entities.create_ancientflower("ancientflower",x,y,5,"ΐ",lightblue,False,10)
    elif rand <= 40:
        return entities.create_healthcrystal("healthcrystal", x, y, 5, "♥", red, False, 2)
    elif rand <= 50:
        return entities.create_manacrystal("manacrystal", x, y, 5, "☼", lightblue, False, 2)
    else:
        return entities.create_generic_item("scrap",x,y,1,"&",white, False, "")
    
def rare_loot(x,y):
    rand = random.randint(1,100)
    if rand <= 10:
        return entities.create_healthpotion("epichealthpotion",x,y,5,"P",mint, False, 20)
    elif rand <= 20:
        return entities.create_ancientflower("primordialflower",x,y,5,"ΐ",lightblue,False,20)
    elif rand <= 30:
        return entities.create_IceWall_Spellbook("icewallspellbook", x, y, 10, "Þ", lightblue, False)
    elif rand <= 40:
        return entities.create_FireWall_Spellbook("firewallspellbook", x, y, 10, "ģ", red, False)
    elif rand <= 50:
        return entities.create_HealSpell_Spellbook("healspellspellbook", x, y, 10, "ĥ", green, False)
    elif rand <= 60:
        return entities.create_healthcrystal("uberhealthcrystal", x, y, 5, "♥", red, False, 4)
    elif rand <= 70:
        return entities.create_manacrystal("ubermanacrystal", x, y, 5, "☼", lightblue, False, 4)
    else:
        return entities.create_generic_item("scrap",x,y,1,"&",white, False, "")

def distance(ax, ay, bx, by):
    xdist = ax - bx
    ydist = ay - by
    answer = math.sqrt((xdist ** 2) + (ydist ** 2))
    return answer
