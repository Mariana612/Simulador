import pygame


class ResNode(object):
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect((x, y, width, height))
        self.name = ""
        self.value = ""
        self.rotated = False
        self.anchorPoints = None

    def checkPlacementRes(self):
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

        while not (num_x - (self.rect.x-24) >= 0):
            num_x += 96
        self.setxyRes(num_x, self.rect.y)

    def setxyRes(self, mx, my):
        self.rect.x = mx
        self.rect.y = my

    def setAnchorPoints(self, surface):
        self.anchorPoints = (pygame.draw.circle(surface, (200, 0, 0), (self.rect.x-40, self.rect.y), 5),
                             pygame.draw.circle(surface, (200, 0, 0), (self.rect.x+40, self.rect.y), 5))
