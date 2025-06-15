from enum import Enum, auto

class GameState(Enum):
    """
    All possible application states.
    """
    MENU           = auto()
    ENTER_NAME1    = auto()
    ENTER_NAME2    = auto()
    SETTINGS       = auto()
    LEADERBOARD    = auto()
    CHOOSE_SERVER  = auto()
    PLAYING        = auto()
    PAUSED         = auto()
    MATCH_END      = auto()
    TRANSITION     = auto()
    SERIES_END     = auto()
