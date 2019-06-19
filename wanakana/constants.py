LATIN_LOWERCASE_START = 0x61
LATIN_LOWERCASE_END = 0x7a
LATIN_UPPERCASE_START = 0x41
LATIN_UPPERCASE_END = 0x5a
LOWERCASE_ZENKAKU_START = 0xff41
LOWERCASE_ZENKAKU_END = 0xff5a
UPPERCASE_ZENKAKU_START = 0xff21
UPPERCASE_ZENKAKU_END = 0xff3a
HIRAGANA_START = 0x3041
HIRAGANA_END = 0x3096
KATAKANA_START = 0x30a1
KATAKANA_END = 0x30fc
KANJI_START = 0x4e00
KANJI_END = 0x9faf
PROLONGED_SOUND_MARK = 0x30fc
KANA_SLASH_DOT = 0x30fb

ZENKAKU_NUMBERS = [0xff10, 0xff19]
ZENKAKU_UPPERCASE = [UPPERCASE_ZENKAKU_START, UPPERCASE_ZENKAKU_END]
ZENKAKU_LOWERCASE = [LOWERCASE_ZENKAKU_START, LOWERCASE_ZENKAKU_END]
ZENKAKU_PUNCTUATION_1 = [0xff01, 0xff0f]
ZENKAKU_PUNCTUATION_2 = [0xff1a, 0xff1f]
ZENKAKU_PUNCTUATION_3 = [0xff3b, 0xff3f]
ZENKAKU_PUNCTUATION_4 = [0xff5b, 0xff60]
ZENKAKU_SYMBOLS_CURRENCY = [0xffe0, 0xffee]

HIRAGANA_CHARS = [0x3040, 0x309f]
KATAKANA_CHARS = [0x30a0, 0x30ff]
HANKAKU_KATAKANA = [0xff66, 0xff9f]
KATAKANA_PUNCTUATION = [0x30fb, 0x30fc]
KANA_PUNCTUATION = [0xff61, 0xff65]
CJK_SYMBOLS_PUNCTUATION = [0x3000, 0x303f]
COMMON_CJK = [0x4e00, 0x9fff]
RARE_CJK = [0x3400, 0x4dbf]

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
  ...KANA_RANGES,
  ...JA_PUNCTUATION_RANGES,
  ZENKAKU_UPPERCASE,
  ZENKAKU_LOWERCASE,
  ZENKAKU_NUMBERS,
  COMMON_CJK,
  RARE_CJK,
]

MODERN_ENGLISH = [0x0000, 0x007f]
HEPBURN_MACRON_RANGES = [
  [0x0100, 0x0101], # Ā ā
  [0x0112, 0x0113], # Ē ē
  [0x012a, 0x012b], # Ī ī
  [0x014c, 0x014d], # Ō ō
  [0x016a, 0x016b], # Ū ū
]
SMART_QUOTE_RANGES = [
  [0x2018, 0x2019], # ‘ ’
  [0x201c, 0x201d], # “ ”
]

ROMAJI_RANGES = [MODERN_ENGLISH, *HEPBURN_MACRON_RANGES]

EN_PUNCTUATION_RANGES = [
  [0x20, 0x2f],
  [0x3a, 0x3f],
  [0x5b, 0x60],
  [0x7b, 0x7e],
  *SMART_QUOTE_RANGES,
]