from .spe_ed_lib import accept
import json
import timeit
import copy


def start_rek(dictio, turn, deadlineTicks):
    # Erstelle neues Dictionary mit den Playern
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
    # Überschreibe alle Einträge in cells mit Einsen
    dic = copy.deepcopy(dictio)
    for a in range(0, dic["height"]):
        for b in range(0, dic["width"]):
            if dic["cells"][a][b] != 0:
                dic["cells"][a][b] = 1
    b = ArrayToInt(dic["cells"],dictio["height"],dictio["width"])
    # Führe Rustcode aus
    ret = spe_ed_lib.accept(b[1],b[0],turn,dictio["you"],json.dumps(plays),dictio["width"],dictio["height"], deadlineTicks)
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


# Wandelt das cells Array in zwei Bitboards um, eins enthält alle Zeilen, das andere alle Reihen
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
    rows.reverse()
    return (columns,rows)

