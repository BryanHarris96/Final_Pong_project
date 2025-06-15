# main.py

import os
import json
import pygame
import logging

from constants         import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS,
    SETTINGS_FILE, FONT_PATH, FONT_TITLE_SIZE, FONT_HUD_SIZE
)
from utils             import get_font, draw_text
from menu              import MainMenu
from inputbox          import InputBox
from game              import Game
from leaderboard       import Leaderboard
from win_screen        import WinScreen
from pause_menu        import PauseMenu
from settings_screen   import SettingsScreen
from states            import GameState
from transition_screen import TransitionScreen

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s: %(message)s"
)

def draw_hud(
    surface: pygame.Surface,
    font: pygame.font.Font,
    game: Game,
    player_names: list[str],
    settings: dict,
    current_match: int,
    games_won: dict[str,int],
    series_wins: dict[str,int],
) -> None:
    """
    Draw the HUD with three lines:
     1) Match X/Y
     2) Games won this match
     3) Series wins tally
    """
    cx = SCREEN_WIDTH // 2

    # Line 1: match counter
    draw_text(surface,
              f"Match {current_match}/{settings['num_matches']}",
              (cx, 20),
              font)

    # Line 2: games-won within this match
    p1, p2   = player_names
    gw1, gw2 = games_won[p1], games_won[p2]
    best_of  = settings["games_per_match"]
    draw_text(surface,
              f"{p1}: {gw1} — {p2}: {gw2}   (best of {best_of})",
              (cx, 50),
              font)

    # Line 3: series-wins tally
    sw1, sw2 = series_wins.get(p1, 0), series_wins.get(p2, 0)
    draw_text(surface,
              f"{p1} series-wins: {sw1}    {p2} series-wins: {sw2}",
              (cx, 80),
              font)


