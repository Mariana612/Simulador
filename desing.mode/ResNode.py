import pygame


class ResNode(object):
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect((x, y, width, height))
        self.name = ""
        self.value =""

    def checkPlacementRes(self):
        # places y
        if self.rect.y <= 180:
            self.setxyRes(self.rect.x, 130)
        elif self.rect.y <= 320:
            self.setxyRes(self.rect.x, 300)
        else:
            self.setxyRes(self.rect.x, 470)

        # places x
        if self.rect.x <= 310:
            if self.rect.y == 250 and self.rect.x <= 140:
                self.setxyRes(70, 250)
            else:
                self.setxyRes(251, self.rect.y)
        else:
            if self.rect.y == 250 and self.rect.x >= 530:
                self.setxyRes(643, 250)
            else:
                self.setxyRes(452, self.rect.y)

    def setxyRes(self, mx, my):
        self.rect.x = mx
        self.rect.y = my