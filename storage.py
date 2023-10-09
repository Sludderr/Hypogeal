import json
import os
import entities
import gamemap


playerpath = os.path.join("savedata/player","playerdata.json")
mappath = os.path.join("savedata/map","mapdata.json")
entitypath = os.path.join("savedata/entities","entitydata.json")
invpath = os.path.join("savedata/inventory","inventorydata.json")

def storeplayer():
    player = entities.getplayer()
    playerdata = open(playerpath, "w")
    playerdict = {
        "name": player.name,
        "x": player.x,
        "y": player.y,
        "health": player.health,
        "maxhealth": player.maxhealth,
        "mana": player.mana,
        "maxmana": player.maxmana,
        "ap": player.ap,
        "invsize": len(player.inventory),
        "char": player.char,
        "initiative": player.initiative,
        "sentient": player.sentient,
        "viewrestrict": player.viewrestrict,
        "colour": player.colour
    }
    
    x = json.dumps(playerdict)
    playerdata.write(x)
    playerdata.close()

    inventory = player.inventory
    invdict = {
    }
    inventorydata = open(invpath, "w")
    for i in range(len(inventory)):
        itemdict = vars(inventory[i])
        invdict[i] = itemdict
        
    inventorydata.write(json.dumps(invdict))
    inventorydata.close()

def loadplayer():
    playerdata = open(playerpath, "r")
    playerdict = json.loads(playerdata.readline())
    player = entities.create_player(playerdict["name"],playerdict["x"],playerdict["y"],playerdict["health"],playerdict["char"],playerdict["colour"], playerdict["viewrestrict"])
    player.mana = playerdict["mana"]
    player.maxmana = playerdict["maxmana"]
    player.ap = playerdict["ap"]
    player.maxhealth = playerdict["maxhealth"]
    player.initiative = playerdict["initiative"]
    player.sentient = playerdict["sentient"]
    
    
    inventorydata = open(invpath, "r")
    inventorydict = json.loads(inventorydata.readline())
    for i in range(playerdict["invsize"]):
        itemdict = inventorydict[str(i)]
        newitem = entities.create_item(itemdict["name"],itemdict["x"],itemdict["y"],itemdict["health"],itemdict["char"],itemdict["colour"])
        player.inventory.append(newitem)


    inventorydata.close()
    playerdata.close()

    return player



def checkplayer():
    if os.path.isfile(playerpath):
        return True
    return False

def storemap():
    mapdata = open(mappath,"w")

    Map = gamemap.getmap()
    width = gamemap.getwidth()
    height = gamemap.getheight()
   

    mapinfo = {
        "width": width,
        "height": height
    }

    mapdict = {
        "0": mapinfo
    }

    index = 0
    for y in range(height):
        for x in range(width):
            tile = Map[y][x]
            tiledict = {
                "name": tile.name,
                "x": tile.x,
                "y": tile.y,
                "char": tile.char,
                "colour": tile.colour,
                "walkable": tile.walkable,
                "visible": tile.visible,
                "rendered": tile.rendered,
            }
            index += 1
            mapdict[index] = tiledict

    mapdata.write(json.dumps(mapdict))

    return

def storeentities():
    entitydata = open(entitypath, "w")

    entitylist = entities.getentities()

    entitydict = {
        "0": len(entitylist)-1
    }

    for i in range(len(entitylist)):

        if entitylist[i].name != "Player":
            if entitylist[i].sentient == True:
                currentdict = {
                    "name": entitylist[i].name,
                    "x": entitylist[i].x,
                    "y": entitylist[i].y,
                    "health": entitylist[i].health,
                    "maxhealth": entitylist[i].maxhealth,
                    "char": entitylist[i].char,
                    "colour": entitylist[i].colour,
                    "speed": entitylist[i].speed,
                    "blocking": entitylist[i].blocking,
                    "sentient": entitylist[i].sentient,
                    "pickupable": entitylist[i].pickupable,
                    "initiative": entitylist[i].initiative,
                    "ap": entitylist[i].ap
                }
            else:
                currentdict = {
                    "name": entitylist[i].name,
                    "x": entitylist[i].x,
                    "y": entitylist[i].y,
                    "health": entitylist[i].health,
                    "maxhealth": entitylist[i].maxhealth,
                    "char": entitylist[i].char,
                    "colour": entitylist[i].colour,
                    "speed": entitylist[i].speed,
                    "blocking": entitylist[i].blocking,
                    "sentient": entitylist[i].sentient,
                    "pickupable": entitylist[i].pickupable
                }
            entitydict[i+1] = currentdict
    
    entitydata.write(json.dumps(entitydict))



def loadmap():
    mapdata = open(mappath, "r")
    mapdict = json.loads(mapdata.readline())
    info = mapdict["0"]
    width = info["width"]
    height = info["height"]
    
    count = 0
    Map = [[0 for x in range(width)] for y in range(height)]

    for y in range(height):
        for x in range(width):
            count += 1
            tiledata = mapdict[str(count)]
            Map[y][x] = gamemap.Tile(tiledata["name"], tiledata["x"], tiledata["y"], tiledata["char"], tiledata["colour"], tiledata["walkable"], tiledata["visible"], tiledata["rendered"])

    gamemap.setmap(Map)
    gamemap.setwidth(width)
    gamemap.setheight(height)

def loadentities():
    entitydata = open(entitypath, "r")
    entitydict = json.loads(entitydata.readline())

    Map = gamemap.getmap()

    for i in range(entitydict["0"]):
        current = entitydict[str(i+1)]
        if current["sentient"] == True:
            newEntity = entities.create_enemy(current["name"],current["x"],current["y"],current["health"],current["char"],current["colour"],current["initiative"])
            newEntity.maxhealth = current["maxhealth"]
            newEntity.speed = current["speed"]
            newEntity.blocking = current["blocking"]
            newEntity.sentient = True
            newEntity.pickupable = current["pickupable"]
            newEntity.ap = current["ap"]
        else:
            newEntity = entities.create_entity(current["name"],current["x"],current["y"],current["health"],current["char"],current["colour"])
            newEntity.maxhealth = current["maxhealth"]
            newEntity.speed = current["speed"]
            newEntity.blocking = current["blocking"]
            newEntity.sentient = False
            newEntity.pickupable = current["pickupable"]
        
        Map[newEntity.y][newEntity.x].occupants.append(newEntity)

    return entities.getentities()

def loadall():
    loadmap()
    loadentities()
    player = loadplayer()
    return player

def storeall():
    storeplayer()
    storeentities()
    storemap()

def clearstorage():
    if os.path.isfile(invpath):
        os.remove(invpath)
    if os.path.isfile(playerpath):
        os.remove(playerpath)
    if os.path.isfile(mappath):
        os.remove(mappath)
    if os.path.isfile(entitypath):
        os.remove(entitypath)
