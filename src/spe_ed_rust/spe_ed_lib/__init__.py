from .spe_ed_lib import accept
import json
import timeit
import copy

def start_rek(dictio, turn):
    return jsonToGameState(dictio, turn)


def jsonToGameState(dictio, turn):
    start = timeit.default_timer()
    plays = {}
    for i in range(1, 7):
        
        if str(i) in dictio["players"]:
            plays[str(i)] = dictio["players"][str(i)]
        else:
            plays[str(i)] = {"x":0,
                             "y":0,
                             "direction":"up",
                             "speed":0,
                             "active":False,
                             "name": str(i)
                             }
    for player in plays:
        if plays[player]["direction"] == "up":
            plays[player]["direction"] = 0
        elif plays[player]["direction"] == "right":
            plays[player]["direction"] = 1
        elif plays[player]["direction"] == "down":
            plays[player]["direction"] = 2
        elif plays[player]["direction"] == "left":
            plays[player]["direction"] = 3
    dic = copy.deepcopy(dictio)
    for a in range(0, dic["height"]):
        for b in range(0, dic["width"]):
            if dic["cells"][a][b] != 0:
                dic["cells"][a][b] = 1
    b = ArrayToInt(dic["cells"],dictio["height"],dictio["width"])
    # statt return rust function aufrufen mit den return werten als argumenten
    ret = spe_ed_lib.accept(b[1],b[0],turn,dictio["you"],json.dumps(plays),dictio["width"],dictio["height"])
    stop = timeit.default_timer()
    time = stop-start
    #return time
    if ret == 0:
        return "change_nothing"
    elif ret == 1:
        return "speed_up"
    elif ret == 2:
        return "slow_down"
    elif ret == 3:
        return "turn_right"
    elif ret == 4:
        return "turn_left"
    else:
        print("Incopatible move")
        return "" 


def ArrayToInt(array, h, w):
    columns = ["1"] * w
    rows = []
    s = "1"
    for row in range(h-1,-1,-1):
        for colo in range(w-1,-1,-1):
            s = s + str(array[row][colo])
            columns[colo] = columns[colo] + str(array[row][colo])
        rows.append(int(s, 2))
        s = "1"
    for i in range(len(columns)-1,-1,-1):
        columns[i] = int(columns[i],2)
    columns.reverse()
    rows.reverse()
    return (columns,rows)



jason = '{"width": 10, "height": 10, "cells": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 3, 0, 0, 0, 6, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 4, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 5, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], "players": {"1": {"x": 4, "y": 5, "direction": "left", "speed": 1, "active": true, "name": "zwei"}, "2": {"x": 0, "y": 0, "direction": "left", "speed": 1, "active": false, "name": "zwei"}, "3": {"x": 2, "y": 1, "direction": "right", "speed": 1, "active": true, "name": "zwei"}, "4": {"x": 6, "y": 7, "direction": "left", "speed": 1, "active": true, "name": "zwei"}, "5": {"x": 8, "y": 3, "direction": "left", "speed": 1, "active": true, "name": "zwei"}, "6": {"x": 2, "y": 5, "direction": "up", "speed": 1, "active": true, "name": "zwei"}}, "you": 1, "running": true, "deadline": "2020-10-01T12:00:00Z"}'
print(jsonToGameState(json.loads(jason), 1))
