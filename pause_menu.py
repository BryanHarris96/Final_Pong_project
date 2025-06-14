import pygame
from utils import draw_text

class PauseMenu:
    def __init__(self, screen, font):
        self.screen = screen
        self.w, self.h = screen.get_size()
        self.font = font

        # Define button rects (Resume, Settings, Main Menu, Quit)
        btn_w, btn_h = 200, 50
        x = (self.w - btn_w) // 2
        start_y = self.h//3
        gap = 70

        self.buttons = {
            'resume'    : pygame.Rect(x, start_y,        btn_w, btn_h),
            'settings'  : pygame.Rect(x, start_y+gap,    btn_w, btn_h),
            'main_menu' : pygame.Rect(x, start_y+2*gap,  btn_w, btn_h),
            'quit'      : pygame.Rect(x, start_y+3*gap,  btn_w, btn_h),
        }

    def draw(self):
        # Dim background
        overlay = pygame.Surface((self.w, self.h))
        overlay.set_alpha(180)
        overlay.fill((0,0,0))
        self.screen.blit(overlay, (0,0))

        # Title
        draw_text(self.screen, "Paused", (self.w//2, self.h//4), self.font)
        labels = {
            'resume':    "Resume",
            'settings':  "Settings",
            'main_menu': "Main Menu",
            'quit':      "Quit"
        }

        for key, rect in self.buttons.items():
            pygame.draw.rect(self.screen, (255,255,255), rect, 2)
            draw_text(self.screen, labels[key], rect.center, self.font)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for key, rect in self.buttons.items():
                if rect.collidepoint(event.pos):
                    return key
        return None
