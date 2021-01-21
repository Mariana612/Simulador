if self.name_int:
    if event.key == pygame.K_BACKSPACE:
        if self.pow:
            self.list_pow[-1].name = self.list_pow[-1].name[:-1]
        else:
            self.list_res[-1].name = self.list_res[-1].name[:-1]
    else:
        if self.pow:
            if len(self.list_pow[-1].name) < 18:
                self.list_pow[-1].name += event.unicode
        else:
            if len(self.list_res[-1].name) < 18:
                self.list_res[-1].name += event.unicode

if self.value_entry:
    if event.key == pygame.K_BACKSPACE:
        if self.pow:
            self.list_pow[-1].value = self.list_pow[-1].value[:-1]
        else:
            self.list_res[-1].value = self.list_res[-1].value[:-1]
    else:
        if self.pow:
            if len(self.list_pow[-1].value) < 18:
                try:
                    int(event.unicode)
                    self.list_pow[-1].value += event.unicode
                except ValueError:
                    pass
        else:
            if len(self.list_res[-1].value) < 18:
                try:
                    int(event.unicode)
                    self.list_res[-1].value += event.unicode
                except ValueError:
                    pass
if self.pow:
    rectangle = pygame.draw.rect(self.screen, (243, 243, 243), (240, 255, 250, 25))
    rectangle = pygame.draw.rect(self.screen, (243, 243, 243), (240, 320, 250, 25))

    text = self.font.render(self.list_pow[-1].name, True, (50, 50, 50))
    text2 = self.font.render(self.list_pow[-1].value, True, (50, 50, 50))

    self.screen.blit(text, (245, 255))
    self.screen.blit(text2, (245, 320))
else:
    rectangle = pygame.draw.rect(self.screen, (243, 243, 243), (240, 255, 250, 25))
    rectangle = pygame.draw.rect(self.screen, (243, 243, 243), (240, 320, 250, 25))

    text = self.font.render(self.list_res[-1].name, True, (50, 50, 50))
    text2 = self.font.render(self.list_res[-1].value, True, (50, 50, 50))

    self.screen.blit(text, (245, 255))
    self.screen.blit(text2, (245, 320))

    def uselessRect(self):
        # middle
        pygame.draw.rect(self.screen, (174, 169, 169), (50, 250, 100, 110))
        pygame.draw.rect(self.screen, (174, 169, 169), (241, 250, 100, 110))
        pygame.draw.rect(self.screen, (174, 169, 169), (432, 250, 100, 110))
        pygame.draw.rect(self.screen, (174, 169, 169), (623, 250, 100, 110))

        # up
        pygame.draw.rect(self.screen, (174, 169, 169), (50, 80, 100, 110))
        pygame.draw.rect(self.screen, (174, 169, 169), (241, 80, 100, 110))
        pygame.draw.rect(self.screen, (174, 169, 169), (432, 80, 100, 110))
        pygame.draw.rect(self.screen, (174, 169, 169), (623, 80, 100, 110))

        # down
        pygame.draw.rect(self.screen, (174, 169, 169), (50, 420, 100, 110))
        pygame.draw.rect(self.screen, (174, 169, 169), (241, 420, 100, 110))
        pygame.draw.rect(self.screen, (174, 169, 169), (432, 420, 100, 110))
        pygame.draw.rect(self.screen, (174, 169, 169), (623, 420, 100, 110))

        pygame.display.flip()