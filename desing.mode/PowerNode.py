import pygame


class PowerNode(object):
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect((x, y, width, height))
        self.name = ""
        self.value = ""

    def checkPlacement(self):
        # places y
        if self.rect.y <= 180:
            self.setxy(self.rect.x, 80)
        elif self.rect.y <= 320:
            self.setxy(self.rect.x, 250)
        else:
            self.setxy(self.rect.x, 420)

        # places x
        if self.rect.x <= 310:
            if self.rect.y == 250 and self.rect.x <= 140:
                self.setxy(50, 250)
            else:
                self.setxy(241, self.rect.y)
        else:
            if self.rect.y == 250 and self.rect.x >= 530:
                self.setxy(623, 250)
            else:
                self.setxy(432, self.rect.y)

    def setxy(self, mx, my):
        self.rect.x = mx
        self.rect.y = my
