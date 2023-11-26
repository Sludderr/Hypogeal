import json
import os
import entities
import gamemap
import menu
import spells

# paths to the files storing the savedata
playerpath = os.path.join("savedata/player","playerdata.json")
mappath = os.path.join("savedata/map","mapdata.json")
entitypath = os.path.join("savedata/entities","entitydata.json")
invpath = os.path.join("savedata/inventory","inventorydata.json")
spellpath = os.path.join("savedata/spells","spellsdata.json")

def storeplayer():
    player = entities.getplayer()
    playerdata = open(playerpath, "w")
    # construct a dictionary using the current states of values in the player object
    playerdict = {
        "name": player.name,
        "x": player.x,
        "y": player.y,
        "health": player.health,
        "maxhealth": player.maxhealth,
        "mana": player.mana,
        "maxmana": player.maxmana,
        "ap": player.ap,
        # stores size of inventory and spells to be used when loading the player
        "invsize": len(player.inventory),
        "spellsize": len(player.spell_list),
        "char": player.char,
        "initiative": player.initiative,
        "sentient": player.sentient,
        "viewrestrict": player.viewrestrict,
        "colour": player.colour,
        "mindamage": player.mindamage,
        "maxdamage": player.maxdamage
    }
    
    # makes a json string out of the player dictionary and writes to file. This will overwrite any previous playerdata stored
    x = json.dumps(playerdict)
    playerdata.write(x)
    playerdata.close()

    inventory = player.inventory
    # dictionary of dictionaries to store the whole inventory. Each item is 1 dictionary contained in a larger dictionary with the keys representing the index
    invdict = {
    }
    inventorydata = open(invpath, "w")
    for i in range(len(inventory)):
        # vars will create a dictionary out of an object, storing its attributes as keys. Only works for objects that do not include references to other objects
        itemdict = vars(inventory[i])
        invdict[i] = itemdict
        
    inventorydata.write(json.dumps(invdict))
    inventorydata.close()

    spell_list = player.spell_list
    spell_list_dict = {
    }
    spellsdata = open(spellpath, "w")
    for i in range(len(spell_list)):
        spelldict = vars(spell_list[i])
        spell_list_dict[i] = spelldict
    
    spellsdata.write(json.dumps(spell_list_dict))
    spellsdata.close

def loadplayer():
    # load the player data from the path. Create a new player object and update the attribute values with those stored
    playerdata = open(playerpath, "r")
    playerdict = json.loads(playerdata.readline())
    player = entities.create_player(playerdict["name"],playerdict["x"],playerdict["y"],playerdict["health"],playerdict["char"],playerdict["colour"], playerdict["viewrestrict"])
    player.mana = playerdict["mana"]
    player.maxmana = playerdict["maxmana"]
    player.ap = playerdict["ap"]
    player.maxhealth = playerdict["maxhealth"]
    player.initiative = playerdict["initiative"]
    player.sentient = playerdict["sentient"]
    player.mindamage = playerdict["mindamage"]
    player.maxdamage = playerdict["maxdamage"]
    
    inventorydata = open(invpath, "r")
    inventorydict = json.loads(inventorydata.readline())
    for i in range(playerdict["invsize"]):
        itemdict = inventorydict[str(i)]
        if "healthpotion" in itemdict["name"]:
            newitem = entities.create_healthpotion(itemdict["name"],itemdict["x"],itemdict["y"],itemdict["health"],itemdict["char"],itemdict["colour"], True, itemdict["healamount"])
        elif "flower" in itemdict["name"]:
            newitem = entities.create_ancientflower(itemdict["name"],itemdict["x"],itemdict["y"],itemdict["health"],itemdict["char"],itemdict["colour"], True, itemdict["manaamount"])
        elif itemdict["name"] == "pickaxe":
            newitem = entities.create_pickaxe(itemdict["name"],itemdict["x"],itemdict["y"],itemdict["health"],itemdict["char"],itemdict["colour"], True)
            player.pickaxe = True
        elif itemdict["name"] == "firewallspellbook":
            newitem = entities.create_FireWall_Spellbook(itemdict["name"],itemdict["x"],itemdict["y"],itemdict["health"],itemdict["char"],itemdict["colour"], True)
        elif itemdict["name"] == "icewallspellbook":
            newitem = entities.create_IceWall_Spellbook(itemdict["name"],itemdict["x"],itemdict["y"],itemdict["health"],itemdict["char"],itemdict["colour"], True)
        elif itemdict["name"] == "healspellspellbook":
            newitem = entities.create_HealSpell_Spellbook(itemdict["name"],itemdict["x"],itemdict["y"],itemdict["health"],itemdict["char"],itemdict["colour"], True)
        elif "healthcrystal" in itemdict["name"]:
            newitem = entities.create_healthcrystal(itemdict["name"],itemdict["x"],itemdict["y"],itemdict["health"],itemdict["char"],itemdict["colour"], True, itemdict["healamount"])
        elif "manacrystal" in itemdict["name"]:
            newitem = entities.create_manacrystal(itemdict["name"],itemdict["x"],itemdict["y"],itemdict["health"],itemdict["char"],itemdict["colour"], True, itemdict["manaamount"])
        elif "strengthessence" in itemdict["name"]:
            newitem = entities.create_strengthessence(itemdict["name"],itemdict["x"],itemdict["y"],itemdict["health"],itemdict["char"],itemdict["colour"], True, itemdict["strengthamount"])
        else:
            newitem = entities.create_generic_item(itemdict["name"],itemdict["x"],itemdict["y"],itemdict["health"],itemdict["char"],itemdict["colour"], True, itemdict["description"])
        menu.addtoinv(newitem)
        player.inventory.append(newitem)

    inventorydata.close()

    spellsdata = open(spellpath, "r")
    spell_list_dict = json.loads(spellsdata.readline())
    for i in range(playerdict["spellsize"]):
        spelldict = spell_list_dict[str(i)]
        if spelldict["name"] == "firewall" and spells.check_spells("firewall") != True:
            newspell = spells.givefirewall(spelldict["timer"])

        elif spelldict["name"] == "icewall" and spells.check_spells("icewall") != True:
            newspell = spells.giveicewall(spelldict["timer"])

        elif spelldict["name"] == "healspell" and spells.check_spells("healspell") != True:
            newspell = spells.givehealspell(spelldict["timer"])
        
    spellsdata.close()

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
        "0": mapinfo # width and height of map
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
                    "ap": entitylist[i].ap,
                    "description": entitylist[i].description
                }
            else:
                currentdict = vars(entitylist[i])
            entitydict[i+1] = currentdict
    
    entitydata.write(json.dumps(entitydict))



