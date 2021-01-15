import json
import random
import copy
import game

# Macht Random Moves durch die man aber zumindest nicht sofort stirbt.
# Zum Testen
def randomKi(gb,id,n):
    if n == 20:
        return "turn_left"
    l = ["turn_left", "turn_right", "speed_up", "slow_down", "change_nothing"]
    r = random.randint(0,len(l)-1)
    if turnAllowed(gb,id,l[r]):
        return l[r]
    else:
        return randomKi(gb, id, n+1)


# Berechnet min Abstand zu allen anderen Spielern
def minAbstand(gb, id, x, y):
    if x > 999 or y > 999:
        return 0
    l = []
    gb.players[id].getX()
    gb.players[id].getY()
    for pID, player in gb.players.items():
        if pID == id: continue
        else:  l.append(abs( x-player.getX())+abs(y-player.getY()))
    return min(l)

# True wenn man durch den Zug nicht stirbt
# Berechnet nicht mögliche Gegner züge, kollision möglich
def turnAllowed(gb, id, str):
    gb2 = copy.deepcopy(gb)
    gb2.savePlayerTurn(id, str, False)
    gb2.easy_player_turn_resolution(gb2.players[id])
    return gb2.players[id].isAlive


# Anzahl der erreichbaren Felder in n zügen
def reachableTiles(gb, id, depth):
    #print(gb.players[id].getX(),gb.players[id].getY())
    l = ["turn_left","turn_right","speed_up","slow_down","change_nothing"]
    u = [(gb.players[id].getX(),gb.players[id].getY())]
    if depth > 2: return []
    else:
        for zug in l:
            if turnAllowed(gb, id, zug):
                p = copy.deepcopy(gb)
                p.savePlayerTurn(id, zug, False)
                p.easy_player_turn_resolution(p.players[id])
                u = u + reachableTiles(p, id,depth+1)
    return u
