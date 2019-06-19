from ...constants import HIRAGANA_END, HIRAGANA_START
from ..common import is_char_in_range
from .common import is_char_long_dash


def is_char_hiragana(char: str = "") -> bool:
    """Tests if a character is Hiragana."""
    if is_char_long_dash(char):
        return True
    return is_char_in_range(char, HIRAGANA_START, HIRAGANA_END)
