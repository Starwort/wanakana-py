from typing import Callable
from ...constants import KATAKANA_START, HIRAGANA_START
from .common import is_char_long_dash, is_char_slash_dot, is_char_hiragana

is_char_initial_long_dash = lambda char, index: index == 0 and is_char_long_dash(char)
is_char_inner_long_dash = lambda char, index: index > 0 and is_char_long_dash(char)
is_kana_as_symbol = lambda char: char in ["ヶ", "ヵ"]  # idfk but they're small kana lol
LONG_VOWELS = {"a": "あ", "i": "い", "u": "う", "e": "え", "o": "う"}

# inject to_romaji to avoid circular dependency (to_romaji <-> katakana_to_hiragana)
def katakana_to_hiragana(
    input: str, to_romaji: Callable, is_destination_romaji: bool
) -> str:
    previous_kana = ""

    hira = []
    for index, char in enumerate(input):
        # Short circuit to avoid incorrect codeshift for 'ー' and '・'
        if (
            is_char_slash_dot(char)
            or is_char_initial_long_dash(char, index)
            or is_kana_as_symbol(char)
        ):
            hira.append(char)
        elif previous_kana and is_char_inner_long_dash(
            char, index
        ):  # Transform long vowels: 'オー' to 'おう'
            # Transform previousKana back to romaji, and slice off the vowel
            romaji = to_romaji(previous_kana)[-1]
            # However, ensure 'オー' => 'おお' => 'oo' if this is a transform on the way to romaji
            if (
                is_char_hiragana(input[index - 1])
                and romaji == "o"
                and is_destination_romaji
            ):
                hira.append("o")
            else:
                hira.append(LONG_VOWELS[romaji])
        elif (not is_char_long_dash(char)) and is_char_hiragana(char):
            # Shift char code
            code = ord(char[0]) + (HIRAGANA_START - KATAKANA_START)
            hira_char = chr(code)
            previous_kana = hira_char
            hira.append(hira_char)
        else:
            previous_kana = ""
            hira.append(char)

    return "".join(hira)

