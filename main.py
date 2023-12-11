import Pong.helper as helper
import Pong.paddle as paddle
import Pong.ball as ball

import pygame
pygame.init()
# region make game window
screen = pygame.display.set_mode((helper.getWidth(), helper.getHeight()), pygame.RESIZABLE)
centerX = screen.get_width() / 2
centerY = screen.get_height() / 2
pygame.display.set_caption("Pong game")
# endregion
# region draw paddles and ball (old code)
player1=paddle.paddle(20,20,30,100);
player1.drawPaddle(screen)
player2=paddle.paddle(750,20,30,100)
player2.drawPaddle(screen)
ball=ball.ball(centerX,centerY,10)
ball.drawBall(screen)
# endregion
# region game loop
isGameRunning = True
clock=pygame.time.Clock()
while isGameRunning:
    pygame.event.get()
    screen.fill(helper.WHITE)
    player1.drawPaddle(screen)
    player2.drawPaddle(screen)
    ball.drawBall(screen)
    pygame.display.update()
    clock.tick(45)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        player1.moveUp(5,screen)
    if keys[pygame.K_DOWN]:
        player1.moveDown(5,screen)
    if keys[pygame.K_w]:
        player2.moveUp(5,screen)
    if keys[pygame.K_s]:
        player2.moveDown(5,screen)
    # player1.movePlayer(5)
    ball.moveBall(screen)
    # for event in pygame.event.get():
    #     if event == pygame.QUIT:
    #         isGameRunning = False
    #     screen.fill(helper.BLUE)
    #     ball.drawStart(screen)
    #     paddle.drawInitial(screen)
    #     pygame.display.flip()
pygame.quit()
# endregion
