import gamemap
import colours
import random
import entities
import math

colourdict = colours.getcolours() 

white = colourdict["white"]
mint = colourdict["mint"]
camel = colourdict["camel"]
maroon = colourdict["maroon"]
red = colourdict["red"]

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
            
            if surrounding <= 1:
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
    stairs = gamemap.Tile("stairs",curx,cury,"Z",mint,True,True,False)
    Map[cury][curx] = stairs
    
    while Map[cury][curx].walkable != True or distance(curx,cury,startx,starty) < 10 or Map[cury][curx].name == "stairs":
        curx = random.randint(3,width-3)
        cury = random.randint(3,height-3)
    newpick = entities.create_entity("pickaxe",curx,cury, 5, "⸕", white)
    Map[cury][curx].occupants.append(newpick)
    newpick.pickupable = True
    
    total = 0
    limit = random.randint(3, 13)
    while total < limit:
        curx = random.randint(3,width-3)
        cury = random.randint(3,height-3)
        if Map[cury][curx].walkable == True and Map[cury][curx].name != "stairs" and distance(curx, cury, startx,starty) > 3:
            total += 1
            Map[cury][curx].occupants.append(entities.create_enemy("Dummy", curx, cury, 3, "$", red, 30))
    
    return Map


def distance(ax, ay, bx, by):
    xdist = ax - bx
    ydist = ay - by
    answer = math.sqrt((xdist ** 2) + (ydist ** 2))
    return answer
