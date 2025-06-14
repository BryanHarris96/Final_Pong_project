# game.py
import pygame
from utils import draw_text

class Paddle:
    def __init__(self, x, y, w, h, speed, up_key, down_key):
        self.rect     = pygame.Rect(x, y, w, h)
        self.speed    = speed
        self.up_key   = up_key
        self.down_key = down_key

    def move(self, keys, screen_h):
        if keys[self.up_key] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[self.down_key] and self.rect.bottom < screen_h:
            self.rect.y += self.speed

    def draw(self, surf):
        pygame.draw.rect(surf, (255,255,255), self.rect)

class Ball:
    def __init__(self, x, y, r, speed_x, speed_y):
        self.x       = x
        self.y       = y
        self.r       = r
        self.speed_x = speed_x
        self.speed_y = speed_y

    def update(self, paddles, screen_w, screen_h):
        self.x += self.speed_x
        self.y += self.speed_y

        # bounce off top/bottom
        if self.y - self.r <= 0 or self.y + self.r >= screen_h:
            self.speed_y *= -1

        # bounce off paddles
        for p in paddles:
            coll_x = self.x + self.r * (1 if self.speed_x>0 else -1)
            if p.rect.collidepoint(coll_x, self.y):
                self.speed_x *= -1
                break

    def draw(self, surf):
        """Draw the ball as a filled circle."""
        pygame.draw.circle(surf, (255,255,255), (int(self.x), int(self.y)), self.r)

class Game:
    def __init__(self, screen, player_names, settings, first_player=0):
        self.screen   = screen
        self.w, self.h= screen.get_size()
        self.names    = player_names[:2]
        self.settings = settings

        # paddles
        ph, pw, sp = 100, 10, 5
        self.paddles = [
            Paddle(10, (self.h-ph)//2, pw, ph, sp, pygame.K_w, pygame.K_s),
            Paddle(self.w-20, (self.h-ph)//2, pw, ph, sp, pygame.K_UP, pygame.K_DOWN)
        ]

        # ball
        speed = 4
        direction = 1 if first_player==1 else -1
        self.ball = Ball(self.w//2, self.h//2, 8, speed * direction, speed)

        # scores
        self.points    = {self.names[0]: 0, self.names[1]: 0}
        self.game_wins = {self.names[0]: 0, self.names[1]: 0}

        self.current_server = first_player
        self.font = pygame.font.Font(None, 48)

    def reset_ball(self, start_right=True):
        self.ball.x = self.w//2
        self.ball.y = self.h//2
        self.ball.speed_x = abs(self.ball.speed_x) * (1 if start_right else -1)

    def update(self):
        keys = pygame.key.get_pressed()
        for p in self.paddles:
            p.move(keys, self.h)

        self.ball.update(self.paddles, self.w, self.h)

        # scoring
        if self.ball.x < 0:
            scorer = self.names[1]
            self.points[scorer] += 1
            self.reset_ball(start_right=True)
            return self._check_point_end(scorer)
        elif self.ball.x > self.w:
            scorer = self.names[0]
            self.points[scorer] += 1
            self.reset_ball(start_right=False)
            return self._check_point_end(scorer)
        return None

    def _check_point_end(self, scorer):
        pts_to_win = self.settings['points_to_win']
        if self.points[scorer] >= pts_to_win:
            self.game_wins[scorer] += 1
            return scorer
        return None

    def prepare_next_round(self):
        for k in self.points:
            self.points[k] = 0
        self.current_server = 1 - self.current_server
        self.reset_ball(start_right=(self.current_server==1))

    def draw(self):
        # draw paddles & ball
        for p in self.paddles:
            p.draw(self.screen)
        self.ball.draw(self.screen)

        # draw current game points
        left_name  = self.names[0]
        right_name = self.names[1]
        draw_text(self.screen,
                  str(self.points[left_name]),
                  (self.w * 0.25, 50),
                  self.font)
        draw_text(self.screen,
                  str(self.points[right_name]),
                  (self.w * 0.75, 50),
                  self.font)

    def current_score_str(self):
        return f"{self.names[0]} {self.points[self.names[0]]}  –  {self.names[1]} {self.points[self.names[1]]}"

    def match_winner(self):
        needed = self.settings['games_per_match']
        for name, wins in self.game_wins.items():
            if wins >= needed:
                return name
        return None

    def match_scores(self):
        return (self.game_wins[self.names[0]], self.game_wins[self.names[1]])
