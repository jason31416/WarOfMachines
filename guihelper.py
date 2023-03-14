import time
import pygame
import pygame_textinput

pygame.init()

sc = pygame.display.set_mode((800, 600))

tick = 0
menu = 0

ft = [pygame.font.SysFont("comic sans", i) for i in range(1, 128)]


def draw_text(txt, clr, pos, sz=24):
    sf = ft[sz].render(txt, False, clr)
    sc.blit(sf, pos)
    return sf.get_rect().move(pos)

sprs = []

sel = (-1, -1)

lst = 0

def rd(x1, y1, x2, y2):
    return "rect", x1//10*10, y1//10*10, (x2//10*10)-(x1//10*10), (y2//10*10)-(y1//10*10)

while True:
    sc.fill((200, 200, 200))
    tm = time.time()
    ky = pygame.key.get_pressed()
    ev = pygame.event.get()

    for i in sprs:
        if i[0] == "rect":
            pygame.draw.rect(sc, (0, 0, 0), (i[1], i[2], i[3], i[4]))
            pygame.draw.rect(sc, (200, 200, 200), (i[1]+1, i[2]+1, i[3]-2, i[4]-2))
        elif i[0] == "txt":
            draw_text("texthere", (0, 0, 0), (i[1], i[2]))

    if sel == (-1, -1) and pygame.mouse.get_pressed()[0] and pygame.key.get_pressed()[pygame.K_t] and tick-lst >= 30:
        sprs.append(("txt", pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]))
        lst = tick
    elif sel == (-1, -1) and pygame.mouse.get_pressed()[0]:
        sel = pygame.mouse.get_pos()
    elif sel != (-1, -1) and not pygame.mouse.get_pressed()[0]:
        if sel[0]<pygame.mouse.get_pos()[0] and sel[1]<pygame.mouse.get_pos()[1]:
            sprs.append(rd(sel[0], sel[1], pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]))
        sel = (-1, -1)

    if pygame.key.get_pressed()[pygame.K_RETURN] and tick-lst >= 30:
        for i in sprs:
            if i[0] == "rect":
                print(f"pygame.draw.rect(sc, (100, 100, 100), ({i[1]}, {i[2]}, {i[3]}, {i[4]}))")
            elif i[0] == "text":
                print(f"draw_text(\"texthere\", (100, 100, 100), ({i[1]}, {i[2]}), sz=24)")


        lst = tick

    if pygame.key.get_pressed()[pygame.K_z] and tick-lst >= 30:
        sprs.pop(-1)

        lst = tick
    if sel != (-1, -1):
        draw_text(f"{pygame.mouse.get_pos()[0]-sel[0]}, {pygame.mouse.get_pos()[1]-sel[1]}", (0, 0, 0), pygame.mouse.get_pos(), 18)
    else:
        draw_text(f"{pygame.mouse.get_pos()}", (0, 0, 0), pygame.mouse.get_pos(), 18)


    for i in ev:
        if i.type == pygame.QUIT:
            exit(0)

    while time.time()-tm<1/30:
        time.sleep(0.001)
    tick += 1
    pygame.display.update()