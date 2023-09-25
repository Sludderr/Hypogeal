import json
import os

def storeplayer(player):
    playerdata = open(os.path.join("savedata/player","playerdata.json"), "w")
    playerdict = {
        "name": player.name,
        "x": player.x,
        "y": player.y,
        "health": player.health,
        "maxheath": player.maxhealth,
        "mana": player.mana,
        "maxmana": player.maxmana,
        "ap": player.ap
    }
    # vars() for object -> dict auto. Can't have objects inside objects
    x = json.dumps(playerdict)
    playerdata.write(x)
    playerdata.close()

    inventory = player.inventory
    for i in range(len(inventory)):
        itemstring = "item" + str(i) + ".json"
        inventorydata = open(os.path.join("savedata/inventory", itemstring), "w")
        itemdict = vars(inventory[i])
        inventorydata.write(json.dumps(itemdict))
        inventorydata.close()
