import os

# ——— Window & Display Settings ———
# Size of the game window in pixels.
SCREEN_WIDTH: int  = 800
SCREEN_HEIGHT: int = 600
# How many frames to draw per second.
FPS: int           = 60

# ——— Color Definitions ———
# Background and foreground colors (RGB).
COLOR_BG:       tuple[int,int,int] = (0,   0,   0)
COLOR_FG:       tuple[int,int,int] = (255, 255, 255)
COLOR_INACTIVE: tuple[int,int,int] = (100, 100, 100)
COLOR_ACTIVE:   tuple[int,int,int] = (255, 255, 255)

# ——— Font Settings ———
# Path to a .ttf font file, or None for default system font.
FONT_PATH:        str|None = None
# Font sizes for titles and HUD text.
FONT_TITLE_SIZE:  int      = 50
FONT_HUD_SIZE:    int      = 26

# ——— Asset & Data File Paths ———
BASE_DIR:      str = os.path.dirname(__file__)
ASSET_DIR:     str = os.path.join(BASE_DIR, 'assets')
SOUND_DIR:     str = os.path.join(ASSET_DIR, 'sounds')
# Persistent settings for number of matches, etc.
SETTINGS_FILE: str = os.path.join(BASE_DIR, 'settings.json')
# Leaderboard data storage.
LEADER_JSON:   str = os.path.join(BASE_DIR, 'leaderboard.json')
LEADER_CSV:    str = os.path.join(BASE_DIR, 'leaderboard.csv')
