import pygame
import sys
from pygame.locals import *
from PowerNode import PowerNode
from ResNode import ResNode
from SimulateMode import SimulateMode
from Graph import Graph


class DesignMode:
    def __init__(self, screen, clock):
        # Screen
        self.screen = screen
        self.screen.fill([243, 243, 243])
        self.font = pygame.font.SysFont('timesnewroman', 20)
        self.clock = clock

        # List of Elements
        self.list_pow = []
        self.list_res = []
        self.list_lines_tuples = []
        self.list_lines_connections = []
        self.list_nodes = []
        self.name = ""
        self.value = ""
        self.currentlyHeldElement = None
        self.lineFirstPoint = (0, 0)
        self.nodeFirstPoint = (0, 0)
        self.graph = Graph()
        self.lastLookedAtNode = None

        # Flags
        self.writing = False
        self.pow = False
        self.name_int = False
        self.value_entry = False
        self.holdingElement = False
        self.mouseOnAnchor = False
        self.drawingLine = False
        self.firstClickDrawingLine = False
        self.lastClickDrawingLine = False
        self.validCircuit = False

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
        rectangle = pygame.draw.rect(self.screen, (81, 125, 164), (825, 420, 100, 34))
        text = self.font.render("simulate", True, (225, 225, 225))
        self.screen.blit(text, [840, 425])
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
        self.screen.blit(white_img, (0, 0))
        if element:
            self.pow = True
            self.screen.blit(blue, (100, 194))
            self.screen.blit(power_img, (450, 224))
            self.screen.blit(pygame.transform.rotate(power_img, 90), (570, 232))
        else:
            self.screen.blit(blue_ohms, (100, 194))
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
                o.setAnchorPoints()
            if o.rotated:
                o.setAnchorPoints()
                self.screen.blit(pygame.transform.rotate(power_img, 90), (o.rect.x, o.rect.y))
                nmx, nmy = pygame.mouse.get_pos()
                if o.anchorPoints[0].collidepoint((nmx, nmy)) and not self.holdingElement:
                    pygame.draw.circle(self.screen, (200, 0, 0), o.anchorPoints[0].center, 5)
                elif o.anchorPoints[1].collidepoint((nmx, nmy)) and not self.holdingElement:
                    pygame.draw.circle(self.screen, (200, 0, 0), o.anchorPoints[1].center, 5)

            else:
                o.setAnchorPoints()
                self.screen.blit(power_img, (o.rect.x, o.rect.y))
                nmx, nmy = pygame.mouse.get_pos()
                if o.anchorPoints[0].collidepoint((nmx, nmy)) and not self.holdingElement:
                    pygame.draw.circle(self.screen, (200, 0, 0), o.anchorPoints[0].center, 5)
                elif o.anchorPoints[1].collidepoint((nmx, nmy)) and not self.holdingElement:
                    pygame.draw.circle(self.screen, (200, 0, 0), o.anchorPoints[1].center, 5)


        for o in self.list_res:  # Refresca todos las resistencias
            if (not o.rect.collidepoint((mx, my)) and not click) or (o.rect.collidepoint((mx, my)) and not click):
                o.checkPlacementRes()
                o.setAnchorPoints()
            if o.rotated:
                o.setAnchorPoints()
                self.screen.blit(pygame.transform.rotate(res_img, 90), (o.rect.x, o.rect.y))
                nmx, nmy = pygame.mouse.get_pos()

                if o.anchorPoints[0].collidepoint((nmx, nmy)) and not self.holdingElement:
                    pygame.draw.circle(self.screen, (200, 0, 0), o.anchorPoints[0].center, 5)
                elif o.anchorPoints[1].collidepoint((nmx, nmy)) and not self.holdingElement:
                    pygame.draw.circle(self.screen, (200, 0, 0), o.anchorPoints[1].center, 5)
            else:
                o.setAnchorPoints()
                self.screen.blit(res_img, (o.rect.x, o.rect.y))
                nmx, nmy = pygame.mouse.get_pos()
                if o.anchorPoints[0].collidepoint((nmx, nmy)) and not self.holdingElement:
                    pygame.draw.circle(self.screen, (200, 0, 0), o.anchorPoints[0].center, 5)
                elif o.anchorPoints[1].collidepoint((nmx, nmy)) and not self.holdingElement:
                    pygame.draw.circle(self.screen, (200, 0, 0), o.anchorPoints[1].center, 5)

        if self.drawingLine:
            if click and not self.firstClickDrawingLine:
                num_y = 96
                num_x = 96
                print(num_x, num_y)
                nmx, nmy = pygame.mouse.get_pos()
                while not (num_y - (nmy - 48) >= 0):
                    num_y += 96
                    print(num_x, num_y)
                while not (num_x - (nmx - 48) >= 0):
                    num_x += 96
                    print(num_x, num_y)
                self.list_lines_tuples.append((self.lineFirstPoint, (num_x, num_y)))
                self.lineFirstPoint = (num_x, num_y)

            pygame.draw.aaline(self.screen, (0, 0, 0), self.lineFirstPoint, (nmx, nmy))


        for o in self.list_lines_tuples:
            pygame.draw.aaline(self.screen, (0, 0, 0), o[0], o[1])






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
            change_button = pygame.Rect((825, 420, 100, 34))

            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN and event.button == 1:  # check for left mouse click
                    click = True
                    self.firstClickDrawingLine = False
                    self.lastClickDrawingLine = False
                if event.type == MOUSEBUTTONUP:
                    click = False
                    self.holdingElement = False

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

                    pygame.display.flip()


                # Closes Simulator
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):  # leave application
                    on = False
                    pygame.quit()
                    sys.exit()

            # Buttons
            power_button = pygame.Rect(825, 200, 100, 110)
            res_button = pygame.Rect(845, 330, 61, 26)

            if not self.writing:
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
                    if o.anchorPoints[0].collidepoint((mx, my)) and click and not self.holdingElement and self.drawingLine and not self.firstClickDrawingLine:
                        self.drawingLine = False
                        self.lastClickDrawingLine = True
                        self.list_lines_tuples.append((self.lineFirstPoint, o.anchorPoints[0].center))
                        self.list_lines_connections.append((self.nodeFirstPoint, o.anchorPoints[0].center))
                        self.lineFirstPoint = None
                        self.nodeFirstPoint = None
                    elif o.anchorPoints[1].collidepoint((mx, my)) and click and not self.holdingElement and self.drawingLine and not self.firstClickDrawingLine:
                        self.drawingLine = False
                        self.lastClickDrawingLine = True
                        self.list_lines_tuples.append((self.lineFirstPoint, o.anchorPoints[1].center))
                        self.list_lines_connections.append((self.nodeFirstPoint, o.anchorPoints[1].center))
                        self.lineFirstPoint = None
                        self.nodeFirstPoint = None
                    elif o.anchorPoints[0].collidepoint((mx, my)) and click and not self.holdingElement and not self.drawingLine and not self.lastClickDrawingLine:
                        self.drawingLine = True
                        self.firstClickDrawingLine = True
                        self.lineFirstPoint = o.anchorPoints[0].center
                        self.nodeFirstPoint = o.anchorPoints[0].center
                    elif o.anchorPoints[1].collidepoint((mx, my)) and click and not self.holdingElement and not self.drawingLine and not self.lastClickDrawingLine:
                        self.drawingLine = True
                        self.firstClickDrawingLine = True
                        self.lineFirstPoint = o.anchorPoints[1].center
                        self.nodeFirstPoint = o.anchorPoints[1].center
                    elif o.rect.collidepoint((mx, my)) and click and not self.holdingElement and not self.drawingLine:
                        self.holdingElement = True
                        o.setxy(mx - 50, my - 50)
                        self.currentlyHeldElement = o


                for o in self.list_res:  # Checks for collitions
                    if o.anchorPoints[0].collidepoint((mx, my)) and click and not self.holdingElement and self.drawingLine and not self.firstClickDrawingLine:
                        self.drawingLine = False
                        self.lastClickDrawingLine = True
                        self.list_lines_tuples.append((self.lineFirstPoint, o.anchorPoints[0].center))
                        self.list_lines_connections.append((self.nodeFirstPoint, o.anchorPoints[1].center))
                        self.lineFirstPoint = None
                        self.nodeFirstPoint = None
                    elif o.anchorPoints[1].collidepoint((mx, my)) and click and not self.holdingElement and self.drawingLine and not self.firstClickDrawingLine:
                        self.drawingLine = False
                        self.lastClickDrawingLine = True
                        self.list_lines_tuples.append((self.lineFirstPoint, o.anchorPoints[1].center))
                        self.list_lines_connections.append((self.nodeFirstPoint, o.anchorPoints[1].center))
                        self.lineFirstPoint = None
                        self.nodeFirstPoint = None
                    elif o.anchorPoints[0].collidepoint((mx, my)) and click and not self.holdingElement and not self.drawingLine and not self.lastClickDrawingLine:
                        self.drawingLine = True
                        self.firstClickDrawingLine = True
                        self.lineFirstPoint = o.anchorPoints[0].center
                        self.nodeFirstPoint = o.anchorPoints[0].center
                    elif o.anchorPoints[1].collidepoint((mx, my)) and click and not self.holdingElement and not self.drawingLine and not self.lastClickDrawingLine:
                        self.drawingLine = True
                        self.firstClickDrawingLine = True
                        self.lineFirstPoint = o.anchorPoints[1].center
                        self.nodeFirstPoint = o.anchorPoints[1].center
                    elif o.rect.collidepoint((mx, my)) and click and not self.holdingElement and not self.drawingLine:
                        if not o.rotated:
                            self.holdingElement = True
                            o.setxyRes(mx - 30, my - 10)
                            self.currentlyHeldElement = o
                        else:
                            self.holdingElement = True
                            o.setxyRes(mx - 13, my - 36)
                            self.currentlyHeldElement = o

                # Move currently held element
                if self.holdingElement:
                    if isinstance(self.currentlyHeldElement, PowerNode):
                        self.currentlyHeldElement.setxy(mx - 50, my - 50)
                    else:
                        if not self.currentlyHeldElement.rotated:
                            self.currentlyHeldElement.setxyRes(mx - 30, my - 10)
                        else:
                            self.currentlyHeldElement.setxyRes(mx - 13, my - 36)



                if change_button.collidepoint((mx, my)) and click:  # changes mode
                    self.checkCircuitValidity()
                    click = False
                    SimulateMode(self.screen, self.clock, self.list_pow, self.list_res, self.list_lines_tuples)
                    on = False

            else:
                self.paintButtons(False, False)

            if not self.writing:  # refresh screen
                self.drawElements(mx, my, click)

    def checkCircuitValidity(self):
        if len(self.list_pow) > 1:
            return False
        voltageSource = self.list_pow[0]
        firstAnchorPoint = voltageSource.anchorPoints[0]
        lastAnchorPoint = voltageSource.anchorPoints[1]
        self.resolveNodes(firstAnchorPoint, lastAnchorPoint)



    def resolveNodes(self, firstAnchorPoint, lastAnchorPoint):
        for line in self.list_lines_connections:
            if line[0] == firstAnchorPoint:
                if line[1] == lastAnchorPoint:
                    if self.checkNodeExistence(line[0]):
                        if self.checkNodeExistence(line[1]):
                            continue
                        else:
                            self.lastLookedAtNode.Points.append(line[1])
                            self.validCircuit = True
                            self.resolveNodes(line[1], lastAnchorPoint)
                            continue
                    elif self.checkNodeExistence(line[1]):
                        self.lastLookedAtNode.Points.append(line[0])
                        continue
                    else:
                        node = self.graph.addnode("node"+str(len(self.list_nodes)), 0)
                        node.Points.append(line[0])
                        node.Points.append(line[1])
                        self.list_nodes.append(node)
                        self.validCircuit = True
                        self.resolveNodes(line[1], lastAnchorPoint)
                        continue
                for res in self.list_res:
                    if res.anchorPoints[0] == line[1]:
                        if self.checkNodeExistence(line[0]):
                            if self.checkNodeExistence(line[1]):
                                break
                            else:
                                self.lastLookedAtNode.Points.append(line[1])
                                self.resolveNodes(res.anchorPoints[1], lastAnchorPoint)
                                self.resolveNodes(line[1], lastAnchorPoint)
                                break
                        elif self.checkNodeExistence(line[1]):
                            self.lastLookedAtNode.Points.append(line[0])
                            break
                        else:
                            node = self.graph.addnode("node" + str(len(self.list_nodes)), 0)
                            node.Points.append(line[0])
                            node.Points.append(line[1])
                            self.list_nodes.append(node)
                            self.resolveNodes(res.anchorPoints[1], lastAnchorPoint)
                            self.resolveNodes(line[1], lastAnchorPoint)
                            break
                    elif res.anchorPoints[1] == line[1]:
                        if self.checkNodeExistence(line[0]):
                            if self.checkNodeExistence(line[1]):
                                break
                            else:
                                self.lastLookedAtNode.Points.append(line[1])
                                self.resolveNodes(res.anchorPoints[1], lastAnchorPoint)
                                self.resolveNodes(line[1], lastAnchorPoint)
                                break
                        elif self.checkNodeExistence(line[1]):
                            self.lastLookedAtNode.Points.append(line[0])
                            break
                        else:
                            node = self.graph.addnode("node" + str(len(self.list_nodes)), 0)
                            node.Points.append(line[0])
                            node.Points.append(line[1])
                            self.list_nodes.append(node)
                            self.resolveNodes(res.anchorPoints[0], lastAnchorPoint)
                            self.resolveNodes(line[1], lastAnchorPoint)
                            break
            elif line[1] == firstAnchorPoint:
                if line[0] == lastAnchorPoint:
                    if self.checkNodeExistence(line[1]):
                        if self.checkNodeExistence(line[0]):
                            continue
                        else:
                            self.lastLookedAtNode.Points.append(line[0])
                            self.validCircuit = True
                            self.resolveNodes(line[0], lastAnchorPoint)
                            continue
                    elif self.checkNodeExistence(line[0]):
                        self.lastLookedAtNode.Points.append(line[1])
                        continue
                    else:
                        node = self.graph.addnode("node" + str(len(self.list_nodes)), 0)
                        node.Points.append(line[1])
                        node.Points.append(line[0])
                        self.list_nodes.append(node)
                        self.validCircuit = True
                        self.resolveNodes(line[0], lastAnchorPoint)
                        continue
                for res in self.list_res:
                    if res.anchorPoints[0] == line[0]:
                        if self.checkNodeExistence(line[1]):
                            if self.checkNodeExistence(line[0]):
                                break
                            else:
                                self.lastLookedAtNode.Points.append(line[0])
                                self.resolveNodes(res.anchorPoints[1], lastAnchorPoint)
                                self.resolveNodes(line[0], lastAnchorPoint)
                                break
                        elif self.checkNodeExistence(line[0]):
                            self.lastLookedAtNode.Points.append(line[1])
                            break
                        else:
                            node = self.graph.addnode("node" + str(len(self.list_nodes)), 0)
                            node.Points.append(line[1])
                            node.Points.append(line[0])
                            self.list_nodes.append(node)
                            self.resolveNodes(res.anchorPoints[1], lastAnchorPoint)
                            self.resolveNodes(line[0], lastAnchorPoint)
                            break
                    elif res.anchorPoints[1] == line[0]:
                        if self.checkNodeExistence(line[1]):
                            if self.checkNodeExistence(line[0]):
                                break
                            else:
                                self.lastLookedAtNode.Points.append(line[0])
                                self.resolveNodes(res.anchorPoints[1], lastAnchorPoint)
                                self.resolveNodes(line[0], lastAnchorPoint)
                                break
                        elif self.checkNodeExistence(line[0]):
                            self.lastLookedAtNode.Points.append(line[1])
                            break
                        else:
                            node = self.graph.addnode("node" + str(len(self.list_nodes)), 0)
                            node.Points.append(line[1])
                            node.Points.append(line[0])
                            self.list_nodes.append(node)
                            self.resolveNodes(res.anchorPoints[0], lastAnchorPoint)
                            self.resolveNodes(line[0], lastAnchorPoint)
                            break

    def checkNodeExistence(self, point):
        for node in self.list_nodes:
            for nodePoint in node.Points:
                if point == nodePoint:
                    return True
        self.lastLookedAtNode = node
        return False

