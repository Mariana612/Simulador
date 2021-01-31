import sys
import pygame
from DesignMode import DesignMode
from pygame.locals import *

pygame.init()


class Start:
    """
Clase de inicial
Autor: Mariana Navarro
    """
    def __init__(self):
        """
Incializador de la clasr
Autor:Mariana Navarro
        """
        self.screen = pygame.display.set_mode((1000, 600))
        self.screen.fill([243, 243, 243])
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Simulador')
        self.font = pygame.font.SysFont('timesnewroman', 36)
        self.fileFont = pygame.font.SysFont('timesnewroman', 20)

        self.initialCall()

    def initialCall(self):
        """
Llamada inicial
Autor:Mariana Navarro
                """
        # Images
        logo = pygame.image.load("Imgs\\logo.png").convert_alpha()
        bg = pygame.image.load("Imgs\\bg.png").convert_alpha()
        design_rect = pygame.Rect((440, 255, 150, 50))
        import_rect = pygame.Rect((440, 400, 150, 50))
        on = True
        click = False
        while on:
            mx, my = pygame.mouse.get_pos()
            click = False
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

            if import_rect.collidepoint((mx, my)) and click:
                self.importMenu()

    def importCircuit(self,filename):
        """
Función para la importación de un circuito
Autor: Ignacio Vargas
Entrada: Nombre del archivo
        """
        import json, os

        path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'circuits')) #agarra el path de circuits
        os.makedirs(path, exist_ok=True) #crea el directorio de circuits si no existe
        try:
            with open(os.path.join(path,filename+'.txt'), 'r') as f: #hay que acer el path.join para que cree un archivo y no un directorio
                circuitList = json.load(f)
        except:
            print("ERROR: No se pudo abrir el archivo especificado")
            return

        DesignMode(self.screen, self.clock, circuitList)

    def importMenu(self):
        """
Función que contiene el menú de importación
Autor: Ignacio Vargas
        """
        from pathvalidate import sanitize_filepath
        running = True
        filenameString = ""
        LIGHTBLUE = (154,169,182)
        WHITE = (255,255,255)
        ORANGE = (253,160,40)
        cancel_button = pygame.Rect((290, 410, 120, 50))
        accept_button = pygame.Rect((590, 410, 120, 50))


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
                    elif event.key == pygame.K_RETURN:
                        if len(filenameString) > 0:
                            self.importCircuit(filenameString)
                            running = False
                    elif self.fileFont.size(filenameString + event.unicode)[0] < 190: #[0] accesa el width ya que returna (w,h)
                        filenameString += event.unicode
                        filenameString = sanitize_filepath(filenameString)
                elif event.type == MOUSEBUTTONDOWN and event.button == 1:  # check for left mouse click
                    click = True

            mx, my = pygame.mouse.get_pos()
            if accept_button.collidepoint((mx, my)) and click:
                if len(filenameString) > 0:
                    self.importCircuit(filenameString)
                    running = False
            elif cancel_button.collidepoint((mx, my)) and click:
                running=False

            if running:  # tal vez ocupe agregar un blit al fondo
                pygame.draw.rect(self.screen, LIGHTBLUE,(250,194,500,300)) #main box
                pygame.draw.rect(self.screen, WHITE, (400, 330, 200, 30)) #text box
                text = self.font.render("Insert import filename:", True, WHITE) #insert import...
                self.screen.blit(text, [323, 230])
                text = self.fileFont.render(".txt", True, (0,0,0)) #.txt
                self.screen.blit(text, [605, 335])
                text = self.fileFont.render(filenameString, True, (0,0,0)) #nombre
                self.screen.blit(text, [405, 335])
                #botones
                pygame.draw.rect(self.screen, ORANGE, cancel_button)
                pygame.draw.rect(self.screen, ORANGE, accept_button)
                text = self.font.render("Cancel", True, WHITE) #cancel
                self.screen.blit(text, [300, 415])
                text = self.font.render("Accept", True, WHITE) #accept
                self.screen.blit(text, [600, 415])
                pygame.display.flip()
                self.clock.tick(60)

        return


start = Start()
