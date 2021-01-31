import pygame


class ResNode(object):
    """
Clase que representa al nodo de resistencia
Autor: Mariana Navarro
    """
    def __init__(self, x, y, width, height, name="", value="", rotated=False):
        """
Inicializador de la clase
Autor: Mariana Navarro
Entradas: posición x, posición y, ancho, alto, nombre, valor, rotado o no
        """
        self.rect = pygame.Rect((x, y, width, height))
        self.name = name
        self.value = value
        self.rotated = rotated
        self.anchorPoints = [pygame.Rect((self.rect.center[0] - 5, self.rect.center[1] - 60, 10, 10)),
                             pygame.Rect((self.rect.center[0] - 5, self.rect.center[1] + 50, 10, 10))]
        self.voltage = None
        self.current = None

    def checkPlacementRes(self):
        """
Función que revisa el placement del nodo
Autor: Mariana Navarro
        """
        # places y
        # places y
        num = 99
        num_x = 99
        if not self.rotated:
            num -= 13
            num_x -= 31
        else:
            num -= 31
            num_x -= 13

        while not (num - (self.rect.y) >= 0):
            num += 96
        self.setxyRes(self.rect.x, num)

        while not (num_x - (self.rect.x - 24) >= 0):
            num_x += 96
        self.setxyRes(num_x, self.rect.y)

    def setxyRes(self, mx, my):
        """
Función setter de las posiciones x y y
Autor: Mariana Navarro
        """
        self.rect.x = mx
        self.rect.y = my

    def setAnchorPoints(self):
        """
Función setter de los anchor points
Autor: Jose Retana
        """
        if not self.rotated:
            self.anchorPoints = [pygame.Rect((self.rect.center[0] - 35, self.rect.center[1] - 9, 10, 10)),
                                 pygame.Rect((self.rect.center[0] + 28, self.rect.center[1] - 9, 10, 10))]
        else:
            self.anchorPoints = [pygame.Rect((self.rect.center[0] - 26, self.rect.center[1] - 18, 10, 10)),
                                 pygame.Rect((self.rect.center[0] - 26, self.rect.center[1] + 43, 10, 10))]

    def toDict(self):
        """
Función: Pasa los atributos del objeto a un diccionario para formato JSON
Autor: Ignacio Vargas
Salida: Diccionario con el nombre de la variable y su valor
        """
        return {"x": self.rect.x, "y": self.rect.y, "width": self.rect.width, "height": self.rect.height, "name": self.name, "value": self.value, "rotated": self.rotated}
