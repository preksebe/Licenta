import os

import Pong.helper as helper
import Pong.paddle as paddle
import Pong.ball as Ball
import neat
import pygame
import pickle
import time




class PongGame:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.player1 = paddle.paddle(20, 20, 30, 100)
        self.player2 = paddle.paddle(750, 20, 30, 100)
        self.ball = Ball.ball(100, 100, 10)
    def playAi(self, net):
        clock = pygame.time.Clock()
        run = True
        self.draw_game()
        while run:
            self.screen.fill(helper.BLUE)
            self.player1.drawPaddle(self.screen)
            self.player2.drawPaddle(self.screen)
            pygame.event.get()
            self.ball.drawBall(self.screen)
            PongGame.draw_text(self.screen,helper.P2Score, PongGame.text_font, 150, 20)
            PongGame.draw_text(self.screen,helper.P1Score, PongGame.text_font, helper.getWidth() - 150, 20)
            pygame.display.update()
            clock.tick(45)
            output = net.activate((self.player2.y, abs(
                self.player2.x - self.ball.x), self.ball.y))
            self.ball.moveBall(self.screen)
            helper.checkCollision(self.player1, self.player2, self.ball)
            decision = output.index(max(output))
            if decision == 1:  # AI moves up
                self.player2.moveUp(6, self.screen)
            elif decision == 2:  # AI moves down
                self.player2.moveDown(6, self.screen)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.player1.moveUp(6, self.screen)
            elif keys[pygame.K_s]:
                self.player1.moveDown(6, self.screen)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break
    pygame.init()
    pygame.font.init()
    text_font = pygame.font.SysFont("Arial", 30)
    def draw_text(screen,text, font, x, y):
        img = font.render(str(text), True, helper.BLACK)
        screen.blit(img, (x, y))

    def draw_game(self):

        # region make game window
        screen = pygame.display.set_mode((helper.getWidth(), helper.getHeight()), pygame.RESIZABLE)
        centerX = self.screen.get_width() / 2
        centerY = self.screen.get_height() / 2
        pygame.display.set_caption("Pong game")
        # endregion
        # region draw paddles and ball (old code)
        self.player1 = paddle.paddle(20, centerY, 5, 100)
        self.player1.drawPaddle(screen)
        self.player2 = paddle.paddle(750, centerY, 5, 100)
        self.player2.drawPaddle(screen)
        self.ball = Ball.ball(centerX, centerY, 10)
        self.ball.drawBall(screen)
        # endregion

    # region game loop
    def trainAi(self, genome1, genome2, config):
        clock = pygame.time.Clock()
        maxHits=20
        startTime=time.time()
        net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
        net2 = neat.nn.FeedForwardNetwork.create(genome2, config)
        self.genome1=genome1
        self.genome2=genome2
        isGameRunning = True
        self.draw_game()
        while isGameRunning:
            # noinspection PyUnreachableCode
            if False:
                self.screen.fill(helper.BLUE)
                self.player1.drawPaddle(self.screen)
                self.player2.drawPaddle(self.screen)
                pygame.event.get()
                #clock.tick(45)
                self.ball.drawBall(self.screen)
                PongGame.draw_text(self.screen,helper.P2Score, PongGame.text_font, 150, 20)
                PongGame.draw_text(self.screen,helper.P1Score, PongGame.text_font, helper.getWidth() - 150, 20)
                pygame.display.update()
            self.ball.moveBall(self.screen)
            self.moveAiPaddles(net1,net2)
            helper.checkCollision(self.player1, self.player2, self.ball)
            duration=time.time()-startTime
            if helper.P1Score == 5 or helper.P2Score == 5 or helper.p1Hits>=maxHits or helper.p2Hits>=maxHits:
                helper.resetScore()
                self.calculate_fitness(duration)
                helper.resetHits()
                break
    # endregion
    def calculate_fitness(self,duration):
        self.genome1.fitness+=helper.p1Hits+duration*0.5
        self.genome2.fitness+=helper.p2Hits+duration*0.5

    def moveAiPaddles(self, net1, net2):
            counter=1
            players = [(self.genome1, net1, self.player1, True), (self.genome2, net2, self.player2, False)]
            for(genome,net,paddle,left) in players:
                output1=net1.activate((
                    (self.player1.y, abs(self.player1.x - self.ball.x), self.ball.y)))
                decision1=output1.index(max(output1))
                output2=net2.activate((
                    (self.player2.y, abs(self.player2.x - self.ball.x), self.ball.y)))
                decision2=output2.index(max(output2))
                valid1 = False
                if(genome==self.genome1):
                    if decision1 == 1:
                        valid1 = self.player1.moveUp(6,self.screen)
                       # genome.fitness += 0.3
                    elif decision1 == 2:
                        valid1 = self.player1.moveUp(6,self.screen)
                       # genome.fitness += 0.3
                    if valid1==False:
                        genome.fitness -= 1
                valid2 = False
                if(genome==self.genome2):
                    if decision2 == 1:
                        valid2 = self.player2.moveUp(6,self.screen)
                        #genome.fitness += 0.3
                    elif  decision2 == 2:
                        valid2 = self.player2.moveDown(6,self.screen)
                        #genome.fitness += 0.3

                    if valid2==False:
                        genome.fitness -= 1


def eval_genomes(genomes, config):
    width, height = 700, 500
    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Pong")

    for i, (genome_id1, genome1) in enumerate(genomes):
        print(round(i / len(genomes) * 100), end=" ")
        genome1.fitness = 0
        for genome_id2, genome2 in genomes[min(i + 1, len(genomes) - 1):]:
            genome2.fitness = 0 if genome2.fitness == None else genome2.fitness

            PongGame(win, width, height).trainAi(genome1, genome2, config)
            PongGame(win, width, height).trainAi(genome2, genome1, config)



def run_neat(config):
    #p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-133')
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1))
    winner = p.run(eval_genomes, 20)
    with open("best.pickle", "wb") as f:
        pickle.dump(winner, f)

def test_best_network(config):
    with open("best.pickle", "rb") as f:
        winner = pickle.load(f)
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)

    width, height = 700, 500
    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Pong")
    pong = PongGame(win, width, height)
    pong.playAi(winner_net)

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    #test_best_network(config)
    run_neat(config)

