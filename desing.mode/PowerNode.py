import pygame


class PowerNode(object):
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect((x, y, width, height))
        self.name = ""
        self.value = ""
        self.rotated = False
        self.sum = 0

    # def recurisve(self,num):
    def checkPlacement(self):
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
        self.rect.x = mx
        self.rect.y = my
