import json
import random
import copy
import game
import util

height = 10
width = 10


def minMax(maxPlayer, minPlayer, depth, a, b, max2, gameState):
    moves = ["turn_left", "turn_right", "speed_up", "slow_down", "change_nothing"]
    if depth == 0:
        return spielstandBewertung(gameState)
    if max:
        maxMove = -1000
        for move in moves:
                maxMove = max(maxMove, minMax(maxPlayer, minPlayer, depth-1, a, b, False, updateGameboard(gameState, move, maxPlayer)))
                a = max(a, maxMove)
                if a >= b:
                    break
        return maxMove
    else:
        minMove = 1000
        for move in moves:
                minMove = min(minMove,minMax(maxPlayer, minPlayer, depth-1, a, b, True, updateGameboard(gameState, move, minPlayer)))
                b = min(a, minMove)
                if a <= b:
                    break
        return minMove


def multiMiniMax(maxPlayer, minPlayers, depth, gameState):
    moves = ["turn_left", "turn_right", "speed_up", "slow_down", "change_nothing"]
    moveToMake = 0
    maxMove = -1000
    a = -1000
    for move in moves:
            minMove = 1000
            b = 1000
            for minPlayer in minPlayers:
                minMove = min(minMove, minMax(maxPlayer, minPlayer, depth-1, a, b, False, updateGameboard(gameState, moves, maxPlayer)))
                b = minMove
                if a <= b:
                    break
            if minMove >= maxMove:
                moveToMake = move
                maxMove = minMove
                a = maxMove
    return moveToMake


def jsonToGameState(json, turn):
    j = json.loads(json)
    gameState = {}
    b = ArrayToInt(j["cells"],j["height"],j["width"])
    gameState["rows"] = b[1]
    gameState["columns"] = b[0]
    gameState["deadline"] = j["deadline"]
    gameState["maxPlayer"] = j["you"]
    gameState["players"] = j["players"]
    gameState["turn"] = turn
    return gameState


def jsonToGameState2(dictio, turn, h, w):
    j = dictio
    gameState = {}
    p = j["cells"]
    for a in range(0, h):
        for b in range(0, w):
            if p[a][b] != 0:
                p[a][b] = 1
    b = ArrayToInt(p,j["height"],j["width"])
    gameState["rows"] = b[1]
    gameState["columns"] = b[0]
    gameState["deadline"] = j["deadline"]
    gameState["maxPlayer"] = j["you"]
    gameState["players"] = j["players"]
    gameState["turn"] = turn
    return gameState


def ArrayToInt(array, h, w):
    columns = ["1"] * w
    rows = []
    s = "1"
    for row in range(0,h):
        for colo in range(0,w):
            s = s + str(array[row][colo])
            columns[colo] = columns[colo] + str(array[row][colo])
        rows.append(int(s, 2))
        s = "1"
    for i in range(0,len(columns)):
        columns[i] = int(columns[i],2)
    return (columns,rows)


