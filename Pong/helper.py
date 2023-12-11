import pygame

BLUE = (118, 171, 223)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
screen_width = 800
screen_height = 600
P1Score = 0
P2Score = 0


def getWidth():
    return screen_width


def setWidth(width):
    global screen_width
    screen_width = width


def getHeight():
    return screen_height


def setHeight(height):
    global screen_height
    screen_height = height


def checkCollision(player1, player2, gameBall, screen):
    if pygame.Rect.colliderect(player1.paddleRect, gameBall.ballRect):
        gameBall.xVel = 2
    if pygame.Rect.colliderect(player2.paddleRect, gameBall.ballRect):
        gameBall.xVel = -2


def setScore(player):
    global P1Score, P2Score
    if player == "p1":
        P1Score += 1
    if player == "p2":
        P2Score += 1


def resetScore():
    global P1Score, P2Score
    P1Score = 0
    P2Score = 0


def drawScore(screen):
    font = pygame.font()
    p1Rect = pygame.get()
