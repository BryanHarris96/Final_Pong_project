import pygame
from utils import draw_text
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

class WinScreen:
    """
    Display a title message (e.g. 'Player X wins match') and a prompt.
    """
    def __init__(
        self,
        surface: pygame.Surface,
        font: pygame.font.Font,
        title: str,
        prompt: str="Press any key to continue"
    ):
        self.surface = surface
        self.font    = font
        self.title   = title
        self.prompt  = prompt

    def draw(self) -> None:
        """Fill screen then draw title + prompt centered."""
        self.surface.fill((0,0,0))
        draw_text(
            self.surface, self.title,
            (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 20),
            self.font
        )
        draw_text(
            self.surface, self.prompt,
            (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 20),
            self.font
        )
