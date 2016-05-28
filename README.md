# CJK tools for Python

[![Build Status](https://travis-ci.org/larsyencken/cjktools.png)](https://travis-ci.org/larsyencken/cjktools)

## Overview

The cjktools package provides useful tools for language processing in Japanese and Chinese, in particular working with dictionaries and other resources. It provides methods for checking the script type of a string. For example:

```pycon
>>> from cjktools import scripts
>>> scripts.script_types(u'素晴らしい')
set([Kanji, Hiragana])
>>> scripts.script_boundaries(u'素晴らしい')
(u'\u7d20\u6674', u'\u3089\u3057\u3044')
```

Cjktools can also segment pinyin, convert it from ASCII form (like 'li4') to unicode tones (like u'lì'), as well as a range of other features. In keeping with the "batteries included" philosophy of Python, each of the free dictionaries cjktools supports is included in the cjktools-data package.

For an alternative library for CJK support in Python, or a command-line dictionary lookup tool, see the related [cjklib](http://code.google.com/p/cjklib/) project.

## Installing

The easiest way to install `cjktools` is to to simply run:

```
pip install cjktools
```

The most recent package will then be downloaded and installed for you. If you also wish to make use of dictionary interfaces, you should install matching [cjkdata](https://github.com/larsyencken/cjkdata) bundle.

```
wget http://files.gakusha.info/cjkdata-2013-06-15-c54b33e.tgz
tar xfz cjkdata-2013-06-15-c54b33e.tgz
mv cjkdata ~/.cjkdata
```

You can put the `cjkdata` directory wherever you like, by specifying its location in the `CJKDATA` environment variable.

You will then have easy access to dictionary resources for Japanese, and the tools to manipulate them.

## Dictionary resources

The `cjktools.resources` package provides access to a large number of dictionary resources. Here are a few examples.

### Radkdict

An interface to the `radkfile`. The `RadkDict` class is basically a dictionary which maps kanji to their components.

```pycon
>>> from cjktools.resources.radkdict import RadkDict
>>> print(', '.join(RadkDict())[u'明'])
日, 月
```

### Auto-format

An extensible wrapper for EDICT and EDICT-like dictionary formats. Here's an example where we load the dictionary and look at an entry.

```pycon
>>> from cjktools.resources import cjkdata, auto_format
>>> edict_file = cjkdata.get_resource('dict/je_edict')
>>> edict = auto_format.load_dictionary(open(edict_file))
>>> edict['パチンコ']
<DictionaryEntry: パチンコ (1 readings, 4 senses)>
>>> _.senses
[u'(n) (1) pachinko (Japanese pinball)', u'(2) slingshot', u'catapult', u'(P)']
```

Several dictionary files are bundled with the `cjktools-data` package:

```
Dictionary  Description                               Path to use
==========  ===========                               ===========
EDICT       General Japanese-English dictionary.      dict/je_edict
JPLACES     Japanese place names.                     dict/je_jplaces
ENAMDIC     Japanese person, place and company names. dict/je_enamdict
COMPDIC     Japanese computing terms.                 dict/je_compdic
CEDICT      General Chinese-English dictionary.       dict/ce_cedict
```

### Kanjidic

A simple dictionary of kanji reading and indexes in various lookup schemes.

```pycon
>>> from cjktools.resources import kanjidic
>>> kjd = kanjidic.Kanjidic()
>>> entry = kjd[u'上']
>>> print(', '.join(entry.gloss))
above, up
>>> print(', '.join(entry.on_readings))
ジョウ, ショウ, シャン
>>> print(', '.join(entry.kun_readings)[:10])
うえ, -うえ, うわ-, かみ, あ.げる, -あ.げる, あ.がる, -あ.がる, あ.がり, -あ.がり
```

