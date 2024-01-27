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
    def test_ai(self, net):
        """
        Test the AI against a human player by passing a NEAT neural network
        """
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
            helper.checkCollision(self.player1, self.player2, self.ball, self.screen)
            decision = output.index(max(output))
            if decision == 1:  # AI moves up
                self.player2.moveUp(8, self.screen)
            elif decision == 2:  # AI moves down
                self.player2.moveDown(8, self.screen)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.player1.moveUp(8, self.screen)
            elif keys[pygame.K_s]:
                self.player1.moveDown(8, self.screen)

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
        self.player1 = paddle.paddle(20, 20, 30, 100)
        self.player1.drawPaddle(screen)
        self.player2 = paddle.paddle(750, 20, 30, 100)
        self.player2.drawPaddle(screen)
        self.ball = Ball.ball(centerX, centerY, 10)
        self.ball.drawBall(screen)
        # endregion

    # region game loop
    def trainAi(self, genome1, genome2, config):
        maxHits=20
        startTime=time.time()
        net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
        net2 = neat.nn.FeedForwardNetwork.create(genome2, config)
        self.genome1=genome1
        self.genome2=genome2
        isGameRunning = True
        clock = pygame.time.Clock()
        self.draw_game()
        while isGameRunning:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True
            # sa scot astea separat
            self.screen.fill(helper.BLUE)
            self.player1.drawPaddle(self.screen)
            self.player2.drawPaddle(self.screen)
            pygame.event.get()
            self.ball.drawBall(self.screen)
            PongGame.draw_text(self.screen,helper.P2Score, PongGame.text_font, 150, 20)
            PongGame.draw_text(self.screen,helper.P1Score, PongGame.text_font, helper.getWidth() - 150, 20)
            self.moveAiPaddles(net1,net2)

            keys = pygame.key.get_pressed()
            # if keys[pygame.K_w]:
            #     player1.moveUp(5, screen)
            # if keys[pygame.K_s]:
            #     player1.moveDown(5, screen)
            # if keys[pygame.K_UP]:
            #     player2.moveUp(5, screen)
            # if keys[pygame.K_DOWN]:
            #     player2.moveDown(5, screen)
            # # player1.movePlayer(5)
            self.ball.moveBall(self.screen)
            helper.checkCollision(self.player1, self.player2, self.ball, self.screen)
            pygame.display.update()


            gameLength=time.time()-startTime
            if helper.P1Score == 1 or helper.P2Score == 1 or helper.p1Hits>=maxHits or helper.p2Hits>=maxHits:
                helper.resetScore()
                self.calculate_fitness(gameLength)
                break
    # endregion
    def calculate_fitness(self,length):
        self.genome1.fitness+=helper.p1Hits
        self.genome2.fitness+=helper.p2Hits
        helper.resetHits()
    def moveAiPaddles(self, net1, net2):
            """
            Determine where to move the left and the right paddle based on the two
            neural networks that control them.
            """
            counter=1
            players = [(self.genome1, net1, self.player1, True), (self.genome2, net2, self.player2, False)]
            for(genome,net,paddle,left) in players:
                output1=net1.activate((
                    (self.player1.y, abs(self.player1.x - self.ball.x), self.ball.y)))
                decision1=output1.index(max(output1))
                output2=net2.activate((
                    (self.player2.y, abs(self.player2.x - self.ball.x), self.ball.y)))
                decision2=output2.index(max(output2))
                valid1 = True
                if(genome==self.genome1):
                    if decision1 == 0:  # Don't move
                        genome.fitness -= 0.01  # we want to discourage this
                    elif decision1 == 1:  # Move up
                        valid1 = self.player1.moveUp(6,self.screen)
                    else:  # Move down
                        valid1 = self.player1.moveDown(6,self.screen)

                    if not valid1:  # If the movement makes the paddle go off the screen punish the AI
                        genome.fitness -= 1

                valid2 = True
                if(genome==self.genome2):
                    if decision2 == 0:  # Don't move
                        genome.fitness -= 0.01  # we want to discourage this
                    elif decision2 == 1:  # Move up
                        valid2 = self.player2.moveUp(6,self.screen)
                    else:  # Move down
                        valid2 = self.player2.moveDown(6,self.screen)

                    if not valid2:  # If the movement makes the paddle go off the screen punish the AI
                        genome.fitness -= 1


def eval_genomes(genomes, config):
    """
    Run each genome against eachother one time to determine the fitness.
    """
    width, height = 700, 500
    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Pong")

    for i, (genome_id1, genome1) in enumerate(genomes):
        print(round(i / len(genomes) * 100), end=" ")
        genome1.fitness = 0
        for genome_id2, genome2 in genomes[min(i + 1, len(genomes) - 1):]:
            genome2.fitness = 0 if genome2.fitness == None else genome2.fitness
            pong = PongGame(win, width, height)

            force_quit = pong.trainAi(genome1, genome2, config)
            if force_quit:
                quit()


def run_neat(config):
    #p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-49')
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1))

    winner = p.run(eval_genomes, 8)
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
    pong.test_ai(winner_net)

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    ##test_best_network(config)
    run_neat(config)

