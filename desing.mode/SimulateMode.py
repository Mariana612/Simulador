import pygame
from pygame.locals import *
import sys


class SimulateMode:
    def __init__(self,screen,clock):
        self.screen = screen
        self.screen.fill([243, 243, 243])
        self.font = pygame.font.SysFont('timesnewroman', 20)
        self.clock = clock

        self.initialCall()

    def initialCall(self):

        # Images

        doge = pygame.image.load("Imgs\\doge.jpg").convert_alpha()

        on = True
        click = False
        while on:
            mx, my = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN and event.button == 1:  # check for left mouse click
                    click = True
                if event.type == MOUSEBUTTONUP:
                    click = False
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):  # leave application
                    on = False
                    pygame.quit()
                    print("\n''''''''''''''''''''''\nOh HEY LOOK SUNNY DOGGO \ndoge loves and suports you, you know? \nnow stop frowning and go bac to work\n'''''''''''''")
                    sys.exit()

            self.screen.blit(doge, (150, 0))
            pygame.display.flip()
