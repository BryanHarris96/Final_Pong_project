# tests/test_core.py

import pygame
import pytest

from constants       import SCREEN_WIDTH, SCREEN_HEIGHT
from utils           import get_font
from game            import Game, Paddle, Ball
from inputbox        import InputBox
from menu            import Menu
from pause_menu      import PauseMenu
from settings_screen import SettingsScreen
from leaderboard     import Leaderboard
from win_screen      import WinScreen

@pytest.fixture(scope="module", autouse=True)
def init_pygame():
    pygame.init()
    yield
    pygame.quit()

def test_font_cache():
    f1 = get_font(20)
    f2 = get_font(20)
    assert f1 is f2

def test_paddle_sprite():
    p = Paddle(0,0,10,10,5,pygame.K_w,pygame.K_s)
    assert isinstance(p.image, pygame.Surface)
    assert hasattr(p, "rect")

def test_ball_sprite():
    b = Ball(100,100,8,4,4)
    assert isinstance(b.image, pygame.Surface)
    assert b.rect.center == (100, 100)

def test_game_init():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    g = Game(screen, ["A","B"], {"points_to_win":1, "games_per_match":1}, first_player=0)
    assert hasattr(g, "all_sprites")
    assert len(g.paddles) == 2
    assert len(g.ball_grp) == 1

def test_inputbox():
    font = get_font(20)
    ib = InputBox((0,0,100,30), font)
    assert hasattr(ib, "rect")

def test_menu():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    m = Menu(screen, get_font(20))
    # simulate a key event
    evt = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)
    # no error on handle_event
    m.handle_event(evt)

def test_pause_menu():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pm = PauseMenu(screen, get_font(20))
    # simulate a click at 0,0 shouldn't error
    evt = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(0,0), button=1)
    assert pm.handle_event(evt) in (None, 'resume', 'settings', 'main_menu', 'quit')

def test_settings_screen():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    ss = SettingsScreen(screen, get_font(20))
    # simulate clicking confirm without changes
    evt = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=ss.confirm.center, button=1)
    res = ss.handle_event(evt)
    assert isinstance(res, dict) or res == 'BACK'

def test_leaderboard():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    lb = Leaderboard(screen, get_font(20))
    evt = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(0,0), button=1)
    assert lb.handle_event(evt) in (None, 'BACK')

def test_win_screen():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    ws = WinScreen(screen, get_font(20), "Player")
    # just ensure draw() runs
    ws.draw()
