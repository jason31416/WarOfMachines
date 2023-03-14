import socket
import time
import client
import pygame
import pygame_textinput
import threading

pygame.init()

sc = pygame.display.set_mode((800, 600))

tick = 0
menu = 0
cur = 0

client.init("spacesmc.cn")

ft = [pygame.font.SysFont("comic sans", i) for i in range(1, 128)]

usni = pygame_textinput.TextInputVisualizer(font_object=ft[24])
pswi = pygame_textinput.TextInputVisualizer(font_object=ft[24])

gimg = [pygame.transform.scale(pygame.image.load(f"src/gear/{i}.png"), (64, 64)) for i in range(64)]
smgimg = pygame.transform.scale(pygame.image.load(f"src/gear/0.png"), (24, 24))
ssid = ""

curcoins = -1

sk = socket.socket()
try:
    sk.connect(("0.0.0.0", 43465))
except ConnectionRefusedError:
    sk = socket.socket()
    sk.connect(("0.0.0.0", 43466))

class cell:
    def __init__(self, tp, belongs):
        self.tp, self.bl, self.tk = tp, belongs, tick

world = {}
reqs = []
usn = ""
vx, vy = 0, 0

running = True

tptostr = {"0": "Flatland"}

# fixme: test:begin

menu = 1
sk.send(client.login("test", "test")[1].encode("utf-8"))
sk.recv(1024)
sk.send(b"ok")
vx, vy = map(int, sk.recv(1024).decode("utf-8").split(" "))
usn = "test"

# fixme: test:end

def handle_reqs():
    global curcoins
    while True:
        while len(reqs) == 0 and running:
            time.sleep(0.05)
        if not running:
            return
        x = reqs[0]
        reqs.pop(0)
        sk.send(x.encode("utf-8"))
        dt = sk.recv(2048).decode("utf-8")
        if x.split(" ")[0] == "world":
            world[int(x.split(" ")[1]), int(x.split(" ")[2])] = cell(dt.split(" ")[1], dt.split(" ")[0])
        elif x.split(" ")[0] == "coin":
            curcoins = int(dt)

def draw_text(txt, clr, pos, sz=24):
    sf = ft[sz].render(txt, False, clr)
    sc.blit(sf, pos)
    return sf.get_rect().move(pos)

threading.Thread(target=handle_reqs).start()

