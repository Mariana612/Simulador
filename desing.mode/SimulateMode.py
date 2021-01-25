import pygame
from pygame.locals import *
import sys


class SimulateMode:
    def __init__(self,screen,clock,list_pow, list_res):
        self.screen = screen
        self.screen.fill([205,200,200])
        self.font = pygame.font.SysFont('timesnewroman', 20)
        self.clock = clock

        self.list_pow = list_pow
        self.list_res = list_res

        self.initialCall()

    def drawElements(self, mx, my, click):  # Refresh elements in screen
        # Images
        power_img = pygame.image.load("Imgs\\power.png").convert_alpha()
        white_img = pygame.image.load("Imgs\\white.png").convert_alpha()
        res_img = pygame.image.load("Imgs\\resistencia.png").convert_alpha()

        self.screen.blit(white_img, [0, 0])  # Changes Background

        for o in self.list_pow:  # Refresca todos los fuentes de poder
            if (not o.rect.collidepoint((mx, my)) and not click) or (o.rect.collidepoint((mx, my)) and not click):
                o.checkPlacement()
            if o.rotated:
                self.screen.blit(pygame.transform.rotate(power_img, 90), (o.rect.x, o.rect.y))
            else:
                self.screen.blit(power_img, (o.rect.x, o.rect.y))

        for o in self.list_res:  # Refresca todos las resistencias
            if (not o.rect.collidepoint((mx, my)) and not click) or (o.rect.collidepoint((mx, my)) and not click):
                o.checkPlacementRes()
            if o.rotated:
                self.screen.blit(pygame.transform.rotate(res_img, 90), (o.rect.x, o.rect.y))
            else:
                self.screen.blit(res_img, (o.rect.x, o.rect.y))

        pygame.display.flip()

    def initialCall(self):

        # Images
        on = True
        click = False

        while on:
            mx, my = pygame.mouse.get_pos()
            self.drawElements(mx, my, click)

            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN and event.button == 1:  # check for left mouse click
                    click = True
                if event.type == MOUSEBUTTONUP:
                    click = False
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):  # leave application
                    on = False
                    pygame.quit()
                    sys.exit()

            pygame.display.flip()
