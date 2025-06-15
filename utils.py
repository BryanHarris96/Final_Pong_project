import pygame
from typing import Tuple

def get_font(size: int, path: str|None=None) -> pygame.font.Font:
    """
    Load and return a pygame.Font at the given size.
    """
    if path is None:
        return pygame.font.SysFont(None, size)
    return pygame.font.Font(path, size)

def draw_text(
    surface: pygame.Surface,
    text: str,
    position: Tuple[int,int],
    font: pygame.font.Font,
    color: Tuple[int,int,int]=(255,255,255)
) -> None:
    """
    Render text centered at `position`.
    """
    rendered = font.render(text, True, color)
    rect     = rendered.get_rect(center=position)
    surface.blit(rendered, rect)
