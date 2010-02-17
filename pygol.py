#!/usr/bin/python

import pygame,sys,time
from pygame.locals import *
from numpy.numarray import *

width = 1024
height = 768
resolution = 16

class Field():
    def __init__(self):
        self.x = width // resolution
        self.y = height // resolution
        self.res = resolution
        self.height = height
        self.width = width
        self.m = zeros([self.x,self.y], Int)

    def update(self):
        screen.fill((0,0,0,255))
        for i in range(self.x - 1):
            pygame.draw.line(screen, lines, ((i+1)*self.res, 0), ((i+1)*self.res, self.height))
        for i in range(self.y - 1):
            pygame.draw.line(screen, lines, (0, (i+1)*self.res), (self.width, (i+1)*self.res))
        for i in range(self.y):
            for j in range(self.x):
                if(self.m[j][i] == 1):
                    self.draw_cell((j,i))
        pygame.display.flip()

    def add_cell(self, pos_c):
        pos_f = (pos_c[0] // self.res , pos_c[1] // self.res)
        self.m[pos_f[0]][pos_f[1]] = 1

    def draw_cell(self, pos_f):
        start = (pos_f[0] * self.res + 1, pos_f[1] * self.res + 1)
        pygame.draw.rect(screen, white, ( start, (self.res - 1, self.res - 1) ) )

    def evolve(self):
        tmp = zeros([self.x, self.y], Int)
        for i in range(self.y):
            for j in range(self.x):
                tl = (j-1,i-1)
                tm = (j, i-1)
                tr = (j+1, i-1)
                ml = (j-1, i)
                mr = (j+1, i)
                bl = (j-1, i+1)
                bm = (j, i+1)
                br = (j+1, i+1)
                if(i-1 < 0):
                    tl = (tl[0],self.y - 1)
                    tm = (tm[0],self.y - 1)
                    tr = (tr[0],self.y - 1)
                if(i+1 > self.y - 1):
                    bl = (bl[0],0)
                    bm = (bm[0],0)
                    br = (br[0],0)
                if(j-1 < 0):
                    tl = (self.x - 1, tl[1]) 
                    ml = (self.x - 1, ml[1])
                    bl = (self.x - 1, bl[1])
                if(j+1 > self.x - 1):
                    tr = (0, tr[1])
                    mr = (0, mr[1])
                    br = (0, br[1])
                a = self.m[tl[0]][tl[1]] + self.m[tm[0]][tm[1]] + self.m[tr[0]][tr[1]] + self.m[ml[0]][ml[1]] + self.m[mr[0]][mr[1]] + self.m[bl[0]][bl[1]] + self.m[bm[0]][bm[1]] + self.m[br[0]][br[1]]
                if(self.m[j][i] == 1 and a < 2):
                    tmp[j][i] = 0
                elif(self.m[j][i] == 1 and a > 3):
                    tmp[j][i] = 0
                elif(self.m[j][i] == 1 and (a == 2 or a == 3)):
                    tmp[j][i] = 1
                elif(self.m[j][i] == 0 and a == 3):
                    tmp[j][i] = 1
        self.m = tmp
        self.update()

pygame.init()
window = pygame.display.set_mode([width,height])
pygame.display.set_caption('PyGoL')
screen = pygame.display.get_surface()
lines = pygame.Color(64, 64, 64, 255)
white = pygame.Color(255, 255, 255, 255)
black = pygame.Color(0,0,0,255)
field = Field()
field.update()

def mouse_draw(pos):
    field.add_cell(pos)
    field.update()

def input(events):
    for event in events:
        if event.type == KEYDOWN:
            if event.key == 27:
                sys.exit(0)
            elif event.key == 32:
                field.evolve()
        elif(event.type == MOUSEBUTTONDOWN):
            if event.button == 1:
                mouse_draw(event.pos)
        #else:
            #print event

while True:
    input(pygame.event.get())
    time.sleep(0.1)
