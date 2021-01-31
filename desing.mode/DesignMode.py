import pygame
import sys
from pygame.locals import *
from PowerNode import PowerNode
from ResNode import ResNode
from SimulateMode import SimulateMode
from Estructuras import Graph
from random import *


class DesignMode:
    """
    Clase que modela el modo diseño
    Autor:
    """
    def __init__(self, screen, clock, circuitList = None):
        """
Inicializador de la clase
Autor:
Entrada:Main window, main clock
        """
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
        self.graph = None
        self.lastLookedAtNode = None
        self.nodeNameCounter = 0
        self.object = None

        if circuitList != None: #se importa un circuito
            for pow in circuitList[0]:
                self.list_pow.append(PowerNode(pow['x'],pow['y'],pow['width'],pow['height'],pow['name'],pow['value'],pow['rotated']))
            for res in circuitList[1]:
                self.list_res.append(ResNode(res['x'],res['y'],res['width'],res ['height'],res['name'],res['value'],res['rotated']))
            self.list_lines_tuples = self.tuple_list(circuitList[2])
            self.list_lines_connections = self.tuple_list(circuitList[3])

            print(self.list_lines_tuples)
            print(self.list_lines_connections)

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
        self.remove = False
        self.remove_thingy = False
        self.modify = False

        pygame.display.set_caption('Simulador')
        self.designMenu()

    def tuple_list(self, listvar):
        """
Función que convierte una lista de listas en una lista de tuplas recursivamente
Autor: Ignacio Vargas
Entrada:Lista de variables
Salida:Lista de tuplas
        """
        tupledList = []
        for element in listvar:
            if isinstance(element, list):
                newElement = self.tuple_list(element)
                tupledList.append(tuple(newElement))
            else:
                tupledList.append(element)
        return tupledList


    def paintButtons(self, touched1, touched2):  # Changes colors of buttons
        """
        Función para cambiar los colores de los botones
        Autor:
        Entrada:Lista de Nodos, booleano que indica si buscamos el mayor o menor peso
        Salida:Nodo de Mayor/Menor distancia
        """
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
        pygame.draw.rect(self.screen, (81, 125, 164), (825, 420, 100, 34))
        pygame.draw.rect(self.screen, (81, 125, 164), (825, 130, 100, 34))
        text_del = self.font.render("delete lines", True, (225, 225, 225))
        self.screen.blit(text_del, [830, 135])
        pygame.draw.rect(self.screen, (81, 125, 164), (825, 75, 100, 34))
        text_del = self.font.render("delete", True, (225, 225, 225))
        self.screen.blit(text_del, [848, 80])
        text = self.font.render("simulate", True, (225, 225, 225))
        self.screen.blit(text, [840, 425])
        pygame.draw.rect(self.screen, (81, 125, 164), (825, 475, 100, 34))
        text_exp = self.font.render("export", True, (225, 225, 225))
        self.screen.blit(text_exp, [850, 480])
        pygame.display.flip()
        self.clock.tick(14)

    def createElement(self, width, height, power):  # Creates new element
        """
Función para crear un elemento en el modo diseño
Autor:
Entrada: Ancho del elemento, altura del elemento y booleano de si se crea una resistencia o fuente
        """
        if power:  # Crea fuente de Poder
            element = PowerNode(350, 250, width, height)
            self.list_pow.append(element)
            self.changeValues(True)

        else:  # Crea fuente de Resistencia
            element = ResNode(350, 250, width, height)
            self.list_res.append(element)
            self.changeValues(False)

    def changeValues(self, element):  # GUI thingy to change Name and Value
        """
Función que permite cambiar al usuario el nombre y valor de un componente añadido (GUI part)
Autor:
Entrada:elemento a cambiar
        """
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

    def changeValues2(self, element, pow):  # GUI thingy to change Name and Value
        """
Función que permite cambiar al usuario el nombre y valor de un componente añadido (actual change)
Autor:
Entrada:elementp a cambiar, booleano para saber si es una fuente o resistencia
        """
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

        if pow:
            self.pow = True
            self.screen.blit(blue, (100, 194))
            self.screen.blit(power_img, (450, 224))
            self.screen.blit(pygame.transform.rotate(power_img, 90), (570, 232))

        else:
            self.screen.blit(blue_ohms, (100, 194))
            self.screen.blit(res_img, (470, 260))
            self.screen.blit(pygame.transform.rotate(res_img, 90), (615, 240))
            self.pow = False

        self.name = element.name
        self.value = element.value
        self.object = element
        self.modify = True
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
        """
Dibujador de todos los elementos
Autor:
Entrada: posición x del mouse, posición y del mouse, click
        """
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
                nmx, nmy = pygame.mouse.get_pos()
                while not (num_y - (nmy - 48) >= 0):
                    num_y += 96
                while not (num_x - (nmx - 48) >= 0):
                    num_x += 96
                self.list_lines_tuples.append((self.lineFirstPoint, (num_x, num_y)))
                self.lineFirstPoint = (num_x, num_y)

            pygame.draw.aaline(self.screen, (0, 0, 0), self.lineFirstPoint, (nmx, nmy))

        for o in self.list_lines_tuples:
            pygame.draw.aaline(self.screen, (0, 0, 0), o[0], o[1])

        pygame.display.flip()

    def exportCircuit(self,filename):
        """
Función para exportar un circuito a un archivo txt
Autor: Ignacio Vargas
Entrada: Nombre del archivo
        """
        import json, os
        powerList=[]
        resList=[]
        for pow in self.list_pow:
            powerList.append(pow.toDict())
        for res in self.list_res:
            resList.append(res.toDict())

        circuitList = [powerList, resList, self.list_lines_tuples, self.list_lines_connections]
        #circuitJSON = json.dumps(circuitList)

        path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'circuits')) #agarra el path de circuits
        os.makedirs(path, exist_ok=True) #crea el directorio de circuits si no existe
        with open(os.path.join(path,filename+'.txt'), 'w', encoding='utf-8') as f: #hay que hacer el path.join para que cree un archivo y no un directorio
            json.dump(circuitList, f, ensure_ascii=False, indent=4)


    def exportMenu(self):
        """
Función que contiene el menú para exportar archivos
Autor: Ignacio Vargas
        """
        from pathvalidate import sanitize_filepath
        running = True
        filenameString = ""
        LIGHTBLUE = (154,169,182)
        WHITE = (255,255,255)
        ORANGE = (253,160,40)
        cancel_button = pygame.Rect((280, 350, 100, 40))
        accept_button = pygame.Rect((450, 350, 100, 40))


        while running:
            click = False
            for event in pygame.event.get():  # check events here
                if event.type == QUIT:  # leave application
                    running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == pygame.K_BACKSPACE:
                        filenameString = filenameString[:-1]
                    elif self.font.size(filenameString + event.unicode)[0] < 190: #[0] accesa el width ya que returna (w,h)
                        filenameString += event.unicode
                        filenameString = sanitize_filepath(filenameString)
                elif event.type == MOUSEBUTTONDOWN and event.button == 1:  # check for left mouse click
                    click = True

            mx, my = pygame.mouse.get_pos()
            if accept_button.collidepoint((mx, my)) and click:
                if len(filenameString) > 0:
                    self.exportCircuit(filenameString)
                    running = False
            elif cancel_button.collidepoint((mx, my)) and click:
                running=False

            if running:  # tal vez ocupe agregar un blit al fondo
                pygame.draw.rect(self.screen, LIGHTBLUE,(250,194,330,213))
                pygame.draw.rect(self.screen, WHITE, (300, 290, 200, 30))
                text = self.font.render("Insert export filename:", True, WHITE)
                self.screen.blit(text, [323, 230])
                text = self.font.render(".txt", True, (0,0,0))
                self.screen.blit(text, [505, 295])
                text = self.font.render(filenameString, True, (0,0,0))
                self.screen.blit(text, [305, 295])
                #botones
                pygame.draw.rect(self.screen, ORANGE, cancel_button)
                pygame.draw.rect(self.screen, ORANGE, accept_button)
                text = self.font.render("Cancel", True, WHITE)
                self.screen.blit(text, [300, 359])
                text = self.font.render("Accept", True, WHITE)
                self.screen.blit(text, [472, 359])
                pygame.display.flip()
                self.clock.tick(60)

        return

    def designMenu(self):  # Design Menu
        """
Función que contiene el menu de diseño
Autor:
        """
        # Flags
        on = True
        click = False
        click_left = False

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
            delete_button = pygame.Rect((825, 130, 100, 34))
            delete_thingy_button = pygame.Rect((825, 75, 100, 34))
            export_button = pygame.Rect((825, 475, 100, 34))

            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN and event.button == 1:  # check for left mouse click
                    click = True
                    self.firstClickDrawingLine = False
                    self.lastClickDrawingLine = False

                if event.type == MOUSEBUTTONDOWN and event.button == 3:  # check for left mouse click
                    click_left = True

                if event.type == MOUSEBUTTONUP:
                    click = False
                    click_left = False
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
                                self.value = self.value[:-1]
                            else:
                                if len(self.value) < 18:
                                    try:
                                        int(event.unicode)
                                        self.value += event.unicode
                                    except ValueError:
                                        pass

                    # Refresh GUI
                    pygame.draw.rect(self.screen,(255,255,255),name_Rect)
                    pygame.draw.rect(self.screen, (255, 255, 255), value_Rect)
                    text = self.font.render(self.name, True, (50, 50, 50))
                    text2 = self.font.render(self.value, True, (50, 50, 50))
                    self.screen.blit(text, (124, 255))
                    self.screen.blit(text2, (124, 320))

                    if finish_rect.collidepoint((mx, my)) and click:  # Guarda Name & Value
                        if self.modify:
                            self.object.name = self.name
                            self.object.value = self.value
                        else:
                            if self.pow:
                                self.list_pow[-1].name = self.name
                                self.list_pow[-1].value = self.value
                            else:
                                self.list_res[-1].name = self.name
                                self.list_res[-1].value = self.value

                        self.name = ""
                        self.value = ""
                        self.modify = False
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
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif (event.type == KEYDOWN and event.key == K_ESCAPE):  # leave application
                    on = False

            # Buttons
            power_button = pygame.Rect(825, 200, 100, 110)
            res_button = pygame.Rect(845, 330, 61, 26)

            if not self.writing:
                if res_button.collidepoint((mx, my)):  # Crea Resistencias
                    self.paintButtons(False, True)
                    if click:
                        self.createElement(61, 26, False)
                        click = False

                elif power_button.collidepoint((mx, my)) and len(self.list_pow) == 0:  # Crea Fuente de Poder
                    self.paintButtons(True, False)
                    if click:
                        self.createElement(100, 110, True)
                        click = False
                else:
                    self.paintButtons(False, False)

                if delete_button.collidepoint((mx, my)) and click:
                    self.list_lines_tuples = []
                    self.list_lines_connections = []

                if delete_thingy_button.collidepoint((mx, my)) and click:
                    self.remove_thingy = True

                if export_button.collidepoint((mx,my)) and click:
                    self.exportMenu()
                    click = False

                if self.remove_thingy:
                    for elements in self.list_pow:
                        self.list_pow.remove(elements)
                    for elements in self.list_res:
                        self.list_res.remove(elements)
                    self.remove_thingy = False

                for o in self.list_pow:  # Checks for collitions
                    if not (o.rect.collidepoint((mx, my)) and click_left):
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
                    else:
                        self.changeValues2(o, True)

                for o in self.list_res:  # Checks for collitions
                    if not (o.rect.collidepoint((mx, my)) and  click_left):
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
                            if not o.rotated:
                                self.holdingElement = True
                                o.setxyRes(mx - 30, my - 10)
                                self.currentlyHeldElement = o
                            else:
                                self.holdingElement = True
                                o.setxyRes(mx - 13, my - 36)
                                self.currentlyHeldElement = o
                    else:
                        self.changeValues2(o, False)

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
                    if self.validCircuit:
                        click = False
                        SimulateMode(self.screen, self.clock, self.list_pow, self.list_res, self.list_lines_tuples, self.graph, self.list_lines_connections, self.list_nodes)


            else:
                self.paintButtons(False, False)

            if not self.writing:  # refresh screen
                self.drawElements(mx, my, click)

    def checkCircuitValidity(self):
        """
        Función que revisa si un circuito dibujado es válido.
        Si lo es, crea el nodo y sus conexiones.
        Autor: Jose Retana
        Salida: booleano de validación del circuito
        """
        self.graph = Graph.Graph()
        if len(self.list_pow) > 1:
            self.validCircuit = False
            return
        voltageSource = self.list_pow[0]
        firstAnchorPoint = voltageSource.anchorPoints[0].center
        lastAnchorPoint = voltageSource.anchorPoints[1].center
        self.resolveNodes(firstAnchorPoint, lastAnchorPoint)
        if self.validCircuit:
            self.makeNodeConnections()
        else:
            self.graph = Graph.Graph()
            self.list_nodes = []


    def resolveNodes(self, firstAnchorPoint, lastAnchorPoint):
        """
        Función recursiva que analiza el circuito dado y determina si es válido o no.
        Si es válido, crea los nodos correspondientes en el grafo, junto con los puntos claves
        necesarios para crear las conexiones.
        Autor: Jose Retana
        Entrada: firstAnchorPoint, lastAnchorPoint (Tuples)
        """
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
                        node = self.graph.addnode("node"+str(self.nodeNameCounter), 0)
                        self.nodeNameCounter += 1
                        node.Points.append(line[0])
                        node.Points.append(line[1])
                        self.list_nodes.append(node)
                        self.validCircuit = True
                        self.resolveNodes(line[1], lastAnchorPoint)
                        continue
                for res in self.list_res:
                    if res.anchorPoints[0].center == line[1]:
                        if self.checkNodeExistence(line[0]):
                            if self.checkNodeExistence(line[1]):
                                node0, node1 = self.checkTwoNodesExistance(line[0], line[1])
                                if node0 == node1:
                                    break
                                else:
                                    self.graph.fusenodes(node0.name, node1.name)
                                    self.list_nodes.remove(node1)
                                    break
                            else:
                                self.lastLookedAtNode.Points.append(line[1])
                                self.resolveNodes(res.anchorPoints[1].center, lastAnchorPoint)
                                self.resolveNodes(line[1], lastAnchorPoint)
                                break
                        elif self.checkNodeExistence(line[1]):
                            self.lastLookedAtNode.Points.append(line[0])
                            break
                        else:
                            node = self.graph.addnode("node" + str(self.nodeNameCounter), 0)
                            self.nodeNameCounter += 1
                            node.Points.append(line[0])
                            node.Points.append(line[1])
                            self.list_nodes.append(node)
                            self.resolveNodes(res.anchorPoints[1].center, lastAnchorPoint)
                            self.resolveNodes(line[1], lastAnchorPoint)
                            break
                    elif res.anchorPoints[1].center == line[1]:
                        if self.checkNodeExistence(line[0]):
                            if self.checkNodeExistence(line[1]):
                                node0, node1 = self.checkTwoNodesExistance(line[0], line[1])
                                if node0 == node1:
                                    break
                                else:
                                    self.graph.fusenodes(node0.name, node1.name)
                                    self.list_nodes.remove(node1)
                                    break
                            else:
                                self.lastLookedAtNode.Points.append(line[1])
                                self.resolveNodes(res.anchorPoints[0].center, lastAnchorPoint)
                                self.resolveNodes(line[1], lastAnchorPoint)
                                break
                        elif self.checkNodeExistence(line[1]):
                            self.lastLookedAtNode.Points.append(line[0])
                            break
                        else:
                            node = self.graph.addnode("node" + str(self.nodeNameCounter), 0)
                            self.nodeNameCounter += 1
                            node.Points.append(line[0])
                            node.Points.append(line[1])
                            self.list_nodes.append(node)
                            self.resolveNodes(res.anchorPoints[0].center, lastAnchorPoint)
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
                        node = self.graph.addnode("node" + str(self.nodeNameCounter), 0)
                        self.nodeNameCounter += 1
                        node.Points.append(line[1])
                        node.Points.append(line[0])
                        self.list_nodes.append(node)
                        self.validCircuit = True
                        self.resolveNodes(line[0], lastAnchorPoint)
                        continue
                for res in self.list_res:
                    if res.anchorPoints[0].center == line[0]:
                        if self.checkNodeExistence(line[1]):
                            if self.checkNodeExistence(line[0]):
                                node0, node1 = self.checkTwoNodesExistance(line[1], line[0])
                                if node0 == node1:
                                    break
                                else:
                                    self.graph.fusenodes(node0.name, node1.name)
                                    self.list_nodes.remove(node1)
                                    break
                            else:
                                self.lastLookedAtNode.Points.append(line[0])
                                self.resolveNodes(res.anchorPoints[1].center, lastAnchorPoint)
                                self.resolveNodes(line[0], lastAnchorPoint)
                                break
                        elif self.checkNodeExistence(line[0]):
                            self.lastLookedAtNode.Points.append(line[1])
                            break
                        else:
                            node = self.graph.addnode("node" + str(self.nodeNameCounter), 0)
                            self.nodeNameCounter += 1
                            node.Points.append(line[1])
                            node.Points.append(line[0])
                            self.list_nodes.append(node)
                            self.resolveNodes(res.anchorPoints[1].center, lastAnchorPoint)
                            self.resolveNodes(line[0], lastAnchorPoint)
                            break
                    elif res.anchorPoints[1].center == line[0]:
                        if self.checkNodeExistence(line[1]):
                            if self.checkNodeExistence(line[0]):
                                node0, node1 = self.checkTwoNodesExistance(line[1], line[0])
                                if node0 == node1:
                                    break
                                else:
                                    self.graph.fusenodes(node0.name, node1.name)
                                    self.list_nodes.remove(node1)
                                    break
                            else:
                                self.lastLookedAtNode.Points.append(line[0])
                                self.resolveNodes(res.anchorPoints[1].center, lastAnchorPoint)
                                self.resolveNodes(line[0], lastAnchorPoint)
                                break
                        elif self.checkNodeExistence(line[0]):
                            self.lastLookedAtNode.Points.append(line[1])
                            break
                        else:
                            node = self.graph.addnode("node" + str(self.nodeNameCounter), 0)
                            self.nodeNameCounter += 1
                            node.Points.append(line[1])
                            node.Points.append(line[0])
                            self.list_nodes.append(node)
                            self.resolveNodes(res.anchorPoints[0].center, lastAnchorPoint)
                            self.resolveNodes(line[0], lastAnchorPoint)
                            break

    def checkNodeExistence(self, point):
        """
        Función que revisa si un punto ya existe entre los nodos existentes
        Autor: Jose Retana
        Entrada: punto de un nodo
        Salida: Bool
        """
        for node in self.list_nodes:
            for nodePoint in node.Points:
                if point == nodePoint:
                    self.lastLookedAtNode = node
                    return True
        return False

    def checkTwoNodesExistance(self, point1, point2):
        """
        Retorna los nodos a los que pertenecen los dos puntos dados
        Autor: Jose Retana
        Entrada: point1, point2 (Tuple)
        Salida: node1, node2 (Node)
        """
        node1 = None
        node2 = None
        for node in self.list_nodes:
            for nodePoint in node.Points:
                if point1 == nodePoint:
                    node1 = node
                if point2 == nodePoint:
                    node2 = node
        return node1, node2

    def makeNodeConnections(self):
        """
        Crea las conexiones entre nodos y asigna los valores de voltaje y
        corriente de cada uno
        Autor: Jose Retana
        """
        for resistance in self.list_res:
            node1 = None
            node2 = None
            for node in self.list_nodes:
                for point in node.Points:
                    if resistance.anchorPoints[0].center == point:
                        node1 = node
                    elif resistance.anchorPoints[1].center == point:
                        node2 = node
            voltage = randint(1, 1000)/100
            self.graph.makeconection(node1.name, node2.name, voltage)
            resistance.voltage = voltage
            current = randint(0,1000)
            resistance.current = current

        for power in self.list_pow:
            current = randint(0, 1000)
            power.current = current



