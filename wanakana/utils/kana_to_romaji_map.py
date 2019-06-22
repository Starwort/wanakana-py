from copy import deepcopy
from .kana_mapping import transform, get_subtree_of
from ..constants import ROMANISATIONS

kana_to_hepburn_map = None
kana_to_kunrei_map = None
BASIC_HEPBURN = {
    "あ": "a",
    "い": "i",
    "う": "u",
    "え": "e",
    "お": "o",
    "か": "ka",
    "き": "ki",
    "く": "ku",
    "け": "ke",
    "こ": "ko",
    "さ": "sa",
    "し": "shi",
    "す": "su",
    "せ": "se",
    "そ": "so",
    "た": "ta",
    "ち": "chi",
    "つ": "tsu",
    "て": "te",
    "と": "to",
    "な": "na",
    "に": "ni",
    "ぬ": "nu",
    "ね": "ne",
    "の": "no",
    "は": "ha",
    "ひ": "hi",
    "ふ": "fu",
    "へ": "he",
    "ほ": "ho",
    "ま": "ma",
    "み": "mi",
    "む": "mu",
    "め": "me",
    "も": "mo",
    "ら": "ra",
    "り": "ri",
    "る": "ru",
    "れ": "re",
    "ろ": "ro",
    "や": "ya",
    "ゆ": "yu",
    "よ": "yo",
    "わ": "wa",
    "ゐ": "wi",
    "ゑ": "we",
    "を": "wo",
    "ん": "n",
    "が": "ga",
    "ぎ": "gi",
    "ぐ": "gu",
    "げ": "ge",
    "ご": "go",
    "ざ": "za",
    "じ": "ji",
    "ず": "zu",
    "ぜ": "ze",
    "ぞ": "zo",
    "だ": "da",
    "ぢ": "dji",
    "づ": "dzu",
    "で": "de",
    "ど": "do",
    "ば": "ba",
    "び": "bi",
    "ぶ": "bu",
    "べ": "be",
    "ぼ": "bo",
    "ぱ": "pa",
    "ぴ": "pi",
    "ぷ": "pu",
    "ぺ": "pe",
    "ぽ": "po",
    "ゔぁ": "va",
    "ゔぃ": "vi",
    "ゔ": "vu",
    "ゔぇ": "ve",
    "ゔぉ": "vo",
}
BASIC_KUNREI = {
    "あ": "a",
    "い": "i",
    "う": "u",
    "え": "e",
    "お": "o",
    "か": "ka",
    "き": "ki",
    "く": "ku",
    "け": "ke",
    "こ": "ko",
    "さ": "sa",
    "し": "si",
    "す": "su",
    "せ": "se",
    "そ": "so",
    "た": "ta",
    "ち": "ti",
    "つ": "tu",
    "て": "te",
    "と": "to",
    "な": "na",
    "に": "ni",
    "ぬ": "nu",
    "ね": "ne",
    "の": "no",
    "は": "ha",
    "ひ": "hi",
    "ふ": "hu",
    "へ": "he",
    "ほ": "ho",
    "ま": "ma",
    "み": "mi",
    "む": "mu",
    "め": "me",
    "も": "mo",
    "ら": "ra",
    "り": "ri",
    "る": "ru",
    "れ": "re",
    "ろ": "ro",
    "や": "ya",
    "ゆ": "yu",
    "よ": "yo",
    "わ": "wa",
    "ゐ": "i",
    "ゑ": "e",
    "を": "o",
    "ん": "n",
    "が": "ga",
    "ぎ": "gi",
    "ぐ": "gu",
    "げ": "ge",
    "ご": "go",
    "ざ": "za",
    "じ": "zi",
    "ず": "zu",
    "ぜ": "ze",
    "ぞ": "zo",
    "だ": "da",
    "ぢ": "zi",
    "づ": "zu",
    "で": "de",
    "ど": "do",
    "ば": "ba",
    "び": "bi",
    "ぶ": "bu",
    "べ": "be",
    "ぼ": "bo",
    "ぱ": "pa",
    "ぴ": "pi",
    "ぷ": "pu",
    "ぺ": "pe",
    "ぽ": "po",
    "ゔぁ": "va",
    "ゔぃ": "vi",
    "ゔ": "vu",
    "ゔぇ": "ve",
    "ゔぉ": "vo",
}

SPECIAL_SYMBOLS = {
    "。": ".",
    "、": ",",
    "：": ":",
    "・": "/",
    "！": "!",
    "？": "?",
    "〜": "~",
    "ー": "-",
    "「": "‘",
    "」": "’",
    "『": "“",
    "』": "”",
    "［": "[",
    "］": "]",
    "（": "(",
    "）": ")",
    "｛": "{",
    "｝": "}",
    "　": " ",
}

# んい -> n'i
AMBIGUOUS_VOWELS = ["あ", "い", "う", "え", "お", "や", "ゆ", "よ"]
SMALL_Y = {"ゃ": "ya", "ゅ": "yu", "ょ": "yo"}
SMALL_Y_EXTRA = {"ぃ": "yi", "ぇ": "ye"}
SMALL_AIUEO = {"ぁ": "a", "ぃ": "i", "ぅ": "u", "ぇ": "e", "ぉ": "o"}
YOON_KANA = ["き", "に", "ひ", "み", "り", "ぎ", "び", "ぴ", "ゔ", "く", "ふ"]
YOON_EXCEPTIONS = {"し": "sh", "ち": "ch", "じ": "j", "ぢ": "dj"}
SMALL_KANA = {
    "っ": "",
    "ゃ": "ya",
    "ゅ": "yu",
    "ょ": "yo",
    "ぁ": "a",
    "ぃ": "i",
    "ぅ": "u",
    "ぇ": "e",
    "ぉ": "o",
}

