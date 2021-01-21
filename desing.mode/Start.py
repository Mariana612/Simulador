import sys
import pygame
from DesignMode import DesignMode
from pygame.locals import *

pygame.init()


class Start:
    def __init__(self):
        self.screen = pygame.display.set_mode((1000, 600))
        self.screen.fill([243, 243, 243])
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Simulador')
        self.font = pygame.font.SysFont('timesnewroman', 36)

        self.initialCall()

    def initialCall(self):

        # Images
        logo = pygame.image.load("Imgs\\logo.png").convert_alpha()
        bg = pygame.image.load("Imgs\\bg.png").convert_alpha()
        design_rect = pygame.Rect((440, 255, 150, 50))
        import_rect = pygame.Rect((440, 400, 150, 50))
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
                    sys.exit()

            Design = self.font.render('Design', True, (243, 243, 243))
            Import = self.font.render('Import', True, (243, 243, 243))

            self.screen.blit(bg, (0, 0))
            rectangle = pygame.draw.rect(self.screen, (81, 125, 164), (440, 255, 150, 50))
            rectangle = pygame.draw.rect(self.screen, (81, 125, 164), (440, 400, 150, 50))

            self.screen.blit(Design, (464, 255))
            self.screen.blit(Import, (464, 400))

            self.screen.blit(logo, [250, 70])
            pygame.display.flip()

            if design_rect.collidepoint((mx, my)) and click:
                DesignMode(self.screen, self.clock)
                on = False

            if import_rect.collidepoint((mx, my)) and click:
                on = False


start = Start()
