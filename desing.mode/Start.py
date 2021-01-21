import pygame
import sys
from pygame.locals import *
from PowerNode import PowerNode
from ResNode import ResNode

pygame.init()


class Start:
    def __init__(self):
        # Screen
        self.screen = pygame.display.set_mode((1000, 600))
        self.screen.fill([243, 243, 243])
        self.font = pygame.font.SysFont('timesnewroman', 20)
        self.clock = pygame.time.Clock()

        # List of Elements
        self.list_pow = []
        self.list_res = []
        self.name = ""
        self.value = ""

        # Flags
        self.writing = False
        self.pow = False
        self.name_int = False
        self.value_entry = False

        pygame.display.set_caption('Simulador')
        self.designMenu()

    def paintButtons(self, touched1, touched2):  # Changes colors of buttons
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

    def createElement(self, width, height, power):  # Creates new element
        if power:  # Crea fuente de Poder
            element = PowerNode(350, 250, width, height)
            self.list_pow.append(element)
            self.changeValues(True)
        else:  # Crea fuente de Resistencia
            element = ResNode(350, 250, width, height)
            self.list_res.append(element)
            self.changeValues(False)

    def changeValues(self, element):  # GUI thingy to change Name and Value
        # Images
        blue_ohms = pygame.image.load("Imgs\\blueRect_Ohm.png").convert_alpha()
        blue = pygame.image.load("Imgs\\blueRect.png").convert_alpha()
        power_img = pygame.image.load("Imgs\\power.png").convert_alpha()
        res_img = pygame.image.load("Imgs\\resistencia.png").convert_alpha()
        white_img = pygame.image.load("Imgs\\white.png").convert_alpha()

        text_surf = self.font.render('Enter Name:', True, (243, 243, 243))
        text_surf2 = self.font.render('Enter Value:', True, (243, 243, 243))
        done = self.font.render('Done', True, (243, 243, 243))
        choose = self.font.render('Choose', True, (243, 243, 243))

        self.writing = True  # Activa modo para escribir
        self.screen.blit(white_img, (100, 194))
        if element:
            self.pow = True
            self.screen.blit(blue_ohms, (100, 194))
            self.screen.blit(power_img, (450, 224))
            self.screen.blit(pygame.transform.rotate(power_img, 90), (570, 232))
        else:
            self.screen.blit(blue, (100, 194))
            self.screen.blit(res_img, (470, 260))
            self.screen.blit(pygame.transform.rotate(res_img, 90), (615, 240))
            self.pow = False

        self.screen.blit(text_surf, (123, 224))
        rectangle = pygame.draw.rect(self.screen, (243, 243, 243), (123, 255, 250, 25))
        self.screen.blit(text_surf2, (123, 290))
        rectangle = pygame.draw.rect(self.screen, (243, 243, 243), (123, 320, 250, 25))
        rectangle = pygame.draw.rect(self.screen, (81, 125, 164), (213, 365, 100, 25))
        self.screen.blit(done, (245, 365))
        rectangle = pygame.draw.rect(self.screen, (81, 125, 164), (470, 355, 70, 25))
        self.screen.blit(choose, (475, 355))
        rectangle = pygame.draw.rect(self.screen, (81, 125, 164), (590, 355, 70, 25))
        self.screen.blit(choose, (595, 355))

        pygame.display.flip()

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
                self.screen.blit(pygame.transform.rotate(power_img, 90),(o.rect.x, o.rect.y))
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

    def designMenu(self):  # Design Menu
        # Flags
        on = True
        click = False

        # self.uselessRect()

        while on:
            # Mouse
            mx, my = pygame.mouse.get_pos()

            # Boxes & Button | Change Name and Value
            name_Rect = pygame.Rect((123, 255, 250, 25))
            value_Rect = pygame.Rect((123, 320, 250, 25))
            finish_rect = pygame.Rect((213, 365, 100, 25))
            blue_rect_l = pygame.Rect((470, 355, 70, 25))
            blue_rect_r = pygame.Rect((590, 355, 70, 25))

            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN and event.button == 1:  # check for left mouse click
                    click = True
                if event.type == MOUSEBUTTONUP:
                    click = False

                # Code to write and save info in Node
                if self.writing:
                    if name_Rect.collidepoint((mx, my)) and click:
                        self.name_int = True
                        self.value_entry = False

                    if value_Rect.collidepoint((mx, my)) and click:
                        self.name_int = False
                        self.value_entry = True

                    if event.type == KEYDOWN:
                        if self.name_int:  # Changes Name
                            if event.key == pygame.K_BACKSPACE:
                                self.name = self.name[:-1]
                            else:
                                if len(self.name) < 18:
                                    self.name += event.unicode

                        if self.value_entry:  # Change Value
                            if event.key == pygame.K_BACKSPACE:
                                self.name = self.value[:-1]
                            else:
                                if len(self.value) < 18:
                                    try:
                                        int(event.unicode)
                                        self.value += event.unicode
                                    except ValueError:
                                        pass

                    # Refresh GUI
                    rectangle = pygame.draw.rect(self.screen, (243, 243, 243), (123, 255, 250, 25))
                    rectangle = pygame.draw.rect(self.screen, (243, 243, 243), (123, 320, 250, 25))

                    text = self.font.render(self.name, True, (50, 50, 50))
                    text2 = self.font.render(self.value, True, (50, 50, 50))
                    self.screen.blit(text, (245, 255))
                    self.screen.blit(text2, (245, 320))

                    if finish_rect.collidepoint((mx, my)) and click:  # Guarda Name & Value
                        if self.pow:
                            self.list_pow[-1].name = self.name
                            self.list_pow[-1].value = self.value
                        else:
                            self.list_res[-1].name = self.name
                            self.list_res[-1].value = self.value
                        self.name = ""
                        self.value = ""
                        self.writing = False

                    pygame.display.flip()

                if blue_rect_l.collidepoint((mx, my)) and click:
                    if self.pow:
                        self.list_pow[-1].rotated = False
                    else:
                        self.list_res[-1].rotated = False

                if blue_rect_r.collidepoint((mx, my)) and click:
                    if self.pow:
                        self.list_pow[-1].rotated = True
                    else:
                        self.list_res[-1].rotated = True

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


