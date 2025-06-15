import pygame
from utils import draw_text

class MainMenu:
    """
    The main menu: displays options (Start, Settings, Leaderboard)
    and allows navigation via arrows or mouse.
    """
    def __init__(self, surface: pygame.Surface, font: pygame.font.Font):
        self.surface = surface
        self.font    = font

        self.options = ["Start", "Settings", "Leaderboard"]
        self.selected_index = 0

        # Precompute bounding rects for mouse clicks
        self.option_rects = []
        width, height = surface.get_size()
        for i, label in enumerate(self.options):
            text_surf = font.render(label, True, (255,255,255))
            rect = text_surf.get_rect(center=(width//2, 200 + i*60))
            self.option_rects.append((label, rect))

    def draw(self) -> None:
        """Render all menu options, highlighting the selected one."""
        for idx, (label, rect) in enumerate(self.option_rects):
            is_selected = (idx == self.selected_index)
            color = (255,255,0) if is_selected else (255,255,255)
            draw_text(self.surface, label, rect.center, self.font, color=color)

    def handle_event(self, event: pygame.event.Event) -> str|None:
        """
        Process key or mouse input.
        Returns the chosen option label if activated.
        """
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_DOWN, pygame.K_s):
                self.selected_index = (self.selected_index + 1) % len(self.options)
            elif event.key in (pygame.K_UP, pygame.K_w):
                self.selected_index = (self.selected_index - 1) % len(self.options)
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                return self.options[self.selected_index].lower()

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for idx, (label, rect) in enumerate(self.option_rects):
                if rect.collidepoint(event.pos):
                    self.selected_index = idx
                    return label.lower()

        return None
