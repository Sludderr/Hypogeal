# Loop through all of the entites and call update if it is their turn
# Each entity has action points. This iterates each tick
def updateturns(entities):
  for i in range(len(entities)):
    if entities[i].sentient == True:
      entities[i].ap += 1
      if entities[i].ap >= entities[i].initiative:
        entities[i].ap = 0
        returncode = entities[i].take_action()
        if returncode == 2:
          return
