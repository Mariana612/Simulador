import pygame
from pygame.locals import *
import sys


class SimulateMode:
    def __init__(self, screen, clock, list_pow, list_res, list_lines_tuples, graph, list_lines_connections, list_nodes):
        self.screen = screen
        self.screen.fill([205, 200, 200])
        self.font = pygame.font.SysFont('timesnewroman', 20)
        self.clock = clock
        self.graph = graph

        self.list_pow = list_pow
        self.list_res = list_res
        self.list_lines_tuples = list_lines_tuples
        self.list_lines_connections = list_lines_connections
        self.list_nodes = list_nodes
        self.dijkstraAnchorPoints = []
        self.dijkstraAnchorSquares = []
        self.pointA = None
        self.pointB = None
        self.list_traveled_lines = []
        self.list_least_voltage_lines = []
        self.list_most_voltage_lines = []
        self.setDijkstraAnchorPoints()

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

        for o in self.list_lines_tuples:
            pygame.draw.aaline(self.screen, (0, 0, 0), o[0], o[1])

        for o in self.dijkstraAnchorSquares:
            if o.collidepoint((mx, my)):
                pygame.draw.circle(self.screen, (0, 187, 255), o.center, 5)

        for o in self.list_least_voltage_lines:
            pygame.draw.aaline(self.screen, (0, 187, 255), o[0], o[1])

    def initialCall(self):

        # Images
        on = True
        click = False
        firstClick = False

        while on:
            mx, my = pygame.mouse.get_pos()
            self.drawElements(mx, my, click)

            delete_button = pygame.Rect((825, 130, 100, 34))

            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN and event.button == 1:  # check for left mouse click
                    click = True
                elif event.type == MOUSEBUTTONUP:
                    click = False
                    firstClick = False
                elif event.type == QUIT:  # leave application
                    on = False
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    on = False

            for i in self.dijkstraAnchorSquares:
                if i.collidepoint((mx, my)) and click and not firstClick:
                    firstClick = True
                    if self.pointA is None:
                        self.pointA = i.center
                    elif self.pointB is None:
                        self.pointB = i.center
                        self.drawDijkstraLines(self.pointA, self.pointB)
                    else:
                        break
            for res in self.list_res:
                if res.rotated:
                    rotatedRect = pygame.Rect(res.rect.x,res.rect.y,res.rect.height,res.rect.width)
                    pygame.draw.rect(self.screen,(255,0,0),rotatedRect)
                else:
                    pygame.draw.rect(self.screen,(255,0,0),res.rect)
            for pow in self.list_pow:
                if pow.rotated:
                    rotatedRect = pygame.Rect(pow.rect.x, pow.rect.y, pow.rect.height, pow.rect.width)
                    pygame.draw.rect(self.screen, (255, 0, 0), rotatedRect)
                else:
                pygame.draw.rect(self.screen, (255, 0, 0), pow.rect)
            pygame.display.flip()

    def setDijkstraAnchorPoints(self):
        for line in self.list_lines_tuples:
            self.dijkstraAnchorPoints.append(line[0])
            self.dijkstraAnchorPoints.append(line[1])
        self.dijkstraAnchorPoints = list(set(self.dijkstraAnchorPoints))
        for point in self.dijkstraAnchorPoints:
            self.dijkstraAnchorSquares.append(pygame.Rect((point[0] - 5, point[1] - 5, 10, 10)))

    def drawDijkstraLines(self, firstPoint, lastPoint):
        print("hello")
        for resistance in self.list_res:
            if resistance.anchorPoints[0].center == firstPoint:
                return True

            elif resistance.anchorPoints[1].center == firstPoint:
                return True
        for line in self.list_lines_tuples:
            if line in self.list_traveled_lines:
                continue
            if line[0] == firstPoint:
                self.list_traveled_lines.append(line)
                self.list_least_voltage_lines.append(line)
                if not self.drawDijkstraLines(line[1], lastPoint):
                    self.list_least_voltage_lines.remove(line)
                else:
                    return True



            elif line[1] == firstPoint:
                self.list_traveled_lines.append(line)
                self.list_least_voltage_lines.append(line)
                if not self.drawDijkstraLines(line[0], lastPoint):
                    self.list_least_voltage_lines.remove(line)
                else:
                    return True
        return False
