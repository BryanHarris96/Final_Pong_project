import os
import json
import csv
import pygame
from datetime import datetime

from constants import (
    LEADER_JSON, LEADER_CSV,
    SCREEN_WIDTH, SCREEN_HEIGHT,
    COLOR_FG, FONT_PATH, FONT_TITLE_SIZE
)
from utils     import get_font, draw_text

class Leaderboard:
    """
    Aggregates all historical match results, displays:
     - Total matches won per player (all time)
     - Recent-match table
    Also persists to JSON + CSV.
    """
    def __init__(self, screen: pygame.Surface, font: pygame.font.Font, max_items:int=10):
        self.screen      = screen
        self.font        = font
        self.title_font  = get_font(FONT_TITLE_SIZE)
        self.max_items   = max_items
        self.back_button = pygame.Rect(20,20,100,40)

        # Load or initialize
        self.entries = self._load_json()
        if self._migrate_old_format():
            self._save_json(); self._write_csv()

    def _load_json(self) -> list[dict]:
        if os.path.isfile(LEADER_JSON):
            try:
                return json.load(open(LEADER_JSON))
            except Exception:
                pass
        return []

    def _save_json(self) -> None:
        json.dump(self.entries, open(LEADER_JSON,"w"), indent=2)

    def _migrate_old_format(self) -> bool:
        """
        If old entries used 'score' instead of 'winner_games'/'loser_games',
        split them out into the new keys.
        """
        migrated = False
        for e in self.entries:
            if "score" in e and "winner_games" not in e:
                try:
                    x,y = map(int, e["score"].split("-"))
                    e["winner_games"], e["loser_games"] = x,y
                    del e["score"]
                    migrated = True
                except Exception:
                    pass
        return migrated

    def _write_csv(self) -> None:
        """Rewrite the CSV from scratch, including header."""
        with open(LEADER_CSV, "w", newline="") as fout:
            writer = csv.writer(fout)
            writer.writerow(["when","player","matches_won","matches_lost","games_won","games_lost"])
            for e in self.entries:
                w, l = e["winner"], e["loser"]
                wg, lg = e["winner_games"], e["loser_games"]
                # winner row
                writer.writerow([e["when"], w,1,0,wg,lg])
                # loser  row
                writer.writerow([e["when"], l,0,1,lg,wg])

    def record(self, names: list[str], scores: tuple[int,int]) -> None:
        """
        Append a new match result to JSON + CSV.
        `scores` is the (games_won_p1, games_won_p2).
        """
        p1,p2 = names
        s1,s2 = scores
        if s1 > s2:
            winner, loser, wg, lg = p1,p2,s1,s2
        else:
            winner, loser, wg, lg = p2,p1,s2,s1

        entry = {
            "when": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "winner": winner,
            "loser":  loser,
            "winner_games": wg,
            "loser_games":  lg
        }
        # Prepend and cap history
        self.entries.insert(0, entry)
        self.entries = self.entries[:100]
        self._save_json()

        # Append to CSV
        new_file = not os.path.isfile(LEADER_CSV)
        with open(LEADER_CSV,"a",newline="") as fout:
            writer = csv.writer(fout)
            if new_file:
                writer.writerow(["when","player","matches_won","matches_lost","games_won","games_lost"])
            writer.writerow([entry["when"], winner,1,0,wg,lg])
            writer.writerow([entry["when"], loser,0,1,lg,wg])

    def draw(self) -> None:
        """Overlay, show total wins, recent-table, and Back button."""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200); overlay.fill((0,0,0))
        self.screen.blit(overlay,(0,0))

        # Title
        draw_text(self.screen, "Leaderboard", (SCREEN_WIDTH//2,50), self.title_font)

        # Total matches won
        tally: dict[str,int] = {}
        for e in self.entries:
            tally[e["winner"]] = tally.get(e["winner"],0)+1
        y = 100
        draw_text(self.screen, "All-Time Matches Won", (SCREEN_WIDTH//2,y), self.font)
        y+=40
        for name,count in sorted(tally.items(),key=lambda x:-x[1])[:self.max_items]:
            draw_text(self.screen, f"{name}: {count}", (SCREEN_WIDTH//2,y), self.font)
            y+=30

        # Recent matches table
        cols = ["When","Winner","Score","Loser"]
        xs   = [100,300,500,650]
        header_y = y+20
        for i,heading in enumerate(cols):
            draw_text(self.screen, heading, (xs[i],header_y), self.font)
        for idx, e in enumerate(self.entries[:self.max_items]):
            row_y = header_y + (idx+1)*30
            score = f"{e['winner_games']}-{e['loser_games']}"
            draw_text(self.screen, e["when"], (xs[0],row_y), self.font)
            draw_text(self.screen, e["winner"], (xs[1],row_y), self.font)
            draw_text(self.screen, score,        (xs[2],row_y), self.font)
            draw_text(self.screen, e["loser"],  (xs[3],row_y), self.font)

        # Back button
        pygame.draw.rect(self.screen, COLOR_FG, self.back_button, 2)
        draw_text(self.screen, "Back", self.back_button.center, self.font)

    def handle_event(self, event: pygame.event.Event) -> str|None:
        """Return 'BACK' if the back-button was clicked."""
        if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
            if self.back_button.collidepoint(event.pos):
                return "BACK"
        return None
