import pygame
import sys
from pygame.locals import *
from PowerNode import PowerNode
from ResNode import ResNode

pygame.init()


class Start:
    def __init__(self):
        self.screen = pygame.display.set_mode((1000, 600))
        self.screen.fill([243, 243, 243])
        pygame.display.set_caption('Simulador')
        self.clock = pygame.time.Clock()
        self.list_pow = []
        self.list_res = []
        self.writing = False
        self.pow = False
        self.name_int = False
        self.value_entry = False
        self.font = pygame.font.SysFont('timesnewroman', 20)

        self.designMenu()

    def paintButtons(self, touched1, touched2):
        # Images
        res_img = pygame.image.load("Imgs\\resistencia.png").convert_alpha()
        res_img_on = pygame.image.load("Imgs\\resistenciaOn.png").convert_alpha()
        power_img = pygame.image.load("Imgs\\power.png").convert_alpha()
        power_img_on = pygame.image.load("Imgs\\power_on.png").convert_alpha()
        rectangle_img = pygame.image.load("Imgs\\rectangle.png").convert()

        # Updates buttons
        self.screen.blit(rectangle_img, [772, 62])  # fix transparency
        self.screen.blit(power_img_on if touched1 else power_img, [825, 200])
        self.screen.blit(res_img_on if touched2 else res_img, [845, 330])
        pygame.display.flip()
        self.clock.tick(14)

    def createElement(self, width, height, power):  # parte de class
        # Images
        power_img = pygame.image.load("Imgs\\power.png").convert_alpha()
        res_img = pygame.image.load("Imgs\\resistencia.png").convert_alpha()
        if power:
            element = PowerNode(350, 250, width, height)
            self.list_pow.append(element)
            self.screen.blit(power_img, (element.rect.x, element.rect.y))
            self.changeValues(True)
        else:
            element = ResNode(350, 250, width, height)
            self.list_res.append(element)
            self.screen.blit(res_img, (element.rect.x, element.rect.y))
            self.changeValues(False)

        pygame.display.flip()

    def drawElements(self, mx, my, click):
        power_img = pygame.image.load("Imgs\\power.png").convert_alpha()
        white_img = pygame.image.load("Imgs\\white.png").convert_alpha()
        res_img = pygame.image.load("Imgs\\resistencia.png").convert_alpha()
        self.screen.blit(white_img, [0, 0])

        for o in self.list_pow:
            if (not o.rect.collidepoint((mx, my)) and not click) or (o.rect.collidepoint((mx, my)) and not click):
                o.checkPlacement()
            self.screen.blit(power_img, (o.rect.x, o.rect.y))

        for o in self.list_res:
            if (not o.rect.collidepoint((mx, my)) and not click) or (o.rect.collidepoint((mx, my)) and not click):
                o.checkPlacementRes()
            self.screen.blit(res_img, (o.rect.x, o.rect.y))

        pygame.display.flip()


    def changeValues(self, element):
        blue = pygame.image.load("Imgs\\blueRect.png").convert_alpha()
        self.screen.blit(blue, (217, 194))

        text_surf = self.font.render('Enter Name:', True, (243, 243, 243))

        text_surf2 = self.font.render('Enter Value:', True, (243, 243, 243))

        self.screen.blit(text_surf, (240, 224))
        rectangle = pygame.draw.rect(self.screen, (243, 243, 243), (240, 255, 250, 25))
        self.screen.blit(text_surf2, (240, 290))
        rectangle = pygame.draw.rect(self.screen, (243, 243, 243), (240, 320, 250, 25))
        rectangle = pygame.draw.rect(self.screen, (81, 125, 164), (330, 365, 100, 25))

        self.writing = True
        if element:
            self.pow = True
        else:
            self.pow = False

        pygame.display.flip()

    def designMenu(self):
        # Flags
        on = True
        click = False

        # self.uselessRect()

        while on:
            # Mouse
            mx, my = pygame.mouse.get_pos()
            name_Rect = pygame.Rect((240, 255, 250, 25))
            value_Rect = pygame.Rect((240, 320, 250, 25))
            finish_rect = pygame.Rect((330, 365, 100, 25))

            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN and event.button == 1:  # check for left mouse click
                    click = True

                if event.type == MOUSEBUTTONUP:
                    click = False

                # Code to write stuff and save it in Node, Es una basura de codigo ahorita lo cambio
                if self.writing:
                    if name_Rect.collidepoint((mx, my)) and click:
                        self.name_int = True
                        self.value_entry = False

                    if value_Rect.collidepoint((mx, my)) and click:
                        self.name_int = False
                        self.value_entry = True

                    if event.type == KEYDOWN:
                        if self.name_int:
                            if event.key == pygame.K_BACKSPACE:
                                if self.pow:
                                    self.list_pow[-1].name = self.list_pow[-1].name[:-1]
                                else:
                                    self.list_res[-1].name = self.list_res[-1].name[:-1]
                            else:
                                if self.pow:
                                    if len(self.list_pow[-1].name) < 18:
                                        self.list_pow[-1].name += event.unicode
                                else:
                                    if len(self.list_res[-1].name) < 18:
                                        self.list_res[-1].name += event.unicode

                        if self.value_entry:
                            if event.key == pygame.K_BACKSPACE:
                                if self.pow:
                                    self.list_pow[-1].value = self.list_pow[-1].value[:-1]
                                else:
                                    self.list_res[-1].value = self.list_res[-1].value[:-1]
                            else:
                                if self.pow:
                                    if len(self.list_pow[-1].value) < 18:
                                        try:
                                            int(event.unicode)
                                            self.list_pow[-1].value += event.unicode
                                        except ValueError:
                                            pass
                                else:
                                    if len(self.list_res[-1].value) < 18:
                                        try:
                                            int(event.unicode)
                                            self.list_res[-1].value += event.unicode
                                        except ValueError:
                                            pass
                        if self.pow:
                            rectangle = pygame.draw.rect(self.screen, (243, 243, 243), (240, 255, 250, 25))
                            rectangle = pygame.draw.rect(self.screen, (243, 243, 243), (240, 320, 250, 25))

                            text = self.font.render(self.list_pow[-1].name, True, (50, 50, 50))
                            text2 = self.font.render(self.list_pow[-1].value, True, (50, 50, 50))

                            self.screen.blit(text, (245, 255))
                            self.screen.blit(text2, (245, 320))
                        else:
                            rectangle = pygame.draw.rect(self.screen, (243, 243, 243), (240, 255, 250, 25))
                            rectangle = pygame.draw.rect(self.screen, (243, 243, 243), (240, 320, 250, 25))

                            text = self.font.render(self.list_res[-1].name, True, (50, 50, 50))
                            text2 = self.font.render(self.list_res[-1].value, True, (50, 50, 50))

                            self.screen.blit(text, (245, 255))
                            self.screen.blit(text2, (245, 320))

                    if finish_rect.collidepoint((mx, my)) and click:
                        self.writing = False
                    pygame.display.flip()
                # Closes Simulator
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):  # leave application
                    on = False
                    pygame.quit()
                    sys.exit()

            # Buttons
            power_button = pygame.Rect(825, 200, 100, 110)
            res_button = pygame.Rect(845, 330, 61, 26)

            if res_button.collidepoint((mx, my)):  # Crea Resistencias
                self.paintButtons(False, True)
                if click:
                    self.createElement(61, 26, False)
                    click = False

            elif power_button.collidepoint((mx, my)):  # Crea Fuente de Poder
                self.paintButtons(True, False)
                if click:
                    self.createElement(100, 110, True)
                    click = False
            else:
                self.paintButtons(False, False)

            for o in self.list_pow:  # Checks for collitions
                if o.rect.collidepoint((mx, my)) and click:
                    o.setxy(mx - 50, my - 50)

            for o in self.list_res:  # Checks for collitions
                if o.rect.collidepoint((mx, my)) and click:
                    o.setxyRes(mx - 30, my - 10)

            if not self.writing:  # refresh screen
                self.drawElements(mx, my, click)


run = Start()

'''
stuff i don't need rn
rectangle = pygame.draw.rect(self.screen, (255, 0, 0), (845, 330, 61, 26))
p!catch
'''
