import pygame
from pygame.locals import *
import sys


class SimulateMode:
    def __init__(self, screen, clock, list_pow, list_res, list_lines_tuples, graph, list_lines_connections, list_nodes):
        self.screen = screen
        self.screen.fill([205, 200, 200])
        self.font = pygame.font.SysFont('timesnewroman', 20)
        self.valuesFont = pygame.font.SysFont('timesnewroman', 14)
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
        self.list_resistance_names_shell = []
        self.list_resistance_names_quick = []
        self.list_text_names_shell = []
        self.list_text_names_quick = []

        self.flagShowResistancesList = False

        self.initialCall()

    def drawElements(self, mx, my, click):  # Refresh elements in screen
        # Images
        power_img = pygame.image.load("Imgs\\power.png").convert_alpha()
        white_img = pygame.image.load("Imgs\\white.png").convert_alpha()
        res_img = pygame.image.load("Imgs\\resistencia.png").convert_alpha()

        text_del = self.font.render("Shell Sort:", True, (225, 225, 225))

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

        if self.flagShowResistancesList:
            pygame.draw.rect(self.screen, (255, 230, 176), (50, 50, 500, 500))
            y = 100
            for text in self.list_text_names_quick:
                self.screen.blit(text, [100, y])
                y += 25
            y = 100
            for text in self.list_text_names_shell:
                self.screen.blit(text, [200, y])
                y += 25




        pygame.display.flip()

    def initialCall(self):

        # Images
        on = True
        click = False
        firstClick = False

        # Resistance Button
        resistances_button = pygame.Rect((815, 75, 140, 34))
        text_del = self.font.render("Resistances", True, (225, 225, 225))

        while on:
            mx, my = pygame.mouse.get_pos()
            self.drawElements(mx, my, click)

            pygame.draw.rect(self.screen, (81, 125, 164), (815, 75, 140, 34))
            self.screen.blit(text_del, [838, 80])

            if resistances_button.collidepoint((mx, my)) and click:
                self.flagShowResistancesList = True
                for res in self.list_res:
                    self.list_resistance_names_shell.append(res.name)
                self.list_resistance_names_quick = self.list_resistance_names_shell.copy()
                self.shellsort(self.list_resistance_names_shell)
                self.QuickSort(self.list_resistance_names_quick)
                for name in self.list_resistance_names_quick:
                    name_text = self.font.render(name, True, (0, 0, 0))
                    self.list_text_names_quick.append(name_text)
                for name in self.list_resistance_names_shell:
                    name_text = self.font.render(name, True, (0, 0, 0))
                    self.list_text_names_shell.append(name_text)


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
                    rotatedRect = pygame.Rect(res.rect.x, res.rect.y, res.rect.height, res.rect.width)
                    if rotatedRect.collidepoint((mx, my)):
                        self.showValues(res, "Resistance")
                else:
                    if res.rect.collidepoint((mx, my)):
                        self.showValues(res, "Resistance")
            for pow in self.list_pow:
                if pow.rotated:
                    rotatedRect = pygame.Rect(pow.rect.x, pow.rect.y, pow.rect.height, pow.rect.width)
                    if rotatedRect.collidepoint((mx, my)):
                        self.showValues(pow, "Power")
                else:
                    if pow.rect.collidepoint((mx, my)):
                        self.showValues(pow, "Power")
            pygame.display.flip()

    def showValues(self, element, type):
        GREY = (200, 200, 200)
        if element.rotated:
            elementRect = pygame.Rect(element.rect.x, element.rect.y, element.rect.height, element.rect.width)
        else:
            elementRect = element.rect
        # pygame.draw.rect(self.screen, (255, 0, 0), elementRect)

        if type == "Power":
            infoRect = pygame.Rect(elementRect.x - 30, elementRect.y - 15, 110, 50)
            pygame.draw.rect(self.screen, GREY, infoRect)
            voltageText = self.valuesFont.render("Voltage: " + str(element.value) + "V", True, (0, 0, 0))
            currentText = self.valuesFont.render("Current: " + str(element.current) + "mA", True, (0, 0, 0))
            self.screen.blit(voltageText, (infoRect.x+5, infoRect.y+7))
            self.screen.blit(currentText, (infoRect.x+5, infoRect.y+30))

        elif type == "Resistance":
            infoRect = pygame.Rect(elementRect.x - 45, elementRect.y - 50, 110, 50)
            pygame.draw.rect(self.screen, GREY, infoRect)
            voltageText = self.valuesFont.render("Voltage: " + str(element.voltage) + "V", True, (0, 0, 0))
            currentText = self.valuesFont.render("Current: " + str(element.current) + "mA", True, (0, 0, 0))
            self.screen.blit(voltageText, (infoRect.x + 5, infoRect.y + 7))
            self.screen.blit(currentText, (infoRect.x + 5, infoRect.y + 30))
        else:
            print("Llamada errónea a showValues en SimulateMode, siendo llamado con un type incorrecto")
        pass

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

    # Ordenamiento de Datos

    # Shell Sort de mayor a menor

    def shellsort(self, list):
        n = len(list)
        partition = n // 2
        while partition > 0:
            for i in range(partition, n):
                temporal = list[i]
                j = i
                while j >= partition and list[j - partition] < temporal:
                    list[j] = list[j - partition]
                    j -= partition
                list[j] = temporal
            partition //= 2

    # QuickSort de menor a mayor

    def QuickSort(self, Lista):
        self.QuickSortaux(Lista, 0, len(Lista) - 1)

    def QuickSortaux(self, Lista, Low, High):
        if Low < High:
            index = self.Partition(Lista, Low, High)

            self.QuickSortaux(Lista, Low, index - 1)
            self.QuickSortaux(Lista, index, High)

    def Partition(self, Lista, Low, High):
        index = Low - 1
        pivot = Lista[High]
        for i in range(Low, High):
            if Lista[i] < pivot:
                index = index + 1
                Lista[index], Lista[i] = Lista[i], Lista[index]
        Lista[index + 1], Lista[High] = Lista[High], Lista[index + 1]
        return i + 1
