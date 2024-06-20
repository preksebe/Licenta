import pygame

BLUE = (118, 171, 223)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
screen_width = 800
screen_height = 600
P1Score = 0
P2Score = 0
p1Hits=0
p2Hits=0

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


def checkCollision(player1, player2, ball):
    if pygame.Rect.colliderect(player1.paddleRect, ball.ballRect):
        ball.xVel *= -1
        setHits("p1")
        # ball.x ball.y

    if pygame.Rect.colliderect(player2.paddleRect, ball.ballRect):
        ball.xVel *= -1
        setHits("p2")



def setScore(player):
    global P1Score, P2Score
    if player == "p1":
        P1Score += 1
    if player == "p2":
        P2Score += 1
def setHits(player):
    global p1Hits, p2Hits
    if player == "p1":
        p1Hits += 1
    if player == "p2":
        p2Hits += 1
def resetHits():
    global p1Hits, p2Hits
    p1Hits=0
    p2Hits=0
def resetScore():
    global P1Score, P2Score
    P1Score = 0
    P2Score = 0


def drawScore(screen):
    font = pygame.font()
    p1Rect = pygame.get()
