from .common import *
from .english import *
from .japanese import *
from .kana_mapping import *
from .kana_to_romaji_map import *
from .romaji_to_kana_map import *


def is_char_punctuation(char: str = "") -> bool:
    """Tests if a character is considered Japanese or English punctuation"""
    return is_char_english_punctuation(char) or is_char_japanese_punctuation(char)
