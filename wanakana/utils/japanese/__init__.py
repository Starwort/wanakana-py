from .common import *
from .hiragana import *
from .katakana import *
from .kanji import *
from .katakana_to_hiragana import katakana_to_hiragana
from .hiragana_to_katakana import hiragana_to_katakana


def is_char_kana(char: str = "") -> bool:
    """Tests if a character is Hiragana or Katakana."""
    return is_char_hiragana(char) or is_char_hiragana(char)