# going with the intuitive (yet incorrect) solution where っや -> yya and っぃ -> ii
# in other words, just assume the sokuon could have been applied to anything
SOKUON_WHITELIST = {
    "b": "b",
    "c": "t",
    "d": "d",
    "f": "f",
    "g": "g",
    "h": "h",
    "j": "j",
    "k": "k",
    "m": "m",
    "p": "p",
    "q": "q",
    "r": "r",
    "s": "s",
    "t": "t",
    "v": "v",
    "w": "w",
    "x": "x",
    "z": "z",
}


def resolve_tsu(tree: dict) -> dict:
    tsu_tree = {}
    for key, value in tree.items():
        if not key:
            # we have reached the bottom of this branch
            consonant = value[0]
            tsu_tree[key] = SOKUON_WHITELIST.get(consonant, "") + value
        else:
            tsu_tree[key] = resolve_tsu(value)
    return tsu_tree


def create_kana_to_hepburn_map() -> dict:
    romaji_tree = transform(BASIC_HEPBURN)

    subtree_of = lambda string: get_subtree_of(romaji_tree, string)

    def set_trans(string, transliteration):
        subtree_of(string)[""] = transliteration

    for jsymbol, symbol in SPECIAL_SYMBOLS.items():
        set_trans(jsymbol, symbol)

    for roma, kana in SMALL_Y.items():
        set_trans(roma, kana)

    for roma, kana in SMALL_AIUEO.items():
        set_trans(roma, kana)

    for kana in YOON_KANA:
        first_romaji_char = subtree_of(kana)[""][0]

        # きゃ -> kya
        for y_kana, y_roma in SMALL_Y.items():
            set_trans(kana + y_kana, first_romaji_char + y_roma)

        # きぃ -> kyi
        for y_kana, y_roma in SMALL_Y_EXTRA.items():
            set_trans(kana + y_kana, first_romaji_char + y_roma)

    for kana, roma in YOON_EXCEPTIONS.items():
        # じゃ -> ja
        for y_kana, y_roma in SMALL_Y.items():
            set_trans(kana + y_kana, roma + y_roma[1])

        # じぃ -> jyi, じぇ -> je
        set_trans(f"{kana}ぃ", f"{roma}yi")
        set_trans(f"{kana}ぇ", f"{roma}e")

    romaji_tree["っ"] = resolve_tsu(romaji_tree)

    for kana, roma in SMALL_KANA.items():
        set_trans(kana, roma)

    for kana in AMBIGUOUS_VOWELS:
        set_trans(f"ん{kana}", f"n'{subtree_of(kana)['']}")

    return romaji_tree.copy()


def create_kana_to_kunrei_map() -> dict:
    romaji_tree = transform(BASIC_KUNREI)

    subtree_of = lambda string: get_subtree_of(romaji_tree, string)

    def set_trans(string, transliteration):
        subtree_of(string)[""] = transliteration

    for jsymbol, symbol in SPECIAL_SYMBOLS.items():
        set_trans(jsymbol, symbol)

    for roma, kana in SMALL_Y.items():
        set_trans(roma, kana)

    for roma, kana in SMALL_AIUEO.items():
        set_trans(roma, kana)

    for kana in YOON_KANA:
        first_romaji_char = subtree_of(kana)[""][0]

        # きゃ -> kya
        for y_kana, y_roma in SMALL_Y.items():
            set_trans(kana + y_kana, first_romaji_char + y_roma)

        # きぃ -> kyi
        for y_kana, y_roma in SMALL_Y_EXTRA.items():
            set_trans(kana + y_kana, first_romaji_char + y_roma)

    for kana, roma in YOON_EXCEPTIONS.items():
        # じゃ -> ja
        for y_kana, y_roma in SMALL_Y.items():
            set_trans(kana + y_kana, roma + y_roma[1])

        # じぃ -> jyi, じぇ -> je
        set_trans(f"{kana}ぃ", f"{roma}yi")
        set_trans(f"{kana}ぇ", f"{roma}e")

    romaji_tree["っ"] = resolve_tsu(romaji_tree)

    for kana, roma in SMALL_KANA.items():
        set_trans(kana, roma)

    for kana in AMBIGUOUS_VOWELS:
        set_trans(f"ん{kana}", f"n'{subtree_of(kana)['']}")

    return romaji_tree.copy()


def get_kana_to_hepburn_tree() -> dict:
    global kana_to_hepburn_map
    if not kana_to_hepburn_map:
        kana_to_hepburn_map = create_kana_to_hepburn_map()
    return deepcopy(kana_to_hepburn_map)


def get_kana_to_kunrei_tree() -> dict:
    global kana_to_kunrei_map
    if not kana_to_kunrei_map:
        kana_to_kunrei_map = create_kana_to_kunrei_map()
    return deepcopy(kana_to_kunrei_map)


def get_kana_to_romaji_tree(*, romanisation: str, **kwargs) -> dict:
    if romanisation == ROMANISATIONS["HEPBURN"]:
        return get_kana_to_hepburn_tree()
    if romanisation == ROMANISATIONS["KUNREI"]:
        return get_kana_to_kunrei_tree()
    return {}
