import json
import random
import copy
import philipp
import util
from spe_ed_lib import start_rek

from flask import Flask, render_template, Response
server = Flask(__name__)

@server.route("/")

def hello():
    f = open('data.json', 'w+')
    f.write('{"game":[{"0":"dummy"}')
    f.close()
    sp = Spielfeld(6,10,10)
    rd = 0
    while True:

        rd += 1
        # !!!! Ab Hier ist wichtig !!!!
        c = 0
        # geht jeden Spieler einmal durch   
        for player in sp.players:
            # Untere Auszeile auskommentieren, dann spielt Spieler 1 mit Philipps KI
            
            # Macht moves nur wenn noch am Leben
            if sp.players[player].isAlive:
                c = c+1
                #if player == 1: sp.savePlayerTurn(player, philipp.phTurn(sp, player), True)
                if player == 2: 
                    print("game.py cords ",sp.players[2].getX(),sp.players[2].getY())
                    print("game.py direction ",sp.players[2].getDirection())
                    r = start_rek(sp.toDict(), rd)
                    print("bot move:",r)
                    sp.savePlayerTurn(player,r, True)

                else: sp.savePlayerTurn(player,util.randomKi(sp, player,0),True)
        print("--------------------------")
        # !!!!! Wichtig Ende !!!!!!
        # Wenn nur noch ein Spieler am Leben ist, ist es vorbei
        if c < 2:
            break
    
    f = open('data.json', 'a')
    f.write(']}')
    f.close()


    print("check")
    res = Response('{"content": "Hello"}')
    res.headers['Content-type'] = "application/json" 
    return res

@server.route("/render")
def render():
    return render_template('render.html')
    
    
@server.route("/data_json")
def jason():
    f = open('data.json', 'r+')
    data_json = f.read()
    f.close()
    #print(data_json)
    return data_json
    

def game_logic():
    pass

def player1():
    pass

def player2():
    pass

def player3():
    pass

if __name__ == "__main__":
    server.run(host='0.0.0.0')



class Player:
    def __init__(self,x,y,playerID):
        self.playerID = playerID
        self.x = x
        self.y = y
        self.speed = 1
        self.isAlive = True
        self.nextTurn = None
        self.direction = "up" #falsch

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getSpeed(self):
        return self.speed

    def getPlayerID(self):
        return self.playernumber

    def getDirection(self):
        return self.direction

    def kill(self):
        self.isAlive = False

    def setX(self,p,w):
        if p<w and p>0:
            self.x=p
        else:
            self.kill()

    def setY(self,p,h):
        if p < h and p>0:
            self.y = p
        else:
            self.kill()

    # Hier noch berücksichtigt, dass Spieler ausscheiden wenn sie die Geschwindigkeit über 10 erhöhen oder auf 0 verlangsamen
    def speedUp(self):
        if self.speed < 10:
            self.speed = self.speed + 1
        else: self.kill()

    def speedDown(self):
        if self.speed > 1:
            self.speed = self.speed - 1
        else: self.kill()

    def setPlayerID(self,p):
        self.playernumber = p

    def setDirection(self,dir):
        if self.direction == "up":
            if dir == "turn_left":
                self.direction="left"
            if dir == "turn_right":
                self.direction = "right"
            # else FEHLER
        elif self.direction == "down":
            if dir == "turn_right":
                self.direction = "left"
            if dir == "turn_left":
                self.direction = "right"
            # else FEHLER
        elif self.direction == "left":
            if dir == "turn_left":
                self.direction = "down"
            if dir == "turn_right":
                self.direction = "up"
            # else FEHLER
        elif self.direction == "right":
            if dir == "turn_left":
                self.direction = "up"
            if dir == "turn_right":
                self.direction = "down"
            # else FEHLER
        # else FEHLER


