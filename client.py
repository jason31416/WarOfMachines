import socket
import time

sk = socket.socket()

def init(addr, port=43456):
    sk.connect((addr, port))

def login(usr, psw):
    sk.send(f"login {usr} {psw}".encode("utf-8"))
    dt = sk.recv(1024).decode("utf-8")
    return dt.split(".")

def register(usr, psw):
    sk.send(f"reg {usr} {psw}".encode("utf-8"))
    dt = sk.recv(1024).decode("utf-8")
    return dt

def getdt(ky):
    sk.send(f"getdt {ky}".encode("utf-8"))
    return sk.recv(1024).decode("utf-8")

def setdt(ky, vl):
    sk.send(f"setdt {ky} {vl}".encode("utf-8"))

def istoken(tkn):
    sk.send(f"token {tkn}".encode("utf-8"))
    return sk.recv(1024).decode("utf-8")

def close():
    sk.send("close".encode("utf-8"))
    sk.close()

if __name__ == '__main__':
    init("0.0.0.0")
    print(login("jason31416", "jason0409"))
    print(istoken(input(">>")))
    close()