def main() -> None:
    """Initialize Pygame and run the main state machine."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pong Tournament")
    clock = pygame.time.Clock()

    # Load persisted settings (JSON)
    saved_settings: dict = {}
    if os.path.isfile(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, 'r') as f:
                saved_settings = json.load(f)
        except Exception:
            logging.exception("Could not load settings.json")

    # Fonts
    title_font = get_font(FONT_TITLE_SIZE, FONT_PATH)
    hud_font   = get_font(FONT_HUD_SIZE, FONT_PATH)

    # Screens & Menus
    main_menu     = MainMenu(screen, title_font)
    leaderboard   = Leaderboard(screen, hud_font)
    pause_menu    = PauseMenu(screen, title_font)
    settings_view = SettingsScreen(
        screen,
        title_font,
        initial_settings=saved_settings or None
    )

    # InputBoxes
    name1_box = InputBox((250, 200, 300, 50), title_font)
    name2_box = InputBox((250, 260, 300, 50), title_font)
    serve_box = InputBox((250, 300, 300, 50), title_font)

    # State variables
    player_names: list[str]     = []
    tournament_settings: dict   = {}
    series_wins: dict[str,int]  = {}
    games_won: dict[str,int]    = {}
    current_match: int          = 0
    game: Game|None             = None
    win_screen: WinScreen|None  = None
    transition: TransitionScreen|None = None

    state = GameState.MENU

    while True:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            # Pause toggle
            if state == GameState.PLAYING and event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                state = GameState.PAUSED

            # Dispatch by current state
            if state == GameState.MENU:
                choice = main_menu.handle_event(event)
                if choice == "start":
                    player_names.clear()
                    tournament_settings.clear()
                    state = GameState.ENTER_NAME1
                elif choice == "settings":
                    settings_view = SettingsScreen(
                        screen,
                        title_font,
                        initial_settings=tournament_settings or saved_settings or None
                    )
                    state = GameState.SETTINGS
                elif choice == "leaderboard":
                    state = GameState.LEADERBOARD

            elif state == GameState.ENTER_NAME1:
                name = name1_box.handle_event(event)
                if name:
                    player_names.append(name)
                    state = GameState.ENTER_NAME2

            elif state == GameState.ENTER_NAME2:
                name = name2_box.handle_event(event)
                if name:
                    player_names.append(name)
                    settings_view = SettingsScreen(
                        screen,
                        title_font,
                        initial_settings=tournament_settings or saved_settings or None
                    )
                    state = GameState.SETTINGS

            elif state == GameState.SETTINGS:
                result = settings_view.handle_event(event)
                if result == "BACK":
                    # return to main menu if names not set
                    state = GameState.MENU if len(player_names) < 2 else GameState.CHOOSE_SERVER
                elif isinstance(result, dict):
                    tournament_settings = result
                    # save to disk
                    try:
                        with open(SETTINGS_FILE, 'w') as f:
                            json.dump(result, f, indent=2)
                    except Exception:
                        logging.exception("Failed to save settings.json")
                    state = GameState.CHOOSE_SERVER

            elif state == GameState.LEADERBOARD:
                if leaderboard.handle_event(event) == "BACK":
                    state = GameState.MENU

            elif state == GameState.CHOOSE_SERVER:
                if len(player_names) < 2:
                    state = GameState.MENU
                else:
                    val = serve_box.handle_event(event)
                    if val in ("1", "2"):
                        starter = int(val) - 1
                        current_match += 1
                        # reset per-match trackers
                        games_won   = {n: 0 for n in player_names}
                        series_wins = series_wins or {n: 0 for n in player_names}
                        game = Game(
                            screen,
                            player_names,
                            tournament_settings,
                            first_player=starter
                        )
                        state = GameState.PLAYING

            elif state == GameState.PLAYING:
                # leave logic to per-frame update below
                pass

            elif state == GameState.PAUSED:
                action = pause_menu.handle_event(event)
                if action == "resume":
                    state = GameState.PLAYING
                elif action == "settings":
                    settings_view = SettingsScreen(
                        screen,
                        title_font,
                        initial_settings=tournament_settings
                    )
                    state = GameState.SETTINGS
                elif action == "main_menu":
                    state = GameState.MENU
                elif action == "quit":
                    pygame.quit()
                    return

            elif state == GameState.MATCH_END:
                if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                    if current_match < tournament_settings["num_matches"]:
                        transition = TransitionScreen(
                            screen,
                            "Next Match",
                            f"Match {current_match+1}/{tournament_settings['num_matches']}",
                            title_font, hud_font
                        )
                        state = GameState.TRANSITION
                    else:
                        winner = max(series_wins, key=series_wins.get)
                        text = f"{winner} wins series {series_wins[winner]}"
                        win_screen = WinScreen(screen, title_font, text)
                        state = GameState.SERIES_END

            elif state == GameState.TRANSITION:
                # no event-based transitions here
                pass

            elif state == GameState.SERIES_END:
                if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                    state = GameState.MENU

        # Per-frame update & draw
        screen.fill((0, 0, 0))

        if state == GameState.MENU:
            main_menu.draw()

        elif state == GameState.ENTER_NAME1:
            draw_text(screen, "Player 1 Name:", (SCREEN_WIDTH//2, 170), title_font)
            name1_box.draw(screen)

        elif state == GameState.ENTER_NAME2:
            draw_text(screen, "Player 2 Name:", (SCREEN_WIDTH//2, 230), title_font)
            name2_box.draw(screen)

        elif state == GameState.SETTINGS:
            settings_view.draw()

        elif state == GameState.LEADERBOARD:
            leaderboard.draw()

        elif state == GameState.CHOOSE_SERVER:
            draw_text(
                screen,
                f"Who serves first? 1={player_names[0]}  2={player_names[1]}",
                (SCREEN_WIDTH//2, 260),
                title_font
            )
            serve_box.draw(screen)

        elif state == GameState.PLAYING:
            # 1) update positions and detect point wins
            point_winner = game.update()

            # 2) if a player won the game (points_to_win)
            if point_winner:
                games_won[point_winner] += 1
                threshold = (tournament_settings["games_per_match"] // 2) + 1
                # match-win?
                if games_won[point_winner] >= threshold:
                    winner = point_winner
                    series_wins[winner] += 1
                    win_screen = WinScreen(
                        screen,
                        title_font,
                        f"{winner} wins match {current_match}",
                        prompt="Press any key to continue"
                    )
                    leaderboard.record(
                        player_names,
                        (games_won[player_names[0]], games_won[player_names[1]])
                    )
                    state = GameState.MATCH_END
                else:
                    # reset for next game in same match
                    game.prepare_next_round()

            # draw game and HUD
            game.draw()
            draw_hud(
                screen,
                hud_font,
                game,
                player_names,
                tournament_settings,
                current_match,
                games_won,
                series_wins
            )

        elif state == GameState.PAUSED:
            game.draw()
            draw_hud(
                screen,
                hud_font,
                game,
                player_names,
                tournament_settings,
                current_match,
                games_won,
                series_wins
            )
            pause_menu.draw()

        elif state == GameState.MATCH_END:
            win_screen.draw()

        elif state == GameState.TRANSITION:
            transition.draw()
            if transition.tick():
                state = GameState.CHOOSE_SERVER

        elif state == GameState.SERIES_END:
            win_screen.draw()

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
