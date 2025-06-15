import pygame
from utils import draw_text

class PauseMenu:
    """
    Overlay menu when paused: Resume, Settings, Main Menu, Quit.
    """

    def __init__(self, surface: pygame.Surface, font: pygame.font.Font):
        self.surface = surface
        self.font    = font
        self.options = ["Resume", "Settings", "Main Menu", "Quit"]
        self.selected = 0

        # Layout
        w, h = surface.get_size()
        self.rects = []
        for i, opt in enumerate(self.options):
            rect = pygame.Rect(0, 0, 200, 40)
            rect.center = (w//2, 200 + i*60)
            self.rects.append((opt.lower().replace(" ", "_"), rect))

    def draw(self) -> None:
        """Draw transparent overlay and menu options."""
        overlay = pygame.Surface(self.surface.get_size())
        overlay.set_alpha(180)
        overlay.fill((0,0,0))
        self.surface.blit(overlay, (0,0))

        for idx, (key, rect) in enumerate(self.rects):
            label = self.options[idx]
            color = (255,255,0) if idx == self.selected else (255,255,255)
            pygame.draw.rect(self.surface, color, rect, width=2)
            draw_text(self.surface, label, rect.center, self.font, color=color)

    def handle_event(self, event: pygame.event.Event) -> str|None:
        """
        Return one of:
          'resume', 'settings', 'main_menu', 'quit'
        when the user activates the corresponding option.
        """
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_DOWN, pygame.K_s):
                self.selected = (self.selected + 1) % len(self.options)
            elif event.key in (pygame.K_UP, pygame.K_w):
                self.selected = (self.selected - 1) % len(self.options)
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                return self.rects[self.selected][0]

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for idx, (_, rect) in enumerate(self.rects):
                if rect.collidepoint(event.pos):
                    self.selected = idx
                    return self.rects[idx][0]

        return None
