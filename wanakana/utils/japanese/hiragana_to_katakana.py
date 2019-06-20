from ...constants import KATAKANA_START, HIRAGANA_START
from .common import is_char_long_dash, is_char_slash_dot, is_char_hiragana


def hiragana_to_katakana(input: str) -> str:
    kata = []
    for char in input:
        # Short circuit to avoid incorrect codeshift for 'ー' and '・'
        if is_char_slash_dot(char) or is_char_long_dash(char):
            kata.append(char)
        elif (not is_char_long_dash(char)) and is_char_hiragana(char):
            # Shift char code
            code = ord(char[0]) + (KATAKANA_START - HIRAGANA_START)
            kata_char = chr(code)
            kata.append(kata_char)
        else:
            kata.append(char)

    return "".join(kata)

