from copy import deepcopy
from .kana_mapping import transform, get_subtree_of, create_custom_mapping

# NOTE: not exactly kunrei shiki, for example ぢゃ -> dya instead of zya
# to avoid name clashing
BASIC_KUNREI = {
    "a": "あ",
    "i": "い",
    "u": "う",
    "e": "え",
    "o": "お",
    "k": {"a": "か", "i": "き", "u": "く", "e": "け", "o": "こ"},
    "s": {"a": "さ", "i": "し", "u": "す", "e": "せ", "o": "そ"},
    "t": {"a": "た", "i": "ち", "u": "つ", "e": "て", "o": "と"},
    "n": {"a": "な", "i": "に", "u": "ぬ", "e": "ね", "o": "の"},
    "h": {"a": "は", "i": "ひ", "u": "ふ", "e": "へ", "o": "ほ"},
    "m": {"a": "ま", "i": "み", "u": "む", "e": "め", "o": "も"},
    "y": {"a": "や", "u": "ゆ", "o": "よ"},
    "r": {"a": "ら", "i": "り", "u": "る", "e": "れ", "o": "ろ"},
    "w": {"a": "わ", "i": "ゐ", "e": "ゑ", "o": "を"},
    "g": {"a": "が", "i": "ぎ", "u": "ぐ", "e": "げ", "o": "ご"},
    "z": {"a": "ざ", "i": "じ", "u": "ず", "e": "ぜ", "o": "ぞ"},
    "d": {"a": "だ", "i": "ぢ", "u": "づ", "e": "で", "o": "ど"},
    "b": {"a": "ば", "i": "び", "u": "ぶ", "e": "べ", "o": "ぼ"},
    "p": {"a": "ぱ", "i": "ぴ", "u": "ぷ", "e": "ぺ", "o": "ぽ"},
    "v": {"a": "ゔぁ", "i": "ゔぃ", "u": "ゔ", "e": "ゔぇ", "o": "ゔぉ"},
}

SPECIAL_SYMBOLS = {
    ".": "。",
    ",": "、",
    ":": "：",
    "/": "・",
    "!": "！",
    "?": "？",
    "~": "〜",
    "-": "ー",
    "‘": "「",
    "’": "」",
    "“": "『",
    "”": "』",
    "[": "［",
    "]": "］",
    "(": "（",
    ")": "）",
    "{": "｛",
    "}": "｝",
}

CONSONANTS = {
    "k": "き",
    "s": "し",
    "t": "ち",
    "n": "に",
    "h": "ひ",
    "m": "み",
    "r": "り",
    "g": "ぎ",
    "z": "じ",
    "d": "ぢ",
    "b": "び",
    "p": "ぴ",
    "v": "ゔ",
    "q": "く",
    "f": "ふ",
}
SMALL_Y = {"ya": "ゃ", "yi": "ぃ", "yu": "ゅ", "ye": "ぇ", "yo": "ょ"}
SMALL_VOWELS = {"a": "ぁ", "i": "ぃ", "u": "ぅ", "e": "ぇ", "o": "ぉ"}

# typing one should be the same as having typed the other instead
ALIASES = {
    "sh": "sy",  # sha -> sya
    "ch": "ty",  # cho -> tyo
    "cy": "ty",  # cyo -> tyo
    "chy": "ty",  # chyu -> tyu
    "shy": "sy",  # shya -> sya
    "dj": "dy",  # dja -> dya
    "j": "zy",  # ja -> zya
    "jy": "zy",  # jye -> zye
    # exceptions to above rules
    "shi": "si",
    "chi": "ti",
    "tsu": "tu",
    "dzu": "du",
    "ji": "zi",
    "dji": "di",
    "fu": "hu",
}

# xtu -> っ
SMALL_LETTERS = {"tu": "っ", "wa": "ゎ", "ka": "ヵ", "ke": "ヶ"}
SMALL_LETTERS.update(SMALL_VOWELS)
SMALL_LETTERS.update(SMALL_Y)

