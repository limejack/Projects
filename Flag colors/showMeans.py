import pygame,sys
from pygame.locals import *
import k_means

def swap(lis,a,b):
    c = lis[a]
    lis[a] = lis[b]
    lis[b] = c
def invert(color):
    return (255-color[0],255-color[1],255-color[2])

HEIGHT = 500
WIDTH  = 500

pygame.init()
screen = pygame.display.set_mode((500,500))
screen.fill((255,255,255))

num_rows = 10

font = pygame.font.SysFont('arial',10)

for k in range(num_rows):
    means,nums = k_means.getMeans(k+1)

    
    for a in range(k):
        for b in range(k):
            if nums[b] < nums[b+1]:
                swap(nums,b,b+1)
                swap(means,b,b+1)

    for i in range(k+1):
        boxWidth = WIDTH/num_rows
        boxHeight = HEIGHT/num_rows
        text = font.render(str(nums[i]),True,invert(means[i]))

        rect = text.get_rect()
        rect.center = ((i+0.5)*boxWidth,(k+0.5)*boxHeight)
        
        pygame.draw.rect(screen,means[i],(i*boxWidth,k*boxHeight,boxWidth,boxHeight))
        screen.blit(text,rect)

        

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
