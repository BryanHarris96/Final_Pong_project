# main.py
import pygame
import json
import os

from menu            import Menu
from inputbox        import InputBox
from utils           import draw_text
from game            import Game
from leaderboard     import Leaderboard
from win_screen      import WinScreen
from pause_menu      import PauseMenu
from settings_screen import SettingsScreen, SETTINGS_FILE

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Pygame Pong")
    clock = pygame.time.Clock()

    # Load persisted settings
    persisted = None
    if os.path.isfile(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, 'r') as f:
                persisted = json.load(f)
        except:
            persisted = None

    # UI modules
    menu        = Menu(screen)
    leaderboard = Leaderboard(screen)
    pause_menu  = PauseMenu(screen, pygame.font.Font(None,50))
    font_hud    = pygame.font.Font(None,26)  # increased by 2
    font_title  = pygame.font.Font(None,50)  # increased by 2

    # Name entry
    name1_box = InputBox((250,200,300,50), font_title)
    name2_box = InputBox((250,260,300,50), font_title)
    names     = []

    # Serve choice
    choose_box = InputBox((250,300,300,50), font_title)

    # Placeholders
    settings        = {}
    settings_screen = None
    game            = None
    win_screen      = None

    # State & counters
    state       = 'menu'
    match_count = 0
    game_count  = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Pause
            elif state=='playing' and event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE:
                state='paused'
                continue

            # State events
            if state=='menu':
                c = menu.handle_event(event)
                if c=='start':
                    names.clear(); settings.clear()
                    state='name1'
                elif c=='settings':
                    settings_screen = SettingsScreen(screen,font_title,initial_settings=persisted)
                    state='settings'
                elif c=='leader':
                    state='leaderboard'

            elif state=='name1':
                v = name1_box.handle_event(event)
                if v:
                    names.append(v); state='name2'

            elif state=='name2':
                v = name2_box.handle_event(event)
                if v:
                    names.append(v)
                    settings_screen = SettingsScreen(screen,font_title,initial_settings=persisted)
                    state='settings'

            elif state=='settings':
                res = settings_screen.handle_event(event)
                if res=='BACK':
                    state='menu'
                elif isinstance(res,dict):
                    settings=res
                    state='choose_start' if len(names)==2 else 'menu'

            elif state=='leaderboard':
                if leaderboard.handle_event(event)=='BACK':
                    state='menu'

            elif state=='choose_start':
                v = choose_box.handle_event(event)
                if v in ('1','2'):
                    first=int(v)-1
                    match_count += 1
                    game_count  = 1
                    game = Game(screen,names,settings,first_player=first)
                    state='playing'

            elif state=='paused':
                a = pause_menu.handle_event(event)
                if a=='resume': state='playing'
                elif a=='settings':
                    settings_screen=SettingsScreen(screen,font_title,initial_settings=settings)
                    state='settings'
                elif a=='main_menu': state='menu'
                elif a=='quit': running=False

            elif state=='playing':
                pass

            elif state=='round_end':
                if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                    if game.match_winner():
                        win_screen = WinScreen(screen, game.match_winner())
                        state='match_end'
                    else:
                        game.prepare_next_round()
                        game_count += 1
                        state='playing'

            elif state=='match_end':
                if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                    leaderboard.record(names, game.match_scores())
                    state='menu'

        # DRAW
        screen.fill((0,0,0))

        if state=='menu':
            menu.draw()

        elif state=='name1':
            draw_text(screen,"Enter Player 1 Name:",(400,170),font_title)
            name1_box.draw(screen)

        elif state=='name2':
            draw_text(screen,"Enter Player 2 Name:",(400,230),font_title)
            name2_box.draw(screen)

        elif state=='settings':
            settings_screen.draw()

        elif state=='leaderboard':
            leaderboard.draw()

        elif state=='choose_start':
            if len(names)>=2:
                draw_text(screen,f"Serve: 1={names[0]}  2={names[1]}",(400,260),font_title)
                choose_box.draw(screen)
            else:
                state='menu'

        elif state=='paused':
            if game: game.draw()
            pause_menu.draw()

        elif state=='playing':
            gw = game.update()
            if gw:
                if game.match_winner():
                    win_screen = WinScreen(screen, game.match_winner())
                    state='match_end'
                else:
                    state='round_end'
            game.draw()

            # HUD — all centered
            # Match count
            draw_text(screen, f"Match {match_count}/{settings.get('num_matches','?')}",
                      (400, 20), font_hud)
            # Game count
            total_games = settings.get('games_per_match',1)
            gc = min(game_count, total_games)
            draw_text(screen, f"Game {gc}/{total_games}",
                      (400, 50), font_hud)
            # Current score
            draw_text(screen, game.current_score_str(),
                      (400, 80), font_hud)
            # Match-wins combined
            ln, rn = names[0], names[1]
            lw, rw = game.game_wins[ln], game.game_wins[rn]
            draw_text(screen, f"{ln}: {lw}    {rn}: {rw}",
                      (400, 110), font_hud)

        elif state=='round_end':
            draw_text(screen,f"Game Over: {game.current_score_str()}",
                      (400,250),font_title)
            draw_text(screen,"Press any key to continue",
                      (400,300),font_title)

        elif state=='match_end':
            win_screen.draw()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__=="__main__":
    try: main()
    except:
        import traceback; traceback.print_exc()
        input("Error encountered. Press Enter to exit.")
