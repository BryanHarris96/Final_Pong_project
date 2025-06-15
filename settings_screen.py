import pygame
from utils import draw_text

class SettingsScreen:
    """
    Let players adjust:
      - Number of matches
      - Games per match
      - Points needed per game

    Uses simple +/- buttons next to each value.
    """

    def __init__(
        self,
        surface: pygame.Surface,
        font: pygame.font.Font,
        initial_settings: dict|None = None
    ):
        self.surface = surface
        self.font    = font

        # Default or loaded
        self.values = {
            "num_matches":    3,
            "games_per_match": 5,
            "points_to_win":   11
        }
        if initial_settings:
            self.values.update(initial_settings)

        # Button layout
        w, h = surface.get_size()
        self.fields = ["num_matches", "games_per_match", "points_to_win"]
        self.labels = {
            "num_matches":    "Matches:",
            "games_per_match": "Games/Match:",
            "points_to_win":   "Points/Game:"
        }
        self.buttons = {}  # (field, 'minus'/'plus') => pygame.Rect
        for i, field in enumerate(self.fields):
            y = 200 + i*60
            # minus
            r_minus = pygame.Rect(w//2 - 80, y, 30, 30)
            # plus
            r_plus  = pygame.Rect(w//2 + 50, y, 30, 30)
            self.buttons[(field,"minus")] = r_minus
            self.buttons[(field,"plus")]  = r_plus

        # Back button
        self.back_rect = pygame.Rect(20,20,100,40)

    def draw(self) -> None:
        """Render labels, current values, +/– buttons, and Back."""
        overlay = pygame.Surface(self.surface.get_size())
        overlay.set_alpha(200)
        overlay.fill((0,0,0))
        self.surface.blit(overlay, (0,0))

        for i, field in enumerate(self.fields):
            label = self.labels[field]
            val   = self.values[field]
            y     = 200 + i*60
            draw_text(self.surface, label, (self.surface.get_width()//2 - 50, y+15), self.font)
            draw_text(self.surface, str(val), (self.surface.get_width()//2, y+15), self.font)

            # minus button
            r_minus = self.buttons[(field,"minus")]
            pygame.draw.rect(self.surface, (255,255,255), r_minus, 2)
            draw_text(self.surface, "-", r_minus.center, self.font)

            # plus button
            r_plus = self.buttons[(field,"plus")]
            pygame.draw.rect(self.surface, (255,255,255), r_plus, 2)
            draw_text(self.surface, "+", r_plus.center, self.font)

        # Back button
        pygame.draw.rect(self.surface, (255,255,255), self.back_rect, 2)
        draw_text(self.surface, "Back", self.back_rect.center, self.font)

    def handle_event(self, event: pygame.event.Event) -> dict|str|None:
        """
        On click:
         - If +/- clicked, adjust the value
         - If Back clicked, return 'BACK'
         - If Enter pressed, return self.values
        """
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_SPACE):
            return self.values

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            # Back?
            if self.back_rect.collidepoint(pos):
                return "BACK"
            # +/- buttons
            for (field,kind), rect in self.buttons.items():
                if rect.collidepoint(pos):
                    if kind == "minus" and self.values[field] > 1:
                        self.values[field] -= 1
                    elif kind == "plus":
                        self.values[field] += 1
                    return None

        return None