while running:
    tm = time.time()
    ky = pygame.key.get_pressed()
    ev = pygame.event.get()

    if menu == 0:
        sc.fill((200, 200, 200))
        sc.blit(gimg[tick%64], (500, 100))
        sc.blit(gimg[63-tick%64], (140, 10))

        draw_text("War", (0, 150, 0), (200, 50), 45)
        draw_text("of", (100, 100, 100), (310, 50), 45)
        draw_text("Machines", (0, 0, 0), (360, 50), 45)

        draw_text("Login:", (0, 0, 0), (220, 150), 35)
        draw_text("Username:", (0, 0, 0), (220, 240))
        draw_text("Password:", (0, 0, 0), (220, 300))
        if cur == 0:
            usni.update(ev)
            pswi.cursor_visible = False
        else:
            usni.cursor_visible = False
            pswi.update(ev)
        if ky[pygame.K_RETURN] and cur == 0 and usni.value:
            cur = 1
        elif ky[pygame.K_RETURN] and cur == 1 and pswi.value:
            ret = client.login(usni.value, pswi.value)
            if ret[0] == "usrnotexist":
                while True:
                    pygame.draw.rect(sc, (0, 0, 0), (195, 195, 410, 210), border_radius=10)
                    pygame.draw.rect(sc, (255, 255, 255), (200, 200, 400, 200), border_radius=10)
                    draw_text("This user doesn't exist!", (255, 0, 0), (220, 230), 32)
                    draw_text("Do you want to register?", (0, 0, 0), (260, 270))
                    if draw_text("Yes", (0, 255, 0), (530, 350)).collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) and pygame.mouse.get_pressed()[0]:
                        client.register(usni.value, pswi.value)
                        ret = client.login(usni.value, pswi.value)
                        ssid = ret[1]
                        sk.send(ssid.encode("utf-8"))
                        sk.recv(1024)
                        sk.send(b"ok")
                        vx, vy = map(int, sk.recv(1024).decode("utf-8").split(" "))
                        usn = usni.value
                        menu = 1
                        break
                    if draw_text("No", (255, 0, 0), (230, 350)).collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) and pygame.mouse.get_pressed()[0]:
                        usni.value = ""
                        pswi.value = ""
                        cur = 0
                        break
                    for i in pygame.event.get():
                        if i.type == pygame.QUIT:
                            exit(0)
                    pygame.display.update()
            elif ret[0] == "success":
                ssid = ret[1]
                sk.send(ssid.encode("utf-8"))
                sk.recv(1024)
                sk.send(b"ok")
                usn = usni.value
                vx, vy = map(int, sk.recv(1024).decode("utf-8").split(" "))
                menu = 1
            elif ret[0] == "wrongpsw":
                while True:
                    pygame.draw.rect(sc, (0, 0, 0), (195, 195, 410, 210), border_radius=10)
                    pygame.draw.rect(sc, (255, 255, 255), (200, 200, 400, 200), border_radius=10)
                    draw_text("Wrong password!", (255, 0, 0), (250, 230), 32)
                    if draw_text("Ok", (0, 0, 0), (400, 350)).collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) and pygame.mouse.get_pressed()[0]:
                        usni.value = ""
                        pswi.value = ""
                        cur = 0
                        break
                    for i in pygame.event.get():
                        if i.type == pygame.QUIT:
                            exit(0)
                    pygame.display.update()
            else:
                raise ValueError(ret)

        sc.blit(usni.surface, (350, 240))
        sc.blit(pswi.surface, (350, 300))

    elif menu == 1: # todo: main menu
        sc.fill((255, 255, 255))

        for i in range(int(vx)-2, int(vx)+22):
            for j in range(int(vy)-2, int(vy)+17):
                if (i, j) not in world:
                    reqs.append(f"world {i} {j}")
                    world[i, j] = None
                elif world[i, j] is not None and world[i, j].tk is not None:
                    if world[i, j].bl == usn:
                        pygame.draw.rect(sc, (0, 255, 0), ((i-vx)*40+1, (j-vy)*40+1, 38, 38), border_radius=5)
                    elif world[i, j].bl == "!out":
                        pass
                    elif world[i, j].bl == "!none":
                        pygame.draw.rect(sc, (200, 200, 200), ((i - vx) * 40 + 1, (j - vy) * 40 + 1, 38, 38),
                                         border_radius=5)
                    else:
                        pygame.draw.rect(sc, (255, 0, 0), ((i - vx) * 40 + 1, (j - vy) * 40 + 1, 38, 38),
                                         border_radius=5)
                    if tick - world[i, j].tk >= 240:
                        reqs.append(f"world {i} {j}")
        for i in range(int(vx) - 2, int(vx) + 22):
            for j in range(int(vy) - 2, int(vy) + 17):
                if world[i, j] is not None and world[i, j].bl not in ["!out", "!none"]:
                    if pygame.Rect((i - vx) * 40 + 1, (j - vy) * 40 + 1, 38, 38).collidepoint(pygame.mouse.get_pos()):
                        mx, my = pygame.mouse.get_pos()
                        pygame.draw.rect(sc, (150, 150, 150), (mx, my, 200, 100), border_radius=15)
                        if world[i, j].bl == usn:
                            draw_text("Your tank", (0, 0, 0), (mx+10, my+5), 18)
                            draw_text("Click to view!", (0, 0, 0), (mx+10, my+30), 12) # todo: click to view
                            draw_text(f"Biome: {tptostr[world[i, j].tp]}", (0, 0, 0), (mx+10, my+55), 12)
                        else:
                            draw_text(f"{world[i, j].bl}'s tank", (0, 0, 0), (mx + 10, my + 5), 12)
                            draw_text(f"Biome: {tptostr[world[i, j].tp]}", (0, 0, 0), (mx + 10, my + 55), 12)
        spd = 0.2
        if ky[pygame.K_UP]:
            vy -= spd
        if ky[pygame.K_DOWN]:
            vy += spd
        if ky[pygame.K_LEFT]:
            vx -= spd
        if ky[pygame.K_RIGHT]:
            vx += spd

        if curcoins == -1:
            curcoins = 0
            reqs.append("coin")

        sc.blit(smgimg, (30+draw_text(str(curcoins), (0, 0, 0), (20, 5)).width, 10))


    for i in ev:
        if i.type == pygame.QUIT:
            running = False

    while time.time()-tm<1/30:
        time.sleep(0.001)
    tick += 1
    pygame.display.update()