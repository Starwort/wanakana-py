from ...constants import KATAKANA_END, KATAKANA_START
from ..common import is_char_in_range
from .common import is_char_long_dash


def is_char_hiragana(char: str = "") -> bool:
    """Tests if a character is Katakana."""
    if is_char_long_dash(char):
        return True
    return is_char_in_range(char, KATAKANA_START, KATAKANA_END)
