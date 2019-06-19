from ...constants import (
    PROLONGED_SOUND_MARK,
    KANA_SLASH_DOT,
    JAPANESE_RANGES,
    JA_PUNCTUATION_RANGES,
)
from ..common import is_empty, is_char_in_range
from .hiragana import is_char_hiragana
from .katakana import is_char_katakana


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


def is_char_kana(char: str = "") -> bool:
    """Tests if a character is Hiragana or Katakana."""
    return is_char_hiragana(char) or is_char_katakana(char)


def apply_mapping(string: str, mapping: dict, convert_ending: bool) -> str:
    root = mapping.copy()  # no idea if it's being mutated but they decided to copy it

    def assign(target: dict, source: dict) -> dict:
        if isinstance(source, dict):
            target.update(source)
        else:
            target.update({"0": source})
        return target

    def next_subtree(tree: dict, next_char: str):
        try:
            subtree = tree[next_char]
        except:
            return
        return assign({"": tree[""] + next_char}, subtree)

    def new_chunk(remaining, current_cursor):
        first_char = remaining[0]
        return parse(
            assign({"": first_char}, root[first_char]),
            remaining[1:],
            current_cursor,
            current_cursor + 1,
        )

    def parse(tree: dict, remaining, last_cursor, current_cursor):
        if not remaining:
            if convert_ending or len(tree.keys()) == 1:
                # nothing more to consume, just commit the last chunk and return it
                # so as not to have an empty element at the end of the result
                return [[last_cursor, current_cursor, tree[""]]] if tree[""] else []
            # if we don't want to convert the ending, because there are still possible
            # continuations, return None as the final node value
            return [[last_cursor, current_cursor, None]]

        if len(tree.keys()) == 1:
            return [[last_cursor, current_cursor, tree[""]]] + new_chunk(
                remaining, current_cursor
            )

        subtree = next_subtree(tree, remaining[0])

        if not subtree:
            return [[last_cursor, current_cursor, tree[""]]] + new_chunk(
                remaining, current_cursor
            )
        # continue current branch
        return parse(subtree, remaining[1:], last_cursor, current_cursor + 1)

    return new_chunk(string, 0)


# transform the tree, so that for example hepburn_tree['ゔ']['ぁ'][''] == 'va'
# or kana_tree['k']['y']['a'][''] == 'きゃ'
def transform(tree: dict):
    map = {}
    for char, subtree in tree.items():
        end_of_branch = isinstance(subtree, str)
        map[char] = {'': subtree} if end_of_branch else transform(subtree)
    return map

def get_subtree_of(tree, string):
    correct_subtree = tree
    for char in string:
        correct_subtree = correct_subtree.get(char, {})
    return correct_subtree