import raycaster
import procgeneration
import math

def distance(ax, ay, bx, by):
    xdist = ax - bx
    ydist = ay - by
    answer = math.sqrt((xdist ** 2) + (ydist ** 2))
    return answer

def update_visibility(Map, playerx, playery, width, height,view):
    # iterate through map tiles within the range of the player
    for y in range((view*2)+1):
        for x in range((view*2)+1):
            # set first position in map
            ytemp = playery-view+y
            xtemp = playerx-view+x
            if ytemp > 0 and ytemp < height and xtemp > 0 and xtemp < width:
                # if inside the map
                if distance(playerx, playery, xtemp, ytemp) < view:
                    # if within viewing distance
                    if procgeneration.checkadjacent(Map, width, height, xtemp, ytemp, "wall", "border") == 8 or raycaster.pathdetect(Map, playerx, playery, xtemp, ytemp) == False:
                        # if obscured or inside a wall
                        Map[ytemp][xtemp].rendered = False
                    
                    else:
                        # otherwise render it
                        Map[ytemp][xtemp].rendered = True
                else:
                    Map[ytemp][xtemp].rendered = False
    return Map
