import pygame
from utils import draw_text

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font   = pygame.font.Font(None, 48)
        self.start_btn    = pygame.Rect(300, 150, 200, 50)
        self.leader_btn   = pygame.Rect(300, 250, 200, 50)
        self.settings_btn = pygame.Rect(300, 350, 200, 50)

    def draw(self):
        pygame.draw.rect(self.screen, (255,255,255), self.start_btn, 2)
        draw_text(self.screen, "Start",       self.start_btn.center,    self.font)

        pygame.draw.rect(self.screen, (255,255,255), self.leader_btn, 2)
        draw_text(self.screen, "Leaderboard", self.leader_btn.center,  self.font)

        pygame.draw.rect(self.screen, (255,255,255), self.settings_btn, 2)
        draw_text(self.screen, "Settings",    self.settings_btn.center, self.font)

    def handle_event(self, event):
        """
        Return 'start', 'leader', or 'settings' when clicked; else None.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.start_btn.collidepoint(event.pos):
                return 'start'
            if self.leader_btn.collidepoint(event.pos):
                return 'leader'
            if self.settings_btn.collidepoint(event.pos):
                return 'settings'
        return None
