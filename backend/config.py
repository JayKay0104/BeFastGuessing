# Global Variables
CORRECT_SONG_ID = None
GAME_START_TIME = None
DATE_FORMAT_STR = '%d/%m/%Y %H:%M:%S.%f'

GAME = {
    "Round_1": None,
    "Round_2": None,
    "Round_3": None,
    "Round_4": None,
    "Round_5": None,
    "Round_6": None,
    "Round_7": None,
    "Round_8": None,
    "Round_9": None,
    "Round_10": None,
}


def reset_game() -> None:
    GAME = {}
