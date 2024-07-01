import pygame
from pygame.locals import *
import math as m

game_name = ("DEFAULT_V1")

pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)

win_width, win_height = (700, 500)
fps = 60 # yes
display = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption(game_name)
clock = pygame.time.Clock()

environment = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
]
fov = 60
xpos, ypos = (1, 1)
rot_r = 0
minimap = 1

if minimap == 1 :
	for path in environment:
		text_surface = my_font.render("hi", False, (0, 0, 0))
text_surface = my_font.render("hi", False, (0, 0, 0))
display.blit(text_surface, (0,0))

testmarker = pygame.image.load("testmarker.png").convert()

lookup = 2

display.blit(testmarker, (0, 0))
pygame.display.flip()

sensitivity = m.pi/256
move_speed = 0.02

precision = 0.02

wk, sk, ak, dk, rk, lk = False, False, False, False, False, False

run = True
while run:
    display.blit(testmarker, (0, 0))
    text_surface = my_font.render("cone engine v1", False, (0, 0, 0))
    display.blit(text_surface, (400,0))

    pygame.display.flip()
    clock.tick(fps)
    pygame.display.update()
    pygame.display.set_caption(game_name + " - FPS: " + str(round(clock.get_fps())))

    for e in pygame.event.get():
        if e.type == QUIT:
            run = False
        
        if e.type == KEYDOWN:
            if e.key == pygame.K_w:
                wk = True
            if e.key == pygame.K_s:
                sk = True
            if e.key == pygame.K_LEFT:
                ak = True
            if e.key == pygame.K_RIGHT:
                dk = True
            if e.key == pygame.K_DOWN:
                rk = True
            if e.key == pygame.K_UP:
                lk = True
        if e.type == KEYUP:
            if e.key == pygame.K_w:
                wk = False
            if e.key == pygame.K_s:
                sk = False
            if e.key == pygame.K_LEFT:
                ak = False
            if e.key == pygame.K_RIGHT:
                dk = False
            if e.key == pygame.K_DOWN:
                rk = False
            if e.key == pygame.K_UP:
                lk = False

    x, y = (xpos, ypos)
    if wk == True:
        x, y = (x+move_speed*m.cos(rot_r), y+move_speed*m.sin(rot_r))
    if sk == True:
        x, y = (x-move_speed*m.cos(rot_r), y-move_speed*m.sin(rot_r))
    if ak == True:
        rot_r -= sensitivity
    if dk == True:
        rot_r += sensitivity
    if rk == True:
        lookup += (sensitivity*3)
    if lk == True:
        lookup -= (sensitivity*3)
    if environment[int(x)][int(y)] == 0:
        xpos, ypos = (x, y)
    if lookup == 0:
        lookup = 1

    display.fill((191, 200, 224))

    for i in range(fov+1):
        rot_d = float(rot_r + m.radians(i - fov/2))
        x, y = (xpos, ypos)
        sin, cos = (precision*m.sin(rot_d), precision*m.cos(rot_d))
        j = 0
        while True:
            x, y = (x + cos, y + sin)
            j += 1
            if environment[int(x)][int(y)] != 0:
                tile = environment[int(x)][int(y)]
                d = j
                j = j * m.cos(m.radians(i-fov/2))
                height = (7/j * 2400)
                break
        if d/2 > 255:
            d = 510
        pygame.draw.line(display,
                         (255-d/2, 255-d/2, 255-d/2), # color
                         (i*(win_width/fov), (win_height/lookup) + height), # pos 1
                         (i*(win_width/fov), (win_height/lookup) - height), # pos 2
                         width=int(win_width/fov))
