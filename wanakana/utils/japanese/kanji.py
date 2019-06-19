from ...constants import KANJI_END, KANJI_START
from ..common import is_char_in_range


def is_char_kanji(char: str = "") -> bool:
    """Tests if a character is a CJK ideograph (kanji)."""
    return is_char_in_range(char, KANJI_START, KANJI_END)
