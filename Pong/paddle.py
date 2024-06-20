import pygame
import Pong.helper as helpers

class paddle:

    def __init__(self,x,y,w,h):
        self.x=x 
        self.y=y 
        self.w=w 
        self.h=h
        self.paddleRect=pygame.Rect(self.x, self.y, self.w, self.h)
    def getTopLeft(self):
        return self.x-self.w/2,self.y+self.h/2
    def getBottomLeft(self):
        return self.x-self.w/2,self.y-self.h/2
    def getTopRight(self):
        return self.x+self.w/2,self.y+self.h/2
    def getBottomRight(self):
        return self.x+self.w/2,self.y-self.h/2
    def setX(self,x):
        self.x=x 
    def setY(self,y):
        self.y=y 
    def setW(self,w):
        self.w=w 
    def setH(self,h):
        self.h=h 
    def setAll(self,x,y,w,h):
        self.x=x 
        self.y=x 
        self.w=w 
        self.h=h 
    def moveDown(self,vel,screen):
        if(self.y<screen.get_height()-self.h):
            self.y+=vel
            return True
    def moveUp(self,vel,screen):
        if(self.y>0):
            self.y-=vel
            return True
    def drawPaddle(self,screen):
        pygame.draw.rect(screen, helpers.BLACK,
                         pygame.Rect(self.x, self.y, self.w, self.h))
        self.paddleRect=pygame.Rect(self.x, self.y, self.w, self.h)
    def movePlayer(self,vel):
        keys=pygame.key.get_pressed()
        if keys[pygame.K_DOWN] and self.y<600:
            self.moveDown(vel)
        if keys[pygame.K_UP] and self.y>0:
            self.moveUp(vel)
    def isatTop(self,height):
        return self.y<height
    def isAtBottom(self,height):
        return self.y>0
