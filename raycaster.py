import math

def distance(playerx, playery, tilex, tiley):
    xdist = playerx - tilex
    ydist = playery - tiley
    answer = math.sqrt((xdist ** 2) + (ydist ** 2))
    return answer



def raydetect(Map, ax, ay, bx, by, grad, firstpass, dx, dy):
    if firstpass == False:
        tempy = int(ay) - 2
        tempx = int(ax) - 2
    else:
        tempy = int(ay) - 1
        tempx = int(ax) - 1
    if Map[tempy][tempx].name == "wall":
        return False
    if tempx == bx:
        if tempy > by:
            for y in range(tempy-by):
                if Map[y + tempy][tempx].name == "wall":
                    return False
        else:
            for y in range(by-tempy):
                if Map[y + tempy][tempx].name == "wall":
                    return False
    elif tempy == by:
        if tempx > bx:
            for x in range(tempx-bx):
                if Map[ay][x + tempx].name == "wall":
                    return False
        else:
            for x in range(bx-tempx):
                if Map[ay][x + tempx].name == "wall":
                    return False

    if firstpass == True:
        grad = (ay - by) / (ax - bx)
        dx = math.sqrt((grad**2) + 1)
        dy = math.sqrt(((1 / grad)**2) + 1)
        
    print("ax = ", ax, ", ay = ", ay, ", bx = ", bx, ", by = ", by, ", dx = ", dx, ", dy = ", dy)
    
    if ax != bx and ay != by:
        if abs(dx) < abs(dy):
            dx += math.sqrt((grad**2) + 1)
            if ax < bx:
                return raydetect(Map, ax+1, ay+grad, bx, by, grad, False, dx, dy)
            else:
                return raydetect(Map, ax-1, ay+grad, bx, by, grad, False, dx, dy)
        else:
            dy += math.sqrt(((1 / grad)**2) + 1)
            if ay < by:
                return raydetect(Map, ax+(ay/grad), ay+1, bx, by, grad, False, dx, dy)
            else:
                return raydetect(Map, ax+(ay/grad), ay-1, bx, by, grad, False, dx, dy)
    return True

def pathdetect(Map, startx, starty, destx, desty):
    while (startx != destx or starty != desty) and Map[starty][startx].name != "wall":
        ndist = distance(startx, starty-1, destx, desty)
        nedist = distance(startx+1, starty-1, destx, desty)
        edist = distance(startx+1, starty, destx, desty)
        sedist = distance(startx+1, starty+1, destx, desty)
        sdist = distance(startx, starty+1, destx, desty)
        swdist = distance(startx-1, starty+1, destx, desty)
        wdist = distance(startx-1, starty, destx, desty)
        nwdist = distance(startx-1, starty-1, destx, desty)
        
        if ndist < nedist and ndist < edist and ndist < sedist and ndist < sdist and ndist < swdist and ndist < wdist and ndist < nwdist:
            starty -= 1
        elif nedist < edist and nedist < sedist and nedist < sdist and nedist < swdist and nedist < wdist and nedist < nwdist:
            starty -= 1
            startx += 1
        elif edist < sedist and edist < sdist and edist < swdist and edist < wdist and edist < nwdist:
            startx += 1
        elif sedist < sdist and sedist < swdist and sedist < wdist and sedist < nwdist:
            starty += 1
            startx += 1
        elif sdist < swdist and sdist < wdist and sdist < nwdist:
            starty += 1
        elif swdist < wdist and swdist < nwdist:
            starty += 1
            startx -= 1
        elif wdist < nwdist:
            startx -= 1
        else:
            starty -= 1
            startx -= 1
            
    if startx != destx or starty != desty:
        print("startx = ", startx, " starty = ", starty, " destx = ", destx, " desty = ", desty)
        return False
    else:
        
        return True
