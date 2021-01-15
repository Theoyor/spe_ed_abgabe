import json
import random
import copy
import game
import util



# Philipps KI
def phTurn(gb, id):
    a = []
    p = []
    l = ["turn_left", "turn_right", "speed_up", "slow_down", "change_nothing"]
    for zug in l:
        if util.turnAllowed(gb, id, zug):
            sp = copy.deepcopy(gb)
            sp.savePlayerTurn(id, zug, False)
            p.append(sp.easy_player_turn_resolution(sp.players[id])[-1])
            a.append(len(list(dict.fromkeys(util.reachableTiles(sp, id, 0)))))
        else:
            a.append(0)
            p.append((1000,1000))
    c = 0
    for player in gb.players.values():
        if player.isAlive:
            c = c+1
    #print(a,l[a.index(max(a))])
    for i in range(0,5):
        a[i] = a[i] + (c*util.minAbstand(gb, id, p[i][0], p[i][1])/len(gb.players))

    print(a,l[a.index(max(a))])
    return l[a.index(max(a))]