def updateGameboard(gameState, move, id):
    direction = gameState["players"][id]["direction"]
    speed = gameState["players"][id]["speed"]
    y = gameState["players"][id]["y"]
    x = gameState["players"][id]["x"]
    rows = gameState["rows"]
    columns = gameState["columns"]
    if (direction == "left" and move == "turn_right") or (direction == "right" and move == "turn_left"):
        direction = "up"
    elif (direction == "right" and move == "turn_right") or (direction == "left" and move == "turn_left"):
        direction = "down"
    elif (direction == "down" and move == "turn_right") or (direction == "up" and move == "turn_left"):
        direction = "left"
    elif (direction == "up" and move == "turn_right") or (direction == "down" and move == "turn_left"):
        direction == "right"
    elif move == "speed_up":
        speed = speed+1
    elif move == "slow_down":
        speed = speed-1
    dead = False

    if gameState["turn"] % 6 != 0:
        if direction == "up":
            invY = columns[gameState["players"][id]["x"]].bit_length() - y - 2
            for i in range(invY + 1, invY + speed + 1):
                if columns[gameState["players"][id]["x"]] >> i << columns[gameState["players"][id]["x"]].bit_length() - 1 == 0:
                    columns[gameState["players"][id]["x"]] = columns[gameState["players"][id]["x"]] + 2 ^ i
                else:
                    dead = True
            rowLength = gameState["rows"][0].bit_length()
            for i in range(y - 1, y - speed - 1):
                if gameState["rows"][i] << gameState["players"][id]["y"] >> rowLength - 1 == 0:
                    rows[i] = rows[i] + 2 ^ y
            y = y - speed


        elif direction == "down":
            invY = columns[gameState["players"][id]["x"]].bit_length() - y -2
            rowLength = gameState["rows"][0].bit_length()
            for i in range(invY - 1, invY - speed - 1):
                if columns[gameState["players"][id]["x"]] >> i << columns[gameState["players"][id]["x"]].bit_length() - 1 == 0:
                    columns[gameState["players"][id]["x"]] = columns[gameState["players"][id]["x"]] + 2 ^ i
                else:
                    dead = True
            for i in range(y + 1, y + speed + 1):
                if i < rowLength and gameState["rows"][i] << gameState["players"][id]["y"] >> rowLength == 0:
                    rows[i] = rows[i] + 2 ^ y
            print("\n")
            y = y + speed

        elif direction == "left":
            invX = rows[gameState["players"][id]["y"]].bit_length() - x -2
            for i in range(invX+1, invX+speed+1):
                if rows[gameState["players"][id]["y"]] == 0 or rows[gameState["players"][id]["y"]] >> i << rows[gameState["players"][id]["y"]].bit_length() - 1 == 0:
                    rows[gameState["players"][id]["y"]] = rows[gameState["players"][id]["y"]] + 2 ^ i
                else:
                    dead = True
            coloLength = gameState["columns"][0].bit_length()
            for i in range(x-1,x-speed-1):
                if gameState["columns"][i] << gameState["players"][id]["y"] >> coloLength - 1 == 0:
                    columns[i] = columns[i] + 2 ^ y
            x = x - speed

        elif direction == "right":
            invX = rows[gameState["players"][id]["y"]].bit_length() - x -2
            for i in range(invX-1, invX - speed - 1):
                if rows[gameState["players"][id]["y"]] >> i << rows[gameState["players"][id]["y"]].bit_length()-1 == 0:
                    rows[gameState["players"][id]["y"]] = rows[gameState["players"][id]["y"]] + 2^i
                else:
                    dead = True
            coloLength = gameState["columns"][0].bit_length()
            for i in range(x+1,x+speed+1):
                if gameState["columns"][i] << gameState["players"][id]["y"] >> coloLength == 0:
                     columns[i] = columns[i] + 2 ^ y
            x = x + speed
    else:
        f1 = (0,0)
        f2 = (0,0)
        if direction == "up":
            f1 = (x, y - 1)
            f2 = (x, y-speed)
            y = y - speed
        elif direction == "down":
            f1 = (x, y + 1)
            f2 = (x, y + speed)
            y = y + speed
        elif direction == "left":
            f1 = (x - 1, y)
            f2 = (x - speed, y)
            x = x - speed
        else:
            f1 = (x + 1, y)
            f2 = (x + speed, y)
            x = x + speed
        if f1 != f2:
            c = columns[f1[0]] << f1[1] >> columns.bit_length() -1
            if c != 0:
                dead = True
            else:
                columns[f1[0]] = columns[f1[0]] + 2 ^ f1[0]
                rows[f1[1]] = rows[f1[1]] + 2 ^ f1[1]
        c = columns[f2[0]] << f2[1] >> columns[f2[0]].bit_length() -1
        if c != 0:
            dead = True
        else:
            columns[f2[0]] = columns[f2[0]] + 2 ^ f2[0]
            rows[f2[1]] = rows[f2[1]] + 2 ^ f2[1]


    dicti = {}
    for player in gameState["players"]:
        if player != id:
            dicti[player] = gameState["players"][player]
    dicti[id] = {
        "x" : x,
        "y" : y,
        "direction" : direction,
        "speed" : speed,
        "active" : not dead,
        "name" : gameState["players"][id]["name"]
    }
    dictio = {x: gameState[x] for x in gameState if x == "deadline" or "maxPlayer"}
    dictio["players"] = dicti
    dictio["rows"] = rows
    dictio["columns"] = columns
    dictio["turn"] = gameState["turn"] + 0.5
    return dictio


def spielstandBewertung(gameState):
   return random.randint(0, 50)














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
    for i in range(0,5):
        a[i] = a[i] + (c*util.minAbstand(gb, id, p[i][0], p[i][1])/len(gb.players))

    return l[a.index(max(a))]

def searchArray(ar, heigth, width):
    # (oben,unten,links,rechts)
    ar2 = [[(0,0,0,0)] * heigth for i in range(width)]
    for r in range(0,width-1):
        length = 0
        for c in range(0,heigth-1):
            if ar[r][c] != 0:
                if length == 0:
                    continue
                else:
                    fillRowFields(ar,r,c,length)
                    length = 0
            else:
                length = length + 1

    for c in range(0,heigth-1):
        length = 0
        for r in range(0,width-1):
            if ar[r][c] != 0:
                if length == 0:
                    continue
                else:
                    fillColoFields(ar,r,c,length)
                    length = 0
            else:
                length = length + 1



def fillRowFields(array,r,c,length):
    l = length
    revL = 0
    for i in range(c,c-length):
        array[r][i] = (array[r][i][0],array[r][i][1],l,revL)
        l = l-1
        revL = revL+1




def fillColoFields(array,r,c,length):
    l = length
    revL = 0
    for i in range(r,r-length):
        array[i][c] = (array[i][c][0],array[i][c][0],l,revL)
        l = l-1
        revL = revL+1

jason = {"width": 10, "height": 10, "cells": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 4, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 5, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], "players": {"1": {"x": 4, "y": 5, "direction": "left", "speed": 1, "active": True, "name": "zwei"}, "2": {"x": 0, "y": 0, "direction": "left", "speed": 1, "active": False, "name": "zwei"}, "3": {"x": 2, "y": 1, "direction": "right", "speed": 1, "active": True, "name": "zwei"}, "4": {"x": 6, "y": 7, "direction": "left", "speed": 1, "active": True, "name": "zwei"}, "5": {"x": 8, "y": 3, "direction": "left", "speed": 1, "active": True, "name": "zwei"}, "6": {"x": 2, "y": 5, "direction": "up", "speed": 1, "active": True, "name": "zwei"}}, "you": 1, "running": True, "deadline": "2020-10-01T12:00:00Z"}

j = jsonToGameState2(jason, 6, height, width)
print(multiMiniMax("1", ["6", "2", "3", "4", "5"], 4, j))





