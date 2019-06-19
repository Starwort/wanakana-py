|ワナカナ \<--> WanaKana \<--> わなかな|
|:--:|
|Python utility library for detecting and transliterating Hiragana, Katakana, and Romaji|

## This library uses Semantic Versioning

See what this means [here](https://semver.org/)

## Demo

Visit the [website](http:#www.wanakana.com) to see WanaKana in action.

## Usage

### Install

```bash
pip install wanakana-python
```

```python
import wanakana
# or
from wanakana import to_kana, is_romaji
```

## Documentation

[Extended API reference](http://www.wanakana.com/docs/global.html)
(Note that function names are converted to snake_case)

## Quick Reference

```python
### TEXT CHECKING UTILITIES ###
wanakana.is_japanese('泣き虫。！〜２￥ｚｅｎｋａｋｕ')
# => true

wanakana.is_kana('あーア')
# => true

wanakana.is_hiragana('すげー')
# => true

wanakana.is_katakana('ゲーム')
# => true

wanakana.is_kanji('切腹')
# => true
wanakana.is_kanji('勢い')
# => false

wanakana.isRomaji('Tōkyō and Ōsaka')
# => true

wanakana.to_kana('ONAJI buttsuuji')
# => 'オナジ ぶっつうじ'
wanakana.to_kana('座禅‘zazen’スタイル')
# => '座禅「ざぜん」スタイル'
wanakana.to_kana('batsuge-mu')
# => 'ばつげーむ'
wanakana.to_kana('wanakana', custom_kana_mapping={'na': 'に', 'ka': 'bana' })
# => 'わにbanaに'

wanakana.to_hiragana('toukyou, オオサカ')
# => 'とうきょう、　おおさか'
wanakana.to_hiragana('only カナ', pass_romaji=True)
# => 'only かな'
wanakana.to_hiragana('wi', use_obsolete_kana=True)
# => 'ゐ'

wanakana.to_katakana('toukyou, おおさか')
# => 'トウキョウ、　オオサカ'
wanakana.to_katakana('only かな', pass_romaji=True)
# => 'only カナ'
wanakana.to_katakana('wi', use_obsolete_kana=True)
# => 'ヰ'

wanakana.to_romaji('ひらがな　カタカナ')
# => 'hiragana katakana'
wanakana.to_romaji('ひらがな　カタカナ', uppercase_katakana=True)
# => 'hiragana KATAKANA'
wanakana.to_romaji('つじぎり', custom_romaji_mapping={'じ': 'zi', 'つ': 'tu', 'り': 'li' })
# => 'tuzigili'

### EXTRA UTILITIES ###
wanakana.strip_okurigana('お祝い')
# => 'お祝'
wanakana.strip_okurigana('踏み込む')
# => '踏み込'
wanakana.strip_okurigana('お腹', leading=True)
# => '腹'
wanakana.strip_okurigana('ふみこむ', match_kanji='踏み込む')
# => 'ふみこ'
wanakana.strip_okurigana('おみまい', match_kanji='お祝い', leading=True)
# => 'みまい'

wanakana.tokenise('ふふフフ')
# => ['ふふ', 'フフ']
wanakana.tokenise('hello 田中さん')
# => ['hello', ' ', '田中', 'さん']
wanakana.tokenise('I said 私はすごく悲しい', compact=True)
# => [ 'I said ', '私はすごく悲しい']
```

## Contributors

* [Starwort](https://github.com/starwort) – Author

## Credits

Port of [WanaKana](https://github.com/WaniKani/WanaKana)