# don't follow any notable patterns
SPECIAL_CASES = {
    "yi": "い",
    "wu": "う",
    "ye": "いぇ",
    "wi": "うぃ",
    "we": "うぇ",
    "kwa": "くぁ",
    "whu": "う",
    # because it's not thya for てゃ but tha
    # and tha is not てぁ, but てゃ
    "tha": "てゃ",
    "thu": "てゅ",
    "tho": "てょ",
    "dha": "でゃ",
    "dhu": "でゅ",
    "dho": "でょ",
}

AIUEO_CONSTRUCTIONS = {
    "wh": "う",
    "qw": "く",
    "q": "く",
    "gw": "ぐ",
    "sw": "す",
    "ts": "つ",
    "th": "て",
    "tw": "と",
    "dh": "で",
    "dw": "ど",
    "fw": "ふ",
    "f": "ふ",
}


def create_romaji_to_kana_map():
    kana_tree = transform(BASIC_KUNREI)
    # pseudo partial application
    subtree_of = lambda string: get_subtree_of(kana_tree, string)

    # add tya, sya, etc.
    for consonant, y_kana in CONSONANTS.items():
        for roma, kana in SMALL_Y.items():
            # for example kyo -> き + ょ
            subtree_of(consonant + roma)[""] = y_kana + kana

    for symbol, jsymbol in SPECIAL_SYMBOLS.items():
        subtree_of(symbol)[""] = jsymbol

    # things like うぃ, くぃ, etc.
    for consonant, aiueo_kana in AIUEO_CONSTRUCTIONS.items():
        for vowel, kana in SMALL_VOWELS.items():
            subtree_of(consonant + vowel)[""] = aiueo_kana + kana

    # different ways to write ん
    for n_char in ["n", "n'", "xn"]:
        subtree_of(n_char)[""] = "ん"

    # c is equivalent to k, but not for chi, cha, etc. That's why we have
    # to make a copy of k
    kana_tree["c"] = deepcopy(kana_tree["k"])

    for string, alternative in ALIASES.items():
        all_except_last = string[:-1]
        last = string[-1]
        parent_tree = subtree_of(all_except_last)
        # copy to avoid recursive containment
        parent_tree[last] = deepcopy(subtree_of(alternative))

    def get_alternatives(string: str):
        items = []

        for alt, roma in [*ALIASES.items(), ["c", "k"]]:
            if string.startswith(roma):
                items.append(string.replace(roma, alt))

        return items

    for kunrei_roma, kana in SMALL_LETTERS.items():
        last = lambda char: char[-1]
        all_except_last = lambda chars: chars[:-1]
        x_roma = f"x{kunrei_roma}"
        x_subtree = subtree_of(x_roma)
        x_subtree[""] = kana

        # ltu -> xtu -> っ
        subtree_of(f"l{all_except_last(kunrei_roma)}")[last(kunrei_roma)] = x_subtree

        # ltsu -> ltu -> っ
        for alt_roma in get_alternatives(kunrei_roma):
            for prefix in "lx":
                subtree_of(prefix + all_except_last(alt_roma))[
                    last(alt_roma)
                ] = subtree_of(prefix + kunrei_roma)

    for string, kana in SPECIAL_CASES.items():
        subtree_of(string)[""] = kana

    # add kka tta, etc.
    def add_tsu(tree: dict):
        tsu_tree = {}

        for key, value in tree.items():
            if not key:
                # we have reached the bottom of this branch
                tsu_tree[key] = f"っ{value}"
            else:
                # more subtrees
                tsu_tree[key] = add_tsu(value)

        return tsu_tree

    # have to explicitly name c here, because we made it a copy of k, not a reference
    for consonant in [*CONSONANTS.keys(), "c", "y", "w", "j"]:
        subtree = kana_tree[consonant]
        subtree[consonant] = add_tsu(subtree)

    # nn should not be っん
    del kana_tree["n"]["n"]
    return deepcopy(kana_tree)


romaji_to_kana_map = None


def get_romaji_to_kana_tree():
    global romaji_to_kana_map

    if not romaji_to_kana_map:
        romaji_to_kana_map = create_romaji_to_kana_map()

    return romaji_to_kana_map


USE_OBSOLETE_KANA_MAP = create_custom_mapping({"wi": "ゐ", "we": "ゑ"})

