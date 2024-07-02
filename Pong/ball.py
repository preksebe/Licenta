import pygame
import Pong.helper as helpers
import math
import random

class ball:

    def __init__(self, x, y, r):
        self.x = x
        self.r = r
        self.y = y
        angle = self._get_random_angle(-70, 70, [0])
        pos = 1 if random.random() < 0.5 else -1
        self.yVel = pos * abs(math.cos(angle) * 7)
        self.xVel =math.sin(angle) * 7
        # self.yVel=20
        # self.xVel=20
        self.ballRect = pygame.Rect(self.x - self.r, self.y - self.r, self.r, self.r)
    def updateRect(self,rect):
        self.ballRect=rect
    def _get_random_angle(self, min_angle, max_angle, excluded):
        angle = 0
        while angle in excluded:
            angle = math.radians(random.randrange(min_angle, max_angle))
        return angle
    def drawBall(self, screen):
        pygame.draw.rect(screen, helpers.BLACK, pygame.Rect(self.x - self.r, self.y - self.r, self.r, self.r))
        # pygame.draw.circle(screen,helpers.BLACK,(self.x,self.y),self.r)

    def moveBall(self, screen):
        upOrDown=random.choice([1,-1])
        if self.y < self.r:
            self.yVel = 7
        if self.y > screen.get_height() - self.r:
            self.yVel = -7
        if self.x <= self.r:
            self.x = screen.get_width() / 2
            self.y = screen.get_height() / 2
            self.yVel = 7*upOrDown
            self.xVel = -7
            helpers.setScore("p1")
        if self.x >= screen.get_width() - self.r:
            self.x = screen.get_width() / 2
            self.y = screen.get_height() / 2
            self.yVel = 7*upOrDown
            self.xVel = 7
            helpers.setScore("p2")

        self.x = self.x + self.xVel
        self.y = self.y + self.yVel
        self.updateRect(pygame.Rect(self.x - self.r, self.y - self.r, self.r, self.r))
