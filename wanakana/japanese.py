import re
from typing import List, Union, Tuple
from .common import (
    is_japanese,
    is_kana,
    is_katakana,
    is_kanji,
    tokenise,
    is_char_kana,
    is_char_kanji,
    is_mixed,
    is_romaji,
    is_char_english_punctuation,
)
from .constants import TO_KANA_METHODS, ROMANISATIONS
from .utils import (
    get_romaji_to_kana_tree,
    get_kana_to_romaji_tree,
    USE_OBSOLETE_KANA_MAP,
    apply_mapping,
    merge_custom_mapping,
    is_char_uppercase,
    hiragana_to_katakana,
    katakana_to_hiragana,
)

is_leading_without_initial_kana = lambda input, leading: leading and (
    not is_kana(input[0])
)
is_trailing_without_final_kana = lambda input, leading: (not leading) and (
    not is_char_kana(input[-1])
)
is_invalid_matcher = lambda input, match_kanji: (
    match_kanji and (not any(is_char_kanji for char in match_kanji))
) or ((not match_kanji) and is_kana(input))


def strip_okurigana(
    input: str = "", leading: bool = False, match_kanji: str = ""
) -> str:
    """Strips Okurigana. If `leading` is set, okurigana will be stripped from the
    beginning instead of the end. If `match_kanji` is set, the input will be treated as
    furigana, and the result will be kana"""
    if (
        (not is_japanese(input))
        or is_leading_without_initial_kana(input, leading)
        or is_trailing_without_final_kana(input, leading)
        or is_invalid_matcher(input, match_kanji)
    ):
        return input
    chars = match_kanji or input
    okurigana_regex = re.compile(
        f"^{tokenise(chars).pop(0)}" if leading else f"{tokenise(chars).pop()}$"
    )
    return okurigana_regex.sub("", input)


custom_roma_to_kana = None


def create_romaji_to_kana_map(
    use_obsolete_kana: bool = False, custom_kana_mapping: dict = None
) -> dict:
    map = get_romaji_to_kana_tree()
    global custom_roma_to_kana

    map = USE_OBSOLETE_KANA_MAP(map) if use_obsolete_kana else map

    if custom_kana_mapping:
        if not custom_roma_to_kana:
            custom_roma_to_kana = merge_custom_mapping(map, custom_kana_mapping)
        map = custom_roma_to_kana

    return map


def _split_into_converted_kana(
    input: str = "",
    use_obsolete_kana: bool = False,
    custom_kana_mapping: dict = None,
    convert_ending: bool = True,
    map: dict = None,
) -> List[Tuple[int, int, str]]:
    if not map:
        map = create_romaji_to_kana_map(
            use_obsolete_kana=use_obsolete_kana, custom_kana_mapping=custom_kana_mapping
        )

    return apply_mapping(input.lower(), map, convert_ending)


def to_kana(
    input: str = "",
    use_obsolete_kana: bool = False,
    custom_kana_mapping: dict = None,
    convert_ending: bool = True,
    full_map: dict = None,
    enforce: Union[None, "hira", "kata"] = None,
) -> str:
    """Converts Romaji to Kana, lowercase will become Hiragana and uppercase will
    become Katakana"""
    if enforce not in [None, "hira", "kata"]:
        enforce = None
    if not full_map:
        kana_map = create_romaji_to_kana_map(
            use_obsolete_kana=use_obsolete_kana, custom_kana_mapping=custom_kana_mapping
        )

    def _process(kana_token: Tuple[int, int, str]) -> str:
        start, end, kana = kana_token
        if not kana:
            # we didn't convert the end of the string
            return input[start:]
        enforce_hiragana = enforce == "hira"
        enforce_katakana = enforce == "kata" or all(
            is_char_uppercase(char) for char in input[start:end]
        )

        return (
            kana
            if enforce_hiragana or (not enforce_katakana)
            else hiragana_to_katakana(kana)
        )

    return "".join(
        map(
            _process,
            _split_into_converted_kana(
                input,
                use_obsolete_kana=use_obsolete_kana,
                custom_kana_mapping=custom_kana_mapping,
                convert_ending=convert_ending,
                map=kana_map,
            ),
        )
    )


custom_kana_to_roma = None


def split_into_romaji(
    input: str,
    custom_romaji_mapping: dict = None,
    convert_ending: bool = True,
    romanisation: ROMANISATIONS = ROMANISATIONS["HEPBURN"],
) -> List[Tuple[int, int, str]]:
    global custom_kana_to_roma
    map = get_kana_to_romaji_tree(romanisation=romanisation)

    if custom_romaji_mapping:
        if not custom_kana_to_roma:
            custom_kana_to_roma = merge_custom_mapping(map, custom_romaji_mapping)
        map = custom_kana_to_roma

    return apply_mapping(
        katakana_to_hiragana(input, to_romaji, True), map, convert_ending
    )


def to_romaji(
    input: str = "",
    uppercase_katakana: bool = False,
    custom_romaji_mapping: dict = None,
    convert_ending: bool = True,
    romanisation: ROMANISATIONS = ROMANISATIONS["HEPBURN"],
):
    """Covert Kana to Romaji"""
    # just throw away the substring index information and just concatenate all the kana
    def _process(romaji_token: Tuple[int, int, str]) -> str:
        start, end, romaji = romaji_token
        make_uppercase = uppercase_katakana and is_katakana(input[start:end])

        return romaji.upper() if make_uppercase else romaji

    return "".join(
        map(
            _process,
            split_into_romaji(
                input, custom_romaji_mapping, convert_ending, romanisation
            ),
        )
    )


def to_hiragana(
    input: str = "",
    ignore_romaji: bool = False,
    use_obsolete_kana: bool = False,
    custom_kana_mapping: dict = None,
    convert_ending: bool = True,
):
    """Convert input to Hiragana"""
    if ignore_romaji:
        return katakana_to_hiragana(input, to_romaji, False)

    if is_mixed(input, ignore_kanji=True):
        converted_katakana = katakana_to_hiragana(input, to_romaji, False)
        return to_kana(
            converted_katakana.lower(),
            use_obsolete_kana=use_obsolete_kana,
            custom_kana_mapping=custom_kana_mapping,
            convert_ending=convert_ending,
        )

    if is_romaji(input) or any(is_char_english_punctuation(char) for char in input):
        return to_kana(
            input.lower(),
            use_obsolete_kana=use_obsolete_kana,
            custom_kana_mapping=custom_kana_mapping,
            convert_ending=convert_ending,
        )

    return katakana_to_hiragana(input, to_romaji, False)


def to_katakana(
    input: str = "",
    ignore_romaji: bool = False,
    use_obsolete_kana: bool = False,
    custom_kana_mapping: dict = None,
    convert_ending: bool = True,
):
    """Convert input to Katakana"""
    if ignore_romaji:
        return hiragana_to_katakana(input)

    if (
        is_mixed(input, ignore_kanji=True)
        or is_romaji(input)
        or any(is_char_english_punctuation(char) for char in input)
    ):
        hiragana = to_kana(
            input.lower(),
            use_obsolete_kana=use_obsolete_kana,
            custom_kana_mapping=custom_kana_mapping,
            convert_ending=convert_ending,
        )
        return hiragana_to_katakana(hiragana)

    return hiragana_to_katakana(input)