def loadmap():
    mapdata = open(mappath, "r")
    mapdict = json.loads(mapdata.readline())
    info = mapdict["0"]
    width = info["width"]
    height = info["height"]
    
    count = 0
    # new map 2D array
    Map = [[0 for x in range(width)] for y in range(height)]

    # loop through array and create new map tiles using the stored values
    for y in range(height):
        for x in range(width):
            count += 1
            tiledata = mapdict[str(count)]
            Map[y][x] = gamemap.Tile(tiledata["name"], tiledata["x"], tiledata["y"], tiledata["char"], tiledata["colour"], tiledata["walkable"], tiledata["visible"], tiledata["rendered"])

    gamemap.setmap(Map)
    gamemap.setwidth(width)
    gamemap.setheight(height)
    # set the gamemap to the new loaded map

def loadentities():
    entitydata = open(entitypath, "r")
    entitydict = json.loads(entitydata.readline())

    Map = gamemap.getmap()

    for i in range(entitydict["0"]):
        current = entitydict[str(i+1)]
        if current["sentient"] == True:
            if current["name"] == "Goblin":
                newEntity = entities.create_goblin(current["x"],current["y"])
            elif current["name"] == "Rat":
                newEntity = entities.create_rat(current["x"],current["y"])
            elif current["name"] == "Orc":
                newEntity = entities.create_orc(current["x"],current["y"])
            elif current["name"] == "Orc Chief":
                newEntity = entities.create_orc_cheif(current["x"],current["y"])
            else:
                newEntity = entities.create_enemy(current["name"],current["x"],current["y"],current["health"],current["char"],current["colour"],current["initiative"],current["description"])
            newEntity.maxhealth = current["maxhealth"]
            newEntity.health = current["health"]
            newEntity.speed = current["speed"]
            newEntity.blocking = current["blocking"]
            newEntity.sentient = True
            newEntity.pickupable = current["pickupable"]
            newEntity.ap = current["ap"]
        else:
            if "pickaxe" in current["name"]:
                newEntity = entities.create_pickaxe(current["name"],current["x"],current["y"],current["health"],current["char"],current["colour"], False)
            elif "healthpotion" in current["name"]:
                newEntity = entities.create_healthpotion(current["name"],current["x"],current["y"],current["health"],current["char"],current["colour"], False, current["healamount"])           
            elif "flower" in current["name"]:
                newEntity = entities.create_ancientflower(current["name"],current["x"],current["y"],current["health"],current["char"],current["colour"], False, current["manaamount"])
            elif "icewall" in current["name"]:
                newEntity = entities.create_IceWall_Spellbook(current["name"],current["x"],current["y"],current["health"],current["char"],current["colour"], False)
            elif "healspell" in current["name"]:
                newEntity = entities.create_HealSpell_Spellbook(current["name"],current["x"],current["y"],current["health"],current["char"],current["colour"], False)
            elif "firewall" in current["name"]:
                newEntity = entities.create_FireWall_Spellbook(current["name"],current["x"],current["y"],current["health"],current["char"],current["colour"], False)
            elif "healthcrystal" in current["name"]:
                newEntity = entities.create_healthcrystal(current["name"],current["x"],current["y"],current["health"],current["char"],current["colour"], False, current["healamount"])
            elif "manacrystal" in current["name"]:
                newEntity = entities.create_manacrystal(current["name"],current["x"],current["y"],current["health"],current["char"],current["colour"], False, current["manaamount"])
            elif "strengthessence" in current["name"]:
                newEntity = entities.create_strengthessence(current["name"],current["x"],current["y"],current["health"],current["char"],current["colour"], False, current["strengthamount"])
            else:
                newEntity = entities.create_generic_item(current["name"],current["x"],current["y"],current["health"],current["char"],current["colour"], False, current["description"])
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
    # delete all the files at the paths to clear the storage. Used when a new game is started or the player dies.
    if os.path.isfile(invpath):
        os.remove(invpath)
    if os.path.isfile(playerpath):
        os.remove(playerpath)
    if os.path.isfile(mappath):
        os.remove(mappath)
    if os.path.isfile(entitypath):
        os.remove(entitypath)
