import pygame
import time
from utils import draw_text
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

class TransitionScreen:
    """
    Shows an interim message for a fixed duration (e.g. 'Next Match' countdown).
    """

    def __init__(
        self,
        surface: pygame.Surface,
        title: str,
        subtitle: str,
        font_title: pygame.font.Font,
        font_sub: pygame.font.Font,
        duration: float = 2.0
    ):
        self.surface     = surface
        self.title       = title
        self.subtitle    = subtitle
        self.font_title  = font_title
        self.font_sub    = font_sub
        self.end_time    = time.time() + duration

    def draw(self) -> None:
        """Render title + subtitle centered."""
        self.surface.fill((0,0,0))
        draw_text(
            self.surface, self.title,
            (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 20),
            self.font_title
        )
        draw_text(
            self.surface, self.subtitle,
            (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 20),
            self.font_sub
        )

    def tick(self) -> bool:
        """
        Returns True once duration has elapsed, signaling the transition is done.
        """
        return time.time() >= self.end_time
