# settings_screen.py

import pygame
from utils import draw_text

class SettingsScreen:
    """
    Adjust tournament settings with dynamic +/- buttons:
      - Number of matches
      - Games per match
      - Points needed per game
    """

    def __init__(
        self,
        surface: pygame.Surface,
        font: pygame.font.Font,
        initial_settings: dict | None = None
    ):
        self.surface = surface
        self.font    = font

        # Default values or load provided ones
        self.values = {
            "num_matches":     3,
            "games_per_match": 5,
            "points_to_win":  11
        }
        if initial_settings:
            self.values.update(initial_settings)

        # Fields and their display labels
        self.fields = ["num_matches", "games_per_match", "points_to_win"]
        self.labels = {
            "num_matches":     "Matches:",
            "games_per_match": "Games/Match:",
            "points_to_win":   "Points/Game:"
        }

        # Vertical spacing
        self.spacing = 80
        w, h = self.surface.get_size()
        total_height = self.spacing * (len(self.fields) - 1)
        # Center the block vertically
        self.start_y = (h // 2) - (total_height // 2)

        # Back button in top-left
        self.back_rect = pygame.Rect(20, 20, 100, 40)

    def draw(self) -> None:
        """
        Render labels, values, and +/- buttons without overlap,
        by measuring text widths at runtime.
        """
        # Dim background
        overlay = pygame.Surface(self.surface.get_size())
        overlay.set_alpha(200)
        overlay.fill((0,0,0))
        self.surface.blit(overlay, (0,0))

        w, _ = self.surface.get_size()

        for i, field in enumerate(self.fields):
            y_center = self.start_y + i * self.spacing

            # 1) Draw label
            label_text = self.labels[field]
            label_surf = self.font.render(label_text, True, (255,255,255))
            label_rect = label_surf.get_rect(midleft=(w//2 - 200, y_center))
            self.surface.blit(label_surf, label_rect)

            # 2) Draw minus button to the right of label
            minus_rect = pygame.Rect(0, 0, 30, 30)
            minus_rect.center = (label_rect.right + 30, y_center)
            pygame.draw.rect(self.surface, (255,255,255), minus_rect, 2)
            draw_text(self.surface, "-", minus_rect.center, self.font)

            # 3) Draw current value to the right of minus
            val_text = str(self.values[field])
            val_surf = self.font.render(val_text, True, (255,255,255))
            val_rect = val_surf.get_rect(midleft=(minus_rect.right + 20, y_center))
            self.surface.blit(val_surf, val_rect)

            # 4) Draw plus button to the right of value
            plus_rect = pygame.Rect(0, 0, 30, 30)
            plus_rect.center = (val_rect.right + 30, y_center)
            pygame.draw.rect(self.surface, (255,255,255), plus_rect, 2)
            draw_text(self.surface, "+", plus_rect.center, self.font)

            # Save button rects for click detection
            setattr(self, f"{field}_minus_rect", minus_rect)
            setattr(self, f"{field}_plus_rect", plus_rect)

        # Draw Back button
        pygame.draw.rect(self.surface, (255,255,255), self.back_rect, 2)
        draw_text(self.surface, "Back", self.back_rect.center, self.font)

    def handle_event(self, event: pygame.event.Event) -> dict | str | None:
        """
        - Clicking +/- adjusts the corresponding setting (min 1).
        - Clicking Back returns 'BACK'.
        - Pressing Enter/Space returns the current values dict.
        """
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_SPACE):
            return self.values

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos

            # Back button?
            if self.back_rect.collidepoint(pos):
                return "BACK"

            # Check each field's minus/plus rect
            for field in self.fields:
                minus_rect = getattr(self, f"{field}_minus_rect")
                plus_rect  = getattr(self, f"{field}_plus_rect")

                if minus_rect.collidepoint(pos) and self.values[field] > 1:
                    self.values[field] -= 1
                    return None
                if plus_rect.collidepoint(pos):
                    self.values[field] += 1
                    return None

        return None
