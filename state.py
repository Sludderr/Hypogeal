import raycaster
import procgeneration

def update_visibility(Map, playerx, playery, width, height):
    for y in range(21):
        for x in range(21):
            ytemp = playery-10+y
            xtemp = playerx-10+x
            if ytemp > 0 and ytemp < height and xtemp > 0 and xtemp < width:
                if raycaster.distance(playerx, playery, xtemp, ytemp) < 10:
                    if procgeneration.checkadjacent(Map, width, height, xtemp, ytemp, "wall", "border") == 8 or raycaster.pathdetect(Map, playerx, playery, xtemp, ytemp) == False:
                        Map[ytemp][xtemp].rendered = False
                    #elif raycaster.raydetect(Map, playerx, playery, xtemp, ytemp, 0, True, 0, 0) == True:
                        #Map[ytemp][xtemp].rendered = True
                    else:
                        Map[ytemp][xtemp].rendered = True
                else:
                    Map[ytemp][xtemp].rendered = False
    return Map
