import pygame
from pygame.locals import K_BACKSPACE, K_RETURN, K_KP_ENTER, MOUSEBUTTONDOWN, KEYDOWN
from constants import COLOR_FG, COLOR_INACTIVE, COLOR_ACTIVE
from utils     import draw_text

class InputBox:
    """
    A rectangular text-entry box.
    Click to activate, type to enter text, Enter to submit.
    """

    def __init__(
        self,
        rect: tuple[int,int,int,int],
        font: pygame.font.Font
    ):
        """
        :param rect: (x, y, width, height) of the box
        :param font: font used to render the text
        """
        self.rect   = pygame.Rect(rect)
        self.font   = font
        self.text   = ""        # current contents
        self.active = False     # True when clicked into

    def handle_event(self, event: pygame.event.Event) -> str|None:
        """
        Process mouse and keyboard events.
        :returns: the submitted text when Enter is pressed, else None.
        """
        if event.type == MOUSEBUTTONDOWN:
            # Click activates/deactivates the box
            self.active = self.rect.collidepoint(event.pos)

        elif event.type == KEYDOWN and self.active:
            if event.key in (K_RETURN, K_KP_ENTER):
                # Submit current text
                submitted = self.text
                self.text = ""
                return submitted
            elif event.key == K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                # Append typed character
                self.text += event.unicode

        return None

    def draw(self, surface: pygame.Surface) -> None:
        """
        Render the current text (or placeholder) and border.
        Active box is drawn in bright; inactive in muted color.
        """
        display_text = self.text if self.text else "..."
        color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        # Draw text centered in the box
        draw_text(surface, display_text, self.rect.center, self.font, color=color)
        # Draw border
        border_color = COLOR_FG if self.active else COLOR_INACTIVE
        pygame.draw.rect(surface, border_color, self.rect, width=2)
