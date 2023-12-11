import Pong.helper as helper
import Pong.paddle as paddle
import Pong.ball as ball

import pygame

pygame.init()
pygame.font.init()
# region make game window
screen = pygame.display.set_mode((helper.getWidth(), helper.getHeight()), pygame.RESIZABLE)
centerX = screen.get_width() / 2
centerY = screen.get_height() / 2
pygame.display.set_caption("Pong game")
# endregion
# region draw paddles and ball (old code)
player1 = paddle.paddle(20, 20, 30, 100)
player1.drawPaddle(screen)
player2 = paddle.paddle(750, 20, 30, 100)
player2.drawPaddle(screen)
ball = ball.ball(centerX, centerY, 10)
ball.drawBall(screen)
# endregion
text_font = pygame.font.SysFont("Arial", 30)


def draw_text(text, font, x, y):
    img = font.render(str(text), True, helper.BLACK)
    screen.blit(img, (x, y))


# region game loop
isGameRunning = True
clock = pygame.time.Clock()
while isGameRunning:
    screen.fill(helper.WHITE)
    player1.drawPaddle(screen)
    player2.drawPaddle(screen)
    pygame.event.get()
    ball.drawBall(screen)
    draw_text(helper.P1Score, text_font, 150, 20)
    draw_text(helper.P2Score, text_font, helper.getWidth() - 150, 20)
    pygame.display.update()
    clock.tick(45)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player1.moveUp(5, screen)
    if keys[pygame.K_s]:
        player1.moveDown(5, screen)
    if keys[pygame.K_UP]:
        player2.moveUp(5, screen)
    if keys[pygame.K_DOWN]:
        player2.moveDown(5, screen)
    # player1.movePlayer(5)
    ball.moveBall(screen)
    helper.checkCollision(player1, player2, ball, screen)
    # for event in pygame.event.get():
    #     if event == pygame.QUIT:
    #         isGameRunning = False
    #     screen.fill(helper.BLUE)
    #     ball.drawStart(screen)
    #     paddle.drawInitial(screen)
    #     pygame.display.flip()
pygame.quit()
# endregion
