from ...constants import (
    PROLONGED_SOUND_MARK,
    KANA_SLASH_DOT,
    JAPANESE_RANGES,
    JA_PUNCTUATION_RANGES,
)
from ..common import is_empty, is_char_in_range


def is_char_long_dash(char: str = "") -> bool:
    if is_empty(char):
        return False
    return ord(char[0]) == PROLONGED_SOUND_MARK


def is_char_slash_dot(char: str = "") -> bool:
    if is_empty(char):
        return False
    return ord(char[0]) == KANA_SLASH_DOT


def is_char_japanese(char: str = "") -> bool:
    """Tests if a character is Japanese."""
    return any(is_char_in_range(char, start, end) for start, end in JAPANESE_RANGES)


def is_char_japanese_punctuation(char: str = "") -> bool:
    """Tests if a character is considered Japanese punctuation."""
    return any(
        is_char_in_range(char, start, end) for start, end in JA_PUNCTUATION_RANGES
    )
