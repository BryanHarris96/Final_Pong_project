import pygame

def draw_text(surface, text, center, font, color=(255,255,255)):
    """
    Render `text` centered at `center` on `surface` using `font`.
    """
    txt_surf = font.render(text, True, color)
    txt_rect = txt_surf.get_rect(center=center)
    surface.blit(txt_surf, txt_rect)
