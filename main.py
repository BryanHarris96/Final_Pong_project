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
    Draw the three-line HUD:
     1) “Match X/Y”
     2) “Player1: n — Player2: m (best of Z)”
     3) “Player1 series-wins: a   Player2 series-wins: b”
    """
    cx = SCREEN_WIDTH // 2

    # 1) Match counter
    draw_text(
        surface,
        f"Match {current_match}/{settings['num_matches']}",
        (cx, 20),
        font
    )

    # 2) Games-won in this match
    p1, p2 = player_names
    won1, won2 = games_won[p1], games_won[p2]
    best_of = settings["games_per_match"]
    draw_text(
        surface,
        f"{p1}: {won1} — {p2}: {won2}   (best of {best_of})",
        (cx, 50),
        font
    )

    # 3) Series-wins tally
    series1, series2 = series_wins.get(p1,0), series_wins.get(p2,0)
    draw_text(
        surface,
        f"{p1} series-wins: {series1}    {p2} series-wins: {series2}",
        (cx, 80),
        font
    )


def main() -> None:
    """Entrypoint: initialize Pygame, run the main loop handling states."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pong Tournament")
    clock = pygame.time.Clock()

    # Load saved defaults (if any)
    saved_settings: dict = {}
    if os.path.isfile(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE) as f:
                saved_settings = json.load(f)
        except Exception:
            logging.exception("Failed loading settings.json")

    # Prepare fonts
    title_font = get_font(FONT_TITLE_SIZE)
    hud_font   = get_font(FONT_HUD_SIZE)

    # Instantiate all screens/menus
    main_menu     = MainMenu(screen, title_font)
    leaderboard   = Leaderboard(screen, hud_font)
    pause_menu    = PauseMenu(screen, title_font)
    settings_view = SettingsScreen(screen, title_font, initial=settings if (settings:=saved_settings) else None)

    # Input boxes for names & serve choice
    name1_box  = InputBox((250,200,300,50), title_font)
    name2_box  = InputBox((250,260,300,50), title_font)
    serve_box  = InputBox((250,300,300,50), title_font)

    # State variables
    player_names: list[str] = []
    tour_settings: dict    = {}
    series_wins: dict[str,int] = {}
    games_won:    dict[str,int] = {}
    current_match = 0
    game          = None
    win_screen    = None
    transition    = None

    state = GameState.MENU

    # -- Main loop --
    while True:
        # — Event handling —
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            # Global ESC → pause if playing
            if state == GameState.PLAYING and event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                state = GameState.PAUSED

            # Dispatch to the active state
            if state == GameState.MENU:
                choice = main_menu.handle_event(event)
                if choice == "start":
                    player_names.clear()
                    tour_settings.clear()
                    state = GameState.ENTER_NAME1
                elif choice == "settings":
                    settings_view.load_initial(saved_settings)
                    state = GameState.SETTINGS
                elif choice == "leader":
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
                    settings_view.load_initial(saved_settings)
                    state = GameState.SETTINGS

            elif state == GameState.SETTINGS:
                result = settings_view.handle_event(event)
                if result == "BACK":
                    state = GameState.MENU if len(player_names) < 2 else GameState.CHOOSE_SERVER
                elif isinstance(result, dict):
                    tour_settings = result
                    saved_settings = result
                    with open(SETTINGS_FILE,"w") as f:
                        json.dump(result,f,indent=2)
                    state = GameState.CHOOSE_SERVER

            elif state == GameState.LEADERBOARD:
                if leaderboard.handle_event(event) == "BACK":
                    state = GameState.MENU

            elif state == GameState.CHOOSE_SERVER:
                # ensure we have 2 names
                if len(player_names) < 2:
                    state = GameState.MENU
                else:
                    val = serve_box.handle_event(event)
                    if val in ("1","2"):
                        starter = int(val)-1
                        # reset match & game trackers
                        current_match += 1
                        games_won    = {n:0 for n in player_names}
                        series_wins  = series_wins or {n:0 for n in player_names}
                        # create game instance
                        game = Game(
                            screen, player_names,
                            tour_settings, starter
                        )
                        state = GameState.PLAYING

            elif state == GameState.PLAYING:
                # Intentionally empty: we update/draw per-frame below

                pass

            elif state == GameState.PAUSED:
                action = pause_menu.handle_event(event)
                if action == "resume":
                    state = GameState.PLAYING
                elif action == "settings":
                    settings_view.load_initial(tour_settings)
                    state = GameState.SETTINGS
                elif action == "main_menu":
                    state = GameState.MENU
                elif action == "quit":
                    pygame.quit()
                    return

            elif state == GameState.MATCH_END:
                if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                    if current_match < tour_settings["num_matches"]:
                        transition = TransitionScreen(
                            screen,
                            "Next Match",
                            f"Match {current_match+1}/{tour_settings['num_matches']}",
                            title_font, hud_font
                        )
                        state = GameState.TRANSITION
                    else:
                        winner = max(series_wins, key=series_wins.get)
                        text   = f"{winner} wins series {series_wins[winner]}"
                        win_screen = WinScreen(screen, title_font, text)
                        state = GameState.SERIES_END

            elif state == GameState.TRANSITION:
                # no event processing here

                pass

            elif state == GameState.SERIES_END:
                if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                    state = GameState.MENU

        # — Per-frame update & draw —
        screen.fill((0,0,0))

        if state == GameState.MENU:
            main_menu.draw()

        elif state == GameState.ENTER_NAME1:
            draw_text(screen, "Player 1 Name:", (SCREEN_WIDTH//2,170), title_font)
            name1_box.draw(screen)

        elif state == GameState.ENTER_NAME2:
            draw_text(screen, "Player 2 Name:", (SCREEN_WIDTH//2,230), title_font)
            name2_box.draw(screen)

        elif state == GameState.SETTINGS:
            settings_view.draw()

        elif state == GameState.LEADERBOARD:
            leaderboard.draw()

        elif state == GameState.CHOOSE_SERVER:
            draw_text(
                screen,
                f"Who serves first? 1={player_names[0]}  2={player_names[1]}",
                (SCREEN_WIDTH//2,260),
                title_font
            )
            serve_box.draw(screen)

        elif state == GameState.PLAYING:
            # 1) move paddles & ball, detect point winner
            point_winner = game.update()

            # 2) if someone scored the game-win
            if point_winner:
                games_won[point_winner] += 1

                # "best of N" means first to floor(N/2)+1
                threshold = tour_settings["games_per_match"]//2 + 1
                if games_won[point_winner] >= threshold:
                    # match is over
                    winner = point_winner
                    series_wins[winner] += 1
                    win_screen = WinScreen(
                        screen,
                        title_font,
                        f"{winner} wins match {current_match}",
                        prompt="Press any key to continue"
                    )
                    # record to persistent leaderboard
                    leaderboard.record(
                        player_names,
                        (games_won[player_names[0]], games_won[player_names[1]])
                    )
                    state = GameState.MATCH_END
                else:
                    # reset for next game in this match
                    game.prepare_next_round()

            # 3) draw game & HUD
            game.draw()
            draw_hud(
                screen, hud_font, game,
                player_names, tour_settings,
                current_match, games_won, series_wins
            )

        elif state == GameState.PAUSED:
            game.draw()
            draw_hud(
                screen, hud_font, game,
                player_names, tour_settings,
                current_match, games_won, series_wins
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
