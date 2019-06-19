import string
from ..constants import EN_PUNCTUATION_RANGES
from .common import is_empty, is_char_in_range


def is_char_consonant(char: str = "", include_y: bool = True) -> bool:
    """Tests if a character is an English consonant.
    Extra parameter `include_y` determines if y is treated as a consonant."""
    if is_empty(char):
        return False
    consonants = set(string.ascii_lowercase) - {"a", "i", "u", "e", "o"}
    if not include_y:
        consonants -= {"y"}
    return char[0].lower() in consonants


def is_char_english_punctuation(char: str = "") -> bool:
    """Tests if a character is considered English punctuation."""
    return any(
        is_char_in_range(char, start, end) for start, end in EN_PUNCTUATION_RANGES
    )


def is_char_uppercase(char: str = "") -> bool:
    """Tests if a character is uppercase English"""
    if is_empty(char):
        return False
    return char[0] in string.ascii_uppercase


def is_char_vowel(char: str = "", include_y=False):
    if is_empty(char):
        return False
    vowels = {"a", "i", "u", "e", "o"} + ({"y"} if include_y else set())
    return char[0].lower() in vowels

