import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

class cube(object):
    rows = 20
    w = 500
    def __init__(self,start,dirnx=1,dirny=0,color=(255,0,0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color
         
    
    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color, (i*dis+1, j*dis+1, dis-2, dis-2))
        
        if eyes:
            center = dis//2
            radius = 3
            CM1 = (i * dis + center - radius, j * dis + 8)
            CM2 = (i*dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(surface, (0,0,0), CM1, radius)
            pygame.draw.circle(surface, (0,0,0), CM2, radius)

    def drawpizza(self,surface,img):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]
        surface.blit(img,(i*dis+1, j*dis+1))

class snake(object):
    body = []
    turns = {}
    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1

    def move(self):
        pygame.init()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
            keys = pygame.key.get_pressed()
            for key in keys:
                if keys[pygame.K_LEFT]:
                    if self.dirnx != 1 and len(self.body) > 2:
                        self.dirnx = -1
                        self.dirny = 0
                        self.turns[self.head.pos[:]] = [self.dirnx,self.dirny]
                    elif len(self.body) <= 2 and (self.dirnx == 1 or self.dirnx == 0):
                        self.dirnx = -1
                        self.dirny = 0
                        self.turns[self.head.pos[:]] = [self.dirnx,self.dirny]
                    else:
                        continue

                elif keys[pygame.K_RIGHT]:
                    if self.dirnx != -1 and len(self.body) > 2:
                        self.dirnx = 1
                        self.dirny = 0
                        self.turns[self.head.pos[:]] = [self.dirnx,self.dirny]
                    elif len(self.body) <= 2 and (self.dirnx == -1 or self.dirnx == 0):
                        self.dirnx = 1
                        self.dirny = 0
                        self.turns[self.head.pos[:]] = [self.dirnx,self.dirny]
                    else:
                        continue

                elif keys[pygame.K_UP]:
                    if self.dirny != 1 and len(self.body) > 2:
                        self.dirnx = 0
                        self.dirny = -1
                        self.turns[self.head.pos[:]] = [self.dirnx,self.dirny]
                    elif len(self.body) <= 2 and (self.dirny == 1 or self.dirny == 0):
                        self.dirnx = 0
                        self.dirny = -1
                        self.turns[self.head.pos[:]] = [self.dirnx,self.dirny]
                    else:
                        continue

                elif keys[pygame.K_DOWN]:
                    if self.dirny != -1 and len(self.body) > 2:
                        self.dirnx = 0
                        self.dirny = 1
                        self.turns[self.head.pos[:]] = [self.dirnx,self.dirny]
                    elif len(self.body) <= 2 and (self.dirny == -1 or self.dirny == 0):
                        self.dirnx = 0
                        self.dirny = 1
                        self.turns[self.head.pos[:]] = [self.dirnx,self.dirny]
                    else:
                        continue


        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0],turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(p)
            else:
                if c.dirnx == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows-1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows-1: 
                    c.pos = (0,c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows-1:
                    c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows-1)
                else:
                    c.move(c.dirnx, c.dirny)

    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1]+1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)

def drawGrid(w, rows, surface):
    sizeBtwn = w // rows
    x = 0
    y = 0
    for l in range(rows):
        x += sizeBtwn
        y += sizeBtwn

        pygame.draw.line(surface, (35,35,35), (x,0), (x,w))
        pygame.draw.line(surface, (35,35,35), (0,y), (w,y))

def redrawWindow(surface):
    global rows, width, pizza, piz
    surface.fill((35,35,35))
    s.draw(surface)
    pizza.drawpizza(surface,piz)
    drawGrid(width, rows, surface)
    pygame.display.update()

def pizzasnack(rows,item):
    
    positions = item.body
    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
            continue
        else:
            break
    return x, y

def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass

def main():

    pygame.init()
    global rows, width, s, pizza, piz
    width = 500
    rows = 20
    win = pygame.display.set_mode((width,width))
    s = snake((255,0,0),(10,10))
    piz = pygame.image.load('pizza.png')
    pizza = cube(pizzasnack(rows, s))
    flag = True

    clock  = pygame.time.Clock()
    
    while flag:

        pygame.init()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        pygame.time.delay(50)
        clock.tick(10)
        s.move()
        if s.body[0].pos == pizza.pos:
            s.addCube()
            pizza = cube(pizzasnack(rows, s))
            
        
        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z: z.pos, s.body[x+1:])):
                print('Score: ',len(s.body))
                message_box('You lost lol','Your Score : '+str(len(s.body))+'\nPlay again now dumb')
                s.reset((10,10))
                break
        redrawWindow(win)


rows = 0
width = 0
s = 0
snack = 0
pizza = 0

piz = 0
main()  
