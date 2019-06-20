TO_KANA_METHODS = {"HIRAGANA": "to_hiragana", "KATAKANA": "to_katakana"}

ROMANISATIONS = {"HEPBURN": "hepburn"}

DEFAULT_OPTIONS = {
    "use_obsolete_kana": False,
    "pass_romaji": False,
    "uppercase_katakana": False,
    "ignore_case": False,
    "IME_mode": False,
    "romanisation": ROMANISATIONS["HEPBURN"],
}

LATIN_LOWERCASE_START = 0x61
LATIN_LOWERCASE_END = 0x7A
LATIN_UPPERCASE_START = 0x41
LATIN_UPPERCASE_END = 0x5A
LOWERCASE_ZENKAKU_START = 0xFF41
LOWERCASE_ZENKAKU_END = 0xFF5A
UPPERCASE_ZENKAKU_START = 0xFF21
UPPERCASE_ZENKAKU_END = 0xFF3A
HIRAGANA_START = 0x3041
HIRAGANA_END = 0x3096
KATAKANA_START = 0x30A1
KATAKANA_END = 0x30FC
KANJI_START = 0x4E00
KANJI_END = 0x9FAF
PROLONGED_SOUND_MARK = 0x30FC
KANA_SLASH_DOT = 0x30FB

ZENKAKU_NUMBERS = [0xFF10, 0xFF19]
ZENKAKU_UPPERCASE = [UPPERCASE_ZENKAKU_START, UPPERCASE_ZENKAKU_END]
ZENKAKU_LOWERCASE = [LOWERCASE_ZENKAKU_START, LOWERCASE_ZENKAKU_END]
ZENKAKU_PUNCTUATION_1 = [0xFF01, 0xFF0F]
ZENKAKU_PUNCTUATION_2 = [0xFF1A, 0xFF1F]
ZENKAKU_PUNCTUATION_3 = [0xFF3B, 0xFF3F]
ZENKAKU_PUNCTUATION_4 = [0xFF5B, 0xFF60]
ZENKAKU_SYMBOLS_CURRENCY = [0xFFE0, 0xFFEE]

HIRAGANA_CHARS = [0x3040, 0x309F]
KATAKANA_CHARS = [0x30A0, 0x30FF]
HANKAKU_KATAKANA = [0xFF66, 0xFF9F]
KATAKANA_PUNCTUATION = [0x30FB, 0x30FC]
KANA_PUNCTUATION = [0xFF61, 0xFF65]
CJK_SYMBOLS_PUNCTUATION = [0x3000, 0x303F]
COMMON_CJK = [0x4E00, 0x9FFF]
RARE_CJK = [0x3400, 0x4DBF]

KANA_RANGES = [HIRAGANA_CHARS, KATAKANA_CHARS, KANA_PUNCTUATION, HANKAKU_KATAKANA]

JA_PUNCTUATION_RANGES = [
    CJK_SYMBOLS_PUNCTUATION,
    KANA_PUNCTUATION,
    KATAKANA_PUNCTUATION,
    ZENKAKU_PUNCTUATION_1,
    ZENKAKU_PUNCTUATION_2,
    ZENKAKU_PUNCTUATION_3,
    ZENKAKU_PUNCTUATION_4,
    ZENKAKU_SYMBOLS_CURRENCY,
]

# All Japanese unicode start and end ranges
# Includes kanji, kana, zenkaku latin chars, punctuation, and number ranges.
JAPANESE_RANGES = [
    *KANA_RANGES,
    *JA_PUNCTUATION_RANGES,
    ZENKAKU_UPPERCASE,
    ZENKAKU_LOWERCASE,
    ZENKAKU_NUMBERS,
    COMMON_CJK,
    RARE_CJK,
]

MODERN_ENGLISH = [0x0000, 0x007F]
HEPBURN_MACRON_RANGES = [
    [0x0100, 0x0101],  # Ā ā
    [0x0112, 0x0113],  # Ē ē
    [0x012A, 0x012B],  # Ī ī
    [0x014C, 0x014D],  # Ō ō
    [0x016A, 0x016B],  # Ū ū
]
SMART_QUOTE_RANGES = [[0x2018, 0x2019], [0x201C, 0x201D]]  # ‘ ’  # “ ”

ROMAJI_RANGES = [MODERN_ENGLISH, *HEPBURN_MACRON_RANGES]

EN_PUNCTUATION_RANGES = [
    [0x20, 0x2F],
    [0x3A, 0x3F],
    [0x5B, 0x60],
    [0x7B, 0x7E],
    *SMART_QUOTE_RANGES,
]