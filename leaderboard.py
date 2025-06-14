# leaderboard.py
import pygame
import json
import os
import csv
from datetime import datetime
from utils import draw_text

JSON_FILE = 'leaderboard.json'
CSV_FILE  = 'leaderboard.csv'

class Leaderboard:
    def __init__(self, screen, filepath=JSON_FILE, max_display=10):
        self.screen      = screen
        self.w, self.h   = screen.get_size()
        self.filepath    = filepath
        self.max_display = max_display
        self.font        = pygame.font.Font(None, 36)
        self.title_font  = pygame.font.Font(None, 48)
        self.back        = pygame.Rect(20, 20, 100, 40)

        # Load & migrate entries
        self.entries = self._load_entries()
        if self._migrate_entries():
            # If any changes, save JSON and rewrite CSV
            self._save_entries()
            self._rewrite_csv()

    def _load_entries(self):
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        return data
            except Exception:
                pass
        return []

    def _save_entries(self):
        try:
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump(self.entries, f, indent=2)
        except Exception as e:
            print("Error saving leaderboard:", e)

    def _migrate_entries(self):
        """
        Convert any entry with old 'score': 'X-Y' field into
        'winner_games': X and 'loser_games': Y, removing 'score'.
        Returns True if any migration occurred.
        """
        migrated = False
        for e in self.entries:
            # Old format: has 'score' but not 'winner_games'
            if 'score' in e and 'winner_games' not in e:
                try:
                    x, y = e['score'].split('-', 1)
                    wg, lg = int(x), int(y)
                    # Determine which name is winner vs loser
                    # Compare wg/lg
                    e['winner_games'] = wg
                    e['loser_games']  = lg
                    # Remove old field
                    del e['score']
                    migrated = True
                except Exception:
                    # Malformed score? skip migration for this entry
                    continue
        return migrated

    def _rewrite_csv(self):
        """
        Rewrite the CSV_FILE entirely based on self.entries.
        """
        header = ['when', 'player', 'matches_won', 'matches_lost', 'games_won', 'games_lost']
        rows = []
        for e in self.entries:
            # skip entries lacking winner/loser fields
            if not all(k in e for k in ('winner','loser','winner_games','loser_games')):
                continue
            when = e.get('when', '')
            w = e['winner']; l = e['loser']
            wg = e['winner_games']; lg = e['loser_games']
            # winner row
            rows.append([when, w, 1, 0, wg, lg])
            # loser row
            rows.append([when, l, 0, 1, lg, wg])
        try:
            with open(CSV_FILE, 'w', newline='', encoding='utf-8') as cf:
                writer = csv.writer(cf)
                writer.writerow(header)
                writer.writerows(rows)
        except Exception as e:
            print("Error rewriting CSV:", e)

    def record(self, player_names, match_scores):
        """
        Add a completed match to the leaderboard (JSON + CSV append).
        player_names: [p1, p2]
        match_scores: (s1, s2)
        """
        p1, p2 = player_names
        s1, s2 = match_scores
        if s1 > s2:
            winner, loser = p1, p2
            wg, lg = s1, s2
        else:
            winner, loser = p2, p1
            wg, lg = s2, s1

        entry = {
            'when'         : datetime.now().strftime("%Y-%m-%d %H:%M"),
            'winner'       : winner,
            'loser'        : loser,
            'winner_games' : wg,
            'loser_games'  : lg
        }
        # Prepend to JSON entries
        self.entries.insert(0, entry)
        # Cap at 100 entries
        self.entries = self.entries[:100]
        # Save JSON
        self._save_entries()

        # Append to CSV
        header = ['when', 'player', 'matches_won', 'matches_lost', 'games_won', 'games_lost']
        rows = [
            [entry['when'], winner, 1, 0, wg, lg],
            [entry['when'], loser,  0, 1, lg, wg]
        ]
        file_exists = os.path.isfile(CSV_FILE)
        try:
            with open(CSV_FILE, 'a', newline='', encoding='utf-8') as cf:
                writer = csv.writer(cf)
                if not file_exists:
                    writer.writerow(header)
                writer.writerows(rows)
        except Exception as e:
            print("Error appending to CSV:", e)

    def draw(self):
        overlay = pygame.Surface((self.w, self.h))
        overlay.set_alpha(200)
        overlay.fill((0,0,0))
        self.screen.blit(overlay, (0,0))

        draw_text(self.screen, "Leaderboard", (self.w//2, 50), self.title_font)

        # Column headers
        headers = ["When","Winner","Score","Loser"]
        xs = [100, 300, 500, 650]
        for i,hdr in enumerate(headers):
            draw_text(self.screen, hdr, (xs[i],100), self.font)

        # Entries
        y0 = 140
        spacing = 40
        for idx, e in enumerate(self.entries[:self.max_display]):
            y = y0 + idx*spacing
            when = e.get('when','')
            winner = e.get('winner','')
            loser  = e.get('loser','')
            if 'winner_games' in e and 'loser_games' in e:
                score = f"{e['winner_games']}-{e['loser_games']}"
            else:
                score = ''
            draw_text(self.screen, when,   (xs[0], y), self.font)
            draw_text(self.screen, winner, (xs[1], y), self.font)
            draw_text(self.screen, score,  (xs[2], y), self.font)
            draw_text(self.screen, loser,  (xs[3], y), self.font)

        # Back button
        pygame.draw.rect(self.screen, (255,255,255), self.back, 2)
        draw_text(self.screen, "Back", self.back.center, self.font)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.back.collidepoint(event.pos):
                return 'BACK'
        return None