class Spielfeld:
    def __init__(self, num_players, width, height):
        r = random.sample(range(0,width),6)
        p = random.sample(range(0,height),6)
        self.width = width
        self.height = height
        self.gameboard = [[0]*self.height for i in range(self.width)]
        self.turn = 0
        self.num_players = num_players
        self.players = {}
        for player_num in range(1, num_players+1):
            self.players[player_num] = Player(r[player_num-1], p[player_num-1], player_num)   # x und y  sind Falsch
            self.update_gameboard({player_num:[((self.players[player_num].getX()),(self.players[player_num].getY()))]})
        self.running = True
        self.winner = None
        with open('data.json','a') as f:
            f.write(',')
            f.write(self.toJason())

    def getTurn(self):
        return self.turn

    def getGameboard(self):
        a = self.gameboard
        #for player in self.players.values():
            #if player.isAlive:
             #   a[player.getY()[player.getX()]] = a[player.getY()[player.getX()]]
           # else: a[player.getY()[player.getX()]] = a[player.getY()[player.getX()]]
        return a


    def getPlayers(self):
        return self.players

    def incTurn(self):
        self.turn = self.turn + 1




    def toJason(self):
        d = {
            "width": self.width,
            "height": self.height,
            "cells": self.getGameboard(),
            "players": {},
            "you": 2, #Stimmt nicht,
            "running": self.running,
            "deadline": "2020-10-01T12:00:00Z"
        }

        for id in range(1, self.num_players+1):
            d['players'][id] = {
                "x": self.players[id].getX(),
                "y": self.players[id].getY(),
                "direction": self.players[id].getDirection(),
                "speed": self.players[id].getSpeed(),
                "active": self.players[id].isAlive,
                "name": "zwei"
            }

        return json.dumps(d)

    def toDict(self):
        d = {
            "width": self.width,
            "height": self.height,
            "cells": self.getGameboard(),
            "players": {},
            "you": 2, #Stimmt nicht,
            "running": self.running,
            "deadline": "2020-10-01T12:00:00Z"
        }

        for id in range(1, self.num_players+1):
            d['players'][str(id)] = {
                "x": self.players[id].getX(),
                "y": self.players[id].getY(),
                "direction": self.players[id].getDirection(),
                "speed": self.players[id].getSpeed(),
                "active": self.players[id].isAlive,
                "name": "zwei"
            }

        return d



    # Wenn Spieler außerhalb vom Spielfeld ist, bekommt er Koordinaten die außerhalb vom Spielfeld sind.
    # b als flag damit icht alles immer in die json kommt, zB vorrausgesehene Züge
    def playTurn(self, b):
        # Rundenzähler hochsetzen
        self.incTurn()
        # Alle Felder die von allen Spielern besucht wurden kommen in dieses Dic
        player_movements = {}
        for id, p in self.players.items():
            if not p.isAlive:
                continue
            else:
                # BEWEGEN ALLER SPIELER (wie funzt das genau)
                player_movements[id] = self.easy_player_turn_resolution(p)

        # update Gameboard according to player movements
        self.update_gameboard(player_movements)

        c = []
        for p in self.players.values():
            if p.isAlive:
                c.append(p.playerID)
        if len(c) == 1:
            self.winner=c[0]
            self.running = False
        if len(c) == 0:
            self.running = False
        for player in self.players.values():
            player.nextTurn = None

        if b:
            with open('data.json','a') as f:
                f.write(',')
                f.write(self.toJason())
        return self.toJason()




    def easy_player_turn_resolution(self, p):
        # Einfachste Art wie Zug aufgelöst wird, an die ich denken kann:
        # Spieler können nur durch Wände sterben die bereits in vorigen Runden entstanden sind, nicht durch Wände in der aktuellen Runde
        # Spieler  bleiben nicht in Wänden stecken, sondern bewegen sich normal weiter, sterben aber wenn sie eine Wand überquert haben (ohne über die Wand gesprungen zu sein). Glaube ich im Spiel beobachtet zu haben
        visited = self.get_visited_fields((p.getX(), p.getY()), p.getDirection(), p.getSpeed())
        really_visited = []
        for x, y in visited:
            if 0 <= x < self.width and 0 <= y < self.height:
                really_visited.append((x, y))
                if self.gameboard[x][y] != 0: p.kill()
            else:
                p.kill()
                break
        # Update die Position des Spielers, letzte besuchte Position
        p.setX(visited[-1][0], self.width)
        p.setY(visited[-1][1], self.height)
        p.nextTurn=None
        return really_visited

    def get_visited_fields(self, start, direction, speed):
        direction_to_vector = {'up':(0, 1), 'down':(0, -1), 'right': (1, 0), 'left': (-1, 0)}
        x, y = start
        dx, dy = direction_to_vector[direction]
        visited = []
        if self.turn%6 == 0:
            visited.append( (x+dx, y+dy) )
            if speed > 1: visited.append(x+speed*dx, y+speed*dy)
        else: 
            for i in range(1, speed+1):
                visited.append( (x+i*dx, y+i*dy))
        return visited

    def update_gameboard(self, player_movements):
        for id, movements in player_movements.items():
            for move in movements:
                if self.gameboard[move[0]][move[1]] == 0:
                    self.gameboard[move[0]][move[1]] = id
                # Falls Feld von mehreren Spielern besucht wurde , setze Wert -1, um es bei der Anzeige vielleicht schwarz zu färben
                else:
                    self.gameboard[move[0]][move[1]] = -1
                    self.players[id].kill() # neu


    def savePlayerTurn(self, id, zug, b):
        # WANDLE JSON IN ID UND ZUG UM
        if self.players[id].nextTurn != None:
            #self.players[id].kill()    #Hab ich mal rausgenommen, es reicht denke ich wenn es einfach ignoriert wird, damit menschliche Spieler die doppelt klicken nicht gekillt werden
            return
        else: self.players[id].nextTurn = zug
        if zug == "turn_left" or "turn_right":
            self.players[id].setDirection(zug)
        elif zug == "speed_up":
            self.players[id].speedUp()
        elif zug == "slow_down":
            self.players[id].speedDown()

        #Grobe Idee
        # Wenn alle züge abgegeben wurden, wird playTurn automatisc aufgerufen
        for player in self.players.values():
            if player.isAlive and player.nextTurn == None:
                return
        self.playTurn(b)
        return self.toJason()

        # elif zug == "change_nothing":
        #  else FEHLER

    def printGameboard(self):
        a = copy.deepcopy(self.gameboard)
        for player in self.players.values():
            if player.isAlive:
                a[player.getX()][player.getY()] = (a[player.getX()][player.getY()])*10
            else:
                a[player.getX()][player.getY()] = (a[player.getX()][player.getY()])*(-10)
        for line in a:
            print(line, "\n")

    def printPlayerPositions(self):
        for player in self.players.values():
            print(player.getX(), player.getY())
