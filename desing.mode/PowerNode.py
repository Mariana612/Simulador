import pygame


class PowerNode(object):
    """
Clase que representa al nodo de fuente
Autor: Mariana Navarro
    """
    def __init__(self, x, y, width, height, name="", value="", rotated=False):
        """
Inicializador de la clase
Autor: Mariana Navarro
Entradas: posición x, posición y, ancho, altura,nombre, valor, rotación
        """
        self.rect = pygame.Rect((x, y, width, height))
        self.name = name
        self.value = value
        self.rotated = rotated
        self.sum = 0
        self.anchorPoints = [pygame.Rect((self.rect.center[0] - 55, self.rect.center[1] - 10, 10, 10)),
                             pygame.Rect((self.rect.center[0] + 55, self.rect.center[1] - 10, 10, 10))]
        self.current = None

    # def recurisve(self,num):
    def checkPlacement(self):
        """
Función que revisa el placement del nodo
Autor: Mariana Navarro
        """
        # places y
        num = 96
        num_x = 96
        if not self.rotated:
            num -= 55
            num_x -= 50
        else:
            num -= 50
            num_x -= 55

        while not (num - (self.rect.y-50) >= 0):
            num += 96
        self.setxy(self.rect.x, num)
        while not (num_x - (self.rect.x-50) >= 0):
            num_x += 96
        self.setxy(num_x, self.rect.y)

    def setxy(self, mx, my):
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
        if self.rotated:
            self.anchorPoints = [pygame.Rect((self.rect.center[0] - 55, self.rect.center[1] - 10, 10, 10)),
                                 pygame.Rect((self.rect.center[0] + 55, self.rect.center[1] - 10, 10, 10))]
        else:
            self.anchorPoints = [pygame.Rect((self.rect.center[0] - 5, self.rect.center[1] - 60, 10, 10)),
                                 pygame.Rect((self.rect.center[0] - 5, self.rect.center[1] + 50, 10, 10))]

    def toDict(self):
        """
Función: Pasa los atributos del objeto a un diccionario para formato JSON
Autor: Ignacio Vargas
Salida: Diccionario con el nombre de la variable y su valor
        """
        return {"x": self.rect.x, "y": self.rect.y, "width": self.rect.width, "height": self.rect.height, "name": self.name, "value": self.value, "rotated": self.rotated}
