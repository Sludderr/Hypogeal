import math

def distance(playerx, playery, tilex, tiley):
    xdist = playerx - tilex
    ydist = playery - tiley
    answer = math.sqrt((xdist ** 2) + (ydist ** 2))
    return answer



def raydetect(Map, ax, ay, bx, by, grad, firstpass, dx, dy):
    if firstpass == False:
        tempy = ay - 2
        tempx = ax - 2
    else:
        tempy = ay - 1
        tempx = ax - 1
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
                return raydetect(Map, int(ax+1), int(ay+grad), bx, by, grad, False, dx, dy)
            else:
                return raydetect(Map, int(ax-1), int(ay+grad), bx, by, grad, False, dx, dy)
        else:
            dy += math.sqrt(((1 / grad)**2) + 1)
            if ay < by:
                return raydetect(Map, int(ax+(ay/grad)), int(ay+1), bx, by, grad, False, dx, dy)
            else:
                return raydetect(Map, int(ax+(ay/grad)), int(ay-1), bx, by, grad, False, dx, dy)
    return True
