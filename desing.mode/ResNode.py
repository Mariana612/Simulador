import pygame


class ResNode(object):
    def __init__(self, x, y, width, height, name="", value="", rotated=False):
        self.rect = pygame.Rect((x, y, width, height))
        self.name = name
        self.value = value
        self.rotated = rotated
        self.anchorPoints = [pygame.Rect((self.rect.center[0] - 5, self.rect.center[1] - 60, 10, 10)),
                             pygame.Rect((self.rect.center[0] - 5, self.rect.center[1] + 50, 10, 10))]

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

        while not (num_x - (self.rect.x - 24) >= 0):
            num_x += 96
        self.setxyRes(num_x, self.rect.y)

    def setxyRes(self, mx, my):
        self.rect.x = mx
        self.rect.y = my

    def setAnchorPoints(self):
        if not self.rotated:
            self.anchorPoints = [pygame.Rect((self.rect.center[0] - 35, self.rect.center[1] - 9, 10, 10)),
                                 pygame.Rect((self.rect.center[0] + 28, self.rect.center[1] - 9, 10, 10))]
        else:
            self.anchorPoints = [pygame.Rect((self.rect.center[0] - 26, self.rect.center[1] - 18, 10, 10)),
                                 pygame.Rect((self.rect.center[0] - 26, self.rect.center[1] + 43, 10, 10))]

    def toDict(self):
        return {"x": self.rect.x, "y": self.rect.y, "width": self.rect.width, "height": self.rect.height, "name": self.name, "value": self.value, "rotated": self.rotated}
