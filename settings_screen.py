import pygame
import json
import os
from utils import draw_text

SETTINGS_FILE = 'settings.json'

class SettingsScreen:
    def __init__(self, screen, font, initial_settings=None):
        self.screen = screen
        self.w, self.h = screen.get_size()
        self.font = font

        # Load or initialize settings
        if initial_settings:
            self.values = dict(initial_settings)
        else:
            self.values = self._load_persisted() or {
                'num_matches': 1,
                'games_per_match': 1,
                'points_to_win': 1
            }

        self.items = ['num_matches', 'games_per_match', 'points_to_win']
        self.labels = {
            'num_matches':     "Number of Matches",
            'games_per_match': "Games per Match",
            'points_to_win':   "Points to Win"
        }

        # Layout: 8 rows (title, 3×(label+control), confirm), evenly spaced
        rows = 8
        step = self.h / (rows + 1)
        self.ys = [step * i for i in range(1, rows+1)]
        x_center = self.w // 2
        btn_w, btn_h = 40, 40

        # +/- buttons
        self.decr = {}
        self.incr = {}
        for idx, key in enumerate(self.items):
            controls_y = self.ys[2 + idx*2]  # rows 3,5,7
            self.decr[key] = pygame.Rect(x_center - 80 - btn_w//2, controls_y - btn_h//2, btn_w, btn_h)
            self.incr[key] = pygame.Rect(x_center + 80 - btn_w//2, controls_y - btn_h//2, btn_w, btn_h)

        # Confirm button (row 8)
        y_confirm = self.ys[7]
        self.confirm = pygame.Rect(x_center - 100, y_confirm - 25, 200, 50)

        # Back button (top-left)
        self.back = pygame.Rect(20, 20, 100, 40)

    def _load_persisted(self):
        if os.path.isfile(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if all(k in data for k in self.items):
                        return data
            except:
                pass
        return None

    def _save(self):
        try:
            with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.values, f, indent=2)
        except Exception as e:
            print("Error saving settings:", e)

    def draw(self):
        self.screen.fill((0,0,0))
        x_center = self.w//2

        # Title (row1)
        draw_text(self.screen, "Settings", (x_center, self.ys[0]), self.font)

        # Rows 2-7: label and controls
        for idx, key in enumerate(self.items):
            label_y    = self.ys[1 + idx*2]  # rows2,4,6
            controls_y = self.ys[2 + idx*2]  # rows3,5,7
            draw_text(self.screen, self.labels[key],  (x_center, label_y), self.font)
            draw_text(self.screen, str(self.values[key]), (x_center, controls_y), self.font)
            pygame.draw.rect(self.screen, (255,255,255), self.decr[key], 2)
            draw_text(self.screen, "-", self.decr[key].center, self.font)
            pygame.draw.rect(self.screen, (255,255,255), self.incr[key], 2)
            draw_text(self.screen, "+", self.incr[key].center, self.font)

        # Confirm (row8)
        enabled = all(v >= 1 for v in self.values.values())
        color = (255,255,255) if enabled else (100,100,100)
        pygame.draw.rect(self.screen, color, self.confirm, 2)
        draw_text(self.screen, "Confirm", self.confirm.center, self.font)

        # Back
        pygame.draw.rect(self.screen, (255,255,255), self.back, 2)
        draw_text(self.screen, "Back", self.back.center, self.font)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Back?
            if self.back.collidepoint(event.pos):
                return 'BACK'
            # +/- adjustments
            for key in self.items:
                if self.decr[key].collidepoint(event.pos):
                    self.values[key] = max(1, self.values[key] - 1)
                if self.incr[key].collidepoint(event.pos):
                    self.values[key] += 1
            # Confirm?
            if self.confirm.collidepoint(event.pos) and all(v >= 1 for v in self.values.values()):
                self._save()
                return dict(self.values)
        return None
