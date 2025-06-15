# game.py

import os
import pygame

from constants import SOUND_DIR, FONT_PATH
from utils     import draw_text

class Paddle(pygame.sprite.Sprite):
    """
    A single paddle controlled by up/down keys.
    """
    def __init__(
        self,
        x: int, y: int,
        width: int, height: int,
        speed: int,
        key_up: int, key_down: int
    ):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((255,255,255))
        self.rect  = self.image.get_rect(topleft=(x,y))
        self.speed = speed
        self.key_up   = key_up
        self.key_down = key_down

    def update(self, pressed_keys: pygame.key.ScancodeWrapper, screen_height: int) -> None:
        if pressed_keys[self.key_up] and self.rect.top > 0:
            self.rect.y -= self.speed
        if pressed_keys[self.key_down] and self.rect.bottom < screen_height:
            self.rect.y += self.speed


class Ball(pygame.sprite.Sprite):
    """
    The pong ball that bounces off walls & paddles.
    """
    def __init__(self, center_x: int, center_y: int, radius: int, speed_x: int, speed_y: int):
        super().__init__()
        diameter = radius * 2
        self.image = pygame.Surface((diameter, diameter), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255,255,255), (radius, radius), radius)
        self.rect = self.image.get_rect(center=(center_x, center_y))
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.game_ref: "Game"  # set by Game

    def update(self, paddles: pygame.sprite.Group, screen_w: int, screen_h: int) -> None:
        # Move
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Bounce off top/bottom
        if self.rect.top <= 0 or self.rect.bottom >= screen_h:
            self.speed_y *= -1
            self.game_ref.snd_bounce.play()

        # Bounce off any paddle
        if pygame.sprite.spritecollideany(self, paddles):
            self.speed_x *= -1
            self.game_ref.snd_bounce.play()


class Game:
    """
    The core Pong game: handles sprites, input, scoring, and sound.
    """
    def __init__(
        self,
        surface: pygame.Surface,
        player_names: list[str],
        settings: dict,
        first_player: int = 0
    ):
        # Initialize mixer & sounds
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        self.snd_bounce = pygame.mixer.Sound(os.path.join(SOUND_DIR, "bounce.mp3"))
        self.snd_score  = pygame.mixer.Sound(os.path.join(SOUND_DIR, "score.wav"))

        self.surface = surface
        self.width, self.height = surface.get_size()
        self.player1, self.player2 = player_names[:2]
        self.settings = settings

        # Create paddles & ball
        paddle_h, paddle_w, paddle_speed = 100, 10, 5
        p1 = Paddle(10, (self.height-paddle_h)//2, paddle_w, paddle_h, paddle_speed, pygame.K_w, pygame.K_s)
        p2 = Paddle(self.width-20, (self.height-paddle_h)//2, paddle_w, paddle_h, paddle_speed, pygame.K_UP, pygame.K_DOWN)

        ball_speed = 4
        direction = 1 if first_player==1 else -1
        ball = Ball(
            self.width//2, self.height//2, 8,
            ball_speed*direction, ball_speed
        )
        ball.game_ref = self  # back-reference

        # Sprite groups
        self.paddles   = pygame.sprite.Group(p1, p2)
        self.ball_grp  = pygame.sprite.Group(ball)
        self.all_sprites = pygame.sprite.Group(p1, p2, ball)

        # Score trackers
        self.points    = {self.player1:0, self.player2:0}
        self.games_won = {self.player1:0, self.player2:0}

        self.current_server = first_player
        # Use FONT_PATH (may be None) or default system font
        self.font = pygame.font.Font(FONT_PATH, 48)

    def reset_ball(self, to_right: bool) -> None:
        """
        Center the ball and set its horizontal direction.
        """
        ball = next(iter(self.ball_grp))
        ball.rect.center = (self.width//2, self.height//2)
        ball.speed_x = abs(ball.speed_x) * (1 if to_right else -1)

    def update(self) -> str|None:
        """
        Advance one frame: move paddles, move ball, detect scoring.
        Returns the name of the player who just won the *game*
        (i.e. reached points_to_win), or None otherwise.
        """
        keys = pygame.key.get_pressed()
        for paddle in self.paddles:
            paddle.update(keys, self.height)
        ball = next(iter(self.ball_grp))
        ball.update(self.paddles, self.width, self.height)

        # Someone missed → point to the other
        if ball.rect.right < 0:
            scorer = self.player2
            self.points[scorer] += 1
            self.snd_score.play()
            self.reset_ball(to_right=True)
            return self._check_game_end(scorer)
        if ball.rect.left > self.width:
            scorer = self.player1
            self.points[scorer] += 1
            self.snd_score.play()
            self.reset_ball(to_right=False)
            return self._check_game_end(scorer)
        return None

    def _check_game_end(self, scorer: str) -> str|None:
        """
        If scorer has reached points_to_win, increment that player's
        games_won and return scorer. Otherwise return None.
        """
        if self.points[scorer] >= self.settings["points_to_win"]:
            self.games_won[scorer] += 1
            return scorer
        return None

    def prepare_next_round(self) -> None:
        """
        Zero out point scores and switch server for the next rally or game.
        """
        for name in self.points:
            self.points[name] = 0
        self.current_server = 1 - self.current_server
        self.reset_ball(to_right=(self.current_server==1))

    def draw(self) -> None:
        """
        Draw paddles, ball, and the two point scores at quarter widths.
        """
        self.all_sprites.draw(self.surface)
        draw_text(self.surface, str(self.points[self.player1]),  (self.width*0.25, 50), self.font)
        draw_text(self.surface, str(self.points[self.player2]),  (self.width*0.75, 50), self.font)
