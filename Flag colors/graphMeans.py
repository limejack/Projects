class Graph():
    def __init__(self,x,y,w,h,x_axis,y_axis,trueGraph=False):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.trueGraph = trueGraph
    def draw(self,colors,means,screen):
        pygame.draw.rect(screen,(0,0,0),(self.x,self.y,self.w,self.h),1)
        width = self.w-10
        height = self.h-10
        sortedMeans = k_means.sortByMeans(means,colors)


        if self.trueGraph == False:
            for i in range(k):
                for color,number in sortedMeans[i]:
                    if number <= 1000:
                        continue
                    pygame.draw.circle(screen,means[i],(width*color[self.x_axis]/255+self.x+5,height*color[self.y_axis]/255+self.y+5),5)
                    pygame.draw.circle(screen,BLACK,(width*color[self.x_axis]/255+self.x+5,height*color[self.y_axis]/255+self.y+5),5,1)
        else:
            total = 0
            for c in colors:
                total += colors[c]
            for color in colors:
                if colors[color] <= 1000:
                    continue

                pygame.draw.circle(screen,color,(width*color[self.x_axis]/255+self.x+5,height*color[self.y_axis]/255+self.y+5),5)
                pygame.draw.circle(screen,BLACK,(width*color[self.x_axis]/255+self.x+5,height*color[self.y_axis]/255+self.y+5),5,1)


import pygame,sys
from pygame.locals import *
import k_means

HEIGHT = 500
WIDTH  = 500
BLACK = (0,0,0)

pygame.init()
screen = pygame.display.set_mode((500,500))
screen.fill((255,255,255))

k = 10

means,nums = k_means.getMeans(k)
colors     = k_means.readFromFile()

RGT = Graph(0,0,250,250,0,1,True)
RG = Graph(250,0,250,250,0,1,False)

BGT = Graph(0,250,250,250,2,1,True)
BG = Graph(250,250,250,250,2,1,False)

RGT.draw(colors,means,screen)
RG.draw(colors,means,screen)
BGT.draw(colors,means,screen)
BG.draw(colors,means,screen)


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()

