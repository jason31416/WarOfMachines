import socketserver
import socket
import client
import os
import time
import threading
import random

client.init("spacesmc.cn")

splt = "!*(|"
wsize = 100
tick = 0

def getinfo(usr):
    if os.path.exists("dat/"+usr):
        with open("dat/"+usr) as fl:
            rd = fl.read()
        dt = {}
        for i in rd.split("\n"):
            if splt in i:
                dt[i.split(splt)[0]] = i.split(splt)[1]
        return dt
    return {"coins": "0", "tanks": []}

def setinfo(usr, cont):
    with open("dat/"+usr, "w") as fl:
        for i in cont:
            fl.write(f"{i}{splt}{cont[i]}\n")

emptytank = "00000000000000000000000000000000000000000000c000000000000000000000000000000000000"


class tank:
    def __init__(self, s: str, bl=""):
        self.player = bl
        self.tank = [[["0", 0] for j in range(9)] for i in range(9)]
        for i in range(9):
            for j in range(9):
                if s[i*9+j] == "0":
                    self.tank[i][j] = [s[i*9+j], 0]
                elif s[i*9+j] == "c":
                    self.tank[i][j] = [s[i*9+j], 20]

    def to_str(self):
        ret = self.player+":"
        for i in self.tank:
            for j in i:
                ret += f"{j[0]},{j[1]} "
        return ret

class cell:
    def __init__(self, tk: tank=None, tp=0):
        self.tk = tk
        self.tp = tp
        self.mv = (-1, -1)
    def to_str(self):
        if self.tk is None:
            return f"{self.tp}:!n"
        else:
            return f"{self.tp}:"+self.tk.to_str()


world = [[cell() for i in range(wsize)] for i in range(wsize)]

if os.path.exists("dat/world.txt"):
    with open("dat/world.txt") as fl:
        rd = fl.read().split("\n")
    for i in range(wsize):
        for j in range(wsize):
            tmp = rd[i*wsize+j].split(":")
            world[i][j].tp = int(tmp[0])
            if tmp[1] != "!n":
                world[i][j].tk = tank(tmp[2], tmp[1])

def save():
    sv = ""
    for i in world:
        for j in i:
            sv+=j.to_str()+"\n"
    with open("dat/world.txt", "w") as fl:
        fl.write(sv)

"""
0: empty
c: core
"""

class server(socketserver.BaseRequestHandler):
    def recv(self, bufsize=1024):
        return self.request.recv(bufsize).decode("utf-8")

    def send(self, cont):
        return self.request.send(cont.encode("utf-8"))

    def handle(self) -> None:
        dt = self.recv()
        usn = client.istoken(dt)
        if usn == "F" or usn == "" or usn[0] == "!":
            self.request.close()
            return
        if not os.path.exists("dat/"+usn): # new user
            rx, ry = random.randint(0, wsize-1), random.randint(0, wsize-1)
            cnt = 0
            while world[rx][ry].tk is not None and cnt<10000:
                rx, ry = random.randint(0, wsize - 1), random.randint(0, wsize - 1)
                cnt += 1
            if cnt >= 10000:
                self.send("gmfull")
                self.request.close()
            setinfo(usn, {"coin": "0", "lstpos": f"{rx} {ry}"})
            world[rx][ry].tk = tank(emptytank, usn)

        self.send("ok")
        usdt = getinfo(usn) #remember to refresh
        self.recv()
        self.send(usdt["lstpos"])
        try:
            while True:
                dt = self.recv().split(" ")
                if dt[0] == "coin": # todo: handle
                    self.send(usdt["coin"])
                elif dt[0] == "world":
                    if not(0<=int(dt[1])<wsize and 0<=int(dt[2])<wsize):
                        self.send("!out !out")
                    elif world[int(dt[1])][int(dt[2])].tk is not None:
                        self.send(f"{world[int(dt[1])][int(dt[2])].tk.player} {world[int(dt[1])][int(dt[2])].tp}")
                    else:
                        self.send(f"!none {world[int(dt[1])][int(dt[2])].tp}")
                else:
                    self.send("!error")
        except ConnectionResetError:
            pass
        except BrokenPipeError:
            pass


threading.Thread(target=socketserver.ThreadingTCPServer(("0.0.0.0", 43466), server).serve_forever).start()

class executing:
    def update(self):
        pass

while True:
    tk = time.time()

    print(f"\rTick: [{tick}]", end="")

    if tick%120 == 0:
        save()
        print(f"\rTick: [{tick}] saving world...")

    #todo: update
    while time.time()-tk < 0.2: # 5tps
        time.sleep(0.01)
    tick+=1