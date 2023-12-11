import pygame
import Pong.helper as helpers


class ball:
    def __init__(self, x, y, r):
        self.x = x
        self.r = r
        self.y = y
        self.yVel = 2
        self.xVel = 2
        self.ballRect = pygame.Rect(self.x - self.r, self.y - self.r, self.r, self.r)
    def updateRect(self,rect):
        self.ballRect=rect

    def drawBall(self, screen):
        pygame.draw.rect(screen, helpers.BLACK, pygame.Rect(self.x - self.r, self.y - self.r, self.r, self.r))
        # pygame.draw.circle(screen,helpers.BLACK,(self.x,self.y),self.r)

    def moveBall(self, screen):
        if self.y < self.r:
            self.yVel = 2
        if self.y > screen.get_height() - self.r:
            self.yVel = -2
        if self.x <= self.r:
            self.x = screen.get_width() / 2
            self.y = screen.get_height() / 2
            self.yVel = 2
            self.xVel = 2
            helpers.setScore("p1")
        if self.x >= screen.get_width() - self.r:
            self.x = screen.get_width() / 2
            self.y = screen.get_height() / 2
            self.yVel = 2
            self.xVel = -2
            helpers.setScore("p2")

        self.x = self.x + self.xVel
        self.y = self.y + self.yVel
        self.updateRect(pygame.Rect(self.x - self.r, self.y - self.r, self.r, self.r))
