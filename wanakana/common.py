from typing import Iterable, Union, List
from collections import deque
import re
from .utils import (
    is_empty,
    is_char_hiragana,
    is_char_katakana,
    is_char_japanese,
    is_char_kana,
    is_char_kanji,
    is_char_romaji,
    is_char_english_punctuation,
    is_char_japanese_punctuation,
)


def is_hiragana(input: str = "") -> bool:
    """Tests if `input` is Hiragana"""
    return (not is_empty(input)) and all(is_char_hiragana(char) for char in input)


def is_katakana(input: str = "") -> bool:
    """Tests if `input` is Katakana"""
    return (not is_empty(input)) and all(is_char_katakana(char) for char in input)


def is_japanese(input: str = "", augmented: Iterable = None) -> bool:
    """Tests if `input` includes only Kanji, Kana, zenkaku numbers, and
    JA punctuation/symbols"""
    return (not is_empty(input)) and all(
        is_char_japanese(char) or (augmented and char in augmented) for char in input
    )


def is_kana(input: str = "") -> bool:
    """Tests if `input` is Kana (Katakana and/or Hiragana)"""
    return (not is_empty(input)) and all(is_char_kana(char) for char in input)


def is_kanji(input: str = "") -> bool:
    """Tests if `input` is Kanji (Japanese CJK Ideographs)"""
    return (not is_empty(input)) and all(is_char_kanji(char) for char in input)


def is_mixed(input: str = "", ignore_kanji: bool = True) -> bool:
    """Tests if `input` contains a mix of Romaji *and* Kana, ignoring Kanji by default"""
    return (
        (not is_empty(input))
        and any(is_char_kana(char) for char in input)
        and any(is_char_romaji(char) for char in input)
        and (ignore_kanji or not any(is_char_kanji(char) for char in input))
    )


def is_romaji(input: str = "", augmented: Iterable = None) -> bool:
    """Tests if `input` includes only Romaji characters (allowing Hepburn romanisation)"""
    return (not is_empty(input)) and all(
        is_char_romaji(char) or (augmented and char in augmented) for char in input
    )


is_char_en_space = lambda x: x == " "
is_char_ja_space = lambda x: x == "　"
is_char_en_num = lambda x: re.match(r"[0-9]", x)
is_char_ja_num = lambda x: re.match(r"[０-９]", x)

TOKEN_TYPES = {
    "EN": "en",
    "JA": "ja",
    "EN_NUM": "english_numeral",
    "JA_NUM": "japanese_numeral",
    "EN_PUNC": "english_punctuation",
    "JA_PUNC": "japanese_punctuation",
    "KANJI": "kanji",
    "HIRAGANA": "hiragana",
    "KATAKANA": "katakana",
    "SPACE": "space",
    "OTHER": "other",
}


def get_type(input: str, compact: bool = False) -> str:
    EN = "en"
    JA = "ja"
    EN_NUM = "english_numeral"
    JA_NUM = "japanese_numeral"
    EN_PUNC = "english_punctuation"
    JA_PUNC = "japanese_punctuation"
    KANJI = "kanji"
    HIRAGANA = "hiragana"
    KATAKANA = "katakana"
    SPACE = "space"
    OTHER = "other"
    if compact:
        if is_char_ja_num(input) or is_char_en_num(input):
            return OTHER
        if is_char_en_space(input):
            return EN
        if is_char_english_punctuation(input):
            return OTHER
        if is_char_ja_space(input):
            return JA
        if is_char_japanese_punctuation(input):
            return OTHER
        if is_char_japanese(input):
            return JA
        if is_char_romaji(input):
            return EN
        return OTHER
    else:
        if is_char_ja_num(input):
            return JA_NUM
        if is_char_en_num(input):
            return EN_NUM
        if is_char_en_space(input):
            return SPACE
        if is_char_english_punctuation(input):
            return EN_PUNC
        if is_char_ja_space(input):
            return SPACE
        if is_char_japanese_punctuation(input):
            return JA_PUNC
        if is_char_kanji(input):
            return KANJI
        if is_char_hiragana(input):
            return HIRAGANA
        if is_char_katakana(input):
            return KATAKANA
        if is_char_japanese(input):
            return JA
        if is_char_romaji(input):
            return EN
        return OTHER


def tokenise(
    input: str, compact: bool = False, detailed: bool = False
) -> Union[List[str], List[List[str]]]:
    """Splits input into list of strings separated by opinionated token types
    `'en', 'ja', 'english_numeral', 'japanese_numeral', 'english_punctuation',
    'japanese_punctuation', 'kanji', 'hiragana', 'katakana', 'space', 'other'`
    If `compact` is set then many same-language tokens are combined (spaces + text,
    kanji + kana, numeral + punctuation)
    If `detailed` is set then returned list will contain `[type, value]` instead of
    `value`"""
    if is_empty(input):
        return []
    chars = deque(input)
    initial = chars.popleft()
    prev_type = get_type(initial, compact)
    initial = [prev_type, initial] if detailed else initial

    tokens = [initial]
    for char in chars:
        curr_type = get_type(char, compact)
        same_type = curr_type == prev_type
        prev_type = curr_type
        new_value = char

        if same_type:
            new_value = tokens.pop()[1] if detailed else tokens.pop() + new_value

        tokens.append([curr_type, new_value] if detailed else new_value)
    return tokens
