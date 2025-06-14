import pygame

class InputBox:
    """Simple Pygame text-input box."""
    def __init__(self, rect, font):
        self.rect           = pygame.Rect(rect)
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active   = pygame.Color('dodgerblue2')
        self.color          = self.color_inactive
        self.text           = ''
        self.font           = font
        self.txt_surf       = font.render('', True, self.color)
        self.active         = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Toggle activation
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = self.color_active if self.active else self.color_inactive

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                entered = self.text
                self.text   = ''
                self.txt_surf = self.font.render('', True, self.color)
                return entered
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
            self.txt_surf = self.font.render(self.text, True, self.color)

        return None

    def draw(self, surface):
        surface.blit(self.txt_surf, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(surface, self.color, self.rect, 2)
