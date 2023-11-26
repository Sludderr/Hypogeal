import gamemap

class queuenode():
    def __init__(self):
        self.next = None
        # distance to node
        self.distance = 999
        # estimated distance to end tile
        self.heuristic = 999
        # total of distance to node and distance to end tile
        self.total = 999
        # pointer to corresponding map tile
        self.tile = None
        # pointer to previous tile in visited
        self.parent = None

class visitednode():
    def __init__(self):
        self.next = None
        self.tile = None

def addtoqueue(head,current,x,y,Map,end,visited):
    # Loop through visited list
    
    while visited != None:
        if visited.tile.y == y and visited.tile.x == x:
            # if the current tile has already been visited, return
            return head
        visited = visited.next
    
    temp = head
    if temp == None:
        # if the queue is empty, then this don't loop through, just create new node for it and return the new node as the head.
        temp = queuenode()
        temp.distance = current.distance + 1
        temp.tile = Map[y][x]
        temp.parent = current
        temp.heuristic = eucdist(temp.tile, end)
        temp.total = temp.heuristic + temp.distance
        return temp
    # loop through astar priority queue
    while temp.next != None:
        if temp.tile.y == y and temp.tile.x == x:
            # if the tile is in the queue already and the distance is lower, replace the info with the new route to get to it
            if current.distance <= temp.distance-1:
                temp.distance = current.distance + 1
                temp.parent = current
                temp.total = temp.heuristic + temp.distance
                return head
            else:
                # if the distance is higher, discard it and return
                return head
        temp = temp.next
    
    # not already in queue and hasn't been visited -> create new node and add to queue
    temp.next = queuenode()
    temp.next.distance = current.distance + 1
    temp.next.tile = Map[y][x]
    temp.next.parent = current
    temp.next.heuristic = eucdist(temp.next.tile, end)
    temp.next.total = temp.next.heuristic + temp.next.distance
    return head

def addtovisited(visited, tile):
    # add to head of visited list
    newnode = visitednode()
    newnode.tile = tile
    newnode.next = visited
    return newnode

# Priority function loops through the astar priority queue. It removes and then returns the lowest total heuristic value node and the new head of the list
def priority(head):
    temp = head
    lowest = temp
    # loop through queue
    while temp != None:
        if temp.total < lowest.total:
            # new lowest found
            lowest = temp
        temp = temp.next
    temp = head
    if lowest == head:
        # if the lowest is the head of the queue, return the head.next as the new head. (removed the first item in the queue)
        return lowest,head.next
    while temp.next != lowest:
        # get node before the lowest
        temp = temp.next
    # "skip" the lowest node and return
    temp.next = temp.next.next
    return lowest,head

def eucdist(start,end):
    return (end.x-start.x)**2 + (end.y-start.y)**2

# offsets starting from NorthWest clockwise through to West (y,x)
directlist = [(-1,-1),(-1,0),(-1,+1),(0,+1),(+1,+1),(+1,0),(+1,-1),(0,-1)]

def astar(start,end,Map):
    # create new node for the start tile, initialise queues
    current = queuenode()
    current.distance = 0
    current.tile = start
    queue = current
    visited = None
    found = False
    # while the queue is not empty (no possible routes) or the end tile is not found
    while queue != None and found != True:
        # choose the next tile to visit based on which has the lowest total heuristic
        current,queue = priority(queue)
        curx = current.tile.x
        cury = current.tile.y
        # add to a list of the tiles visited. Important as we don't want to go back on ourselves.
        visited = addtovisited(visited, current.tile)
        for i in range(len(directlist)):
            # if the tile is walkable (the enemy can pass through it)
            if Map[cury+directlist[i][0]][curx+directlist[i][1]].walkable == True:
                if Map[cury+directlist[i][0]][curx+directlist[i][1]] == end:
                    # end tile reached!, we can stop looping
                    found = True
                if Map[cury+directlist[i][0]][curx+directlist[i][1]].occupants == []:
                    # if the tile is empty- no entities blocking it
                    queue = addtoqueue(queue,current,curx+directlist[i][1],cury+directlist[i][0], Map, end, visited)

    # return the route as an array to make it easier to handle outside of this module
    tilelist = []
    if found == True: # if we actually found a possible route
        temp = current
        while temp:
            tilelist.append(temp.tile)
            temp = temp.parent
        return found, tilelist # will return True, and the route constructed
    else:
        return found, tilelist # will return False, and no route
