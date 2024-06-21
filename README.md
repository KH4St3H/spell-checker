# SpellChecker
Simple and easy to use spell checker library written in python


## Usage
```python
# With built-in engilsh dictionary
from spell_checker.spellchecker import SpellChecker
sp = SpellChecker()

print(sp.slice_n_check('tost'))
```
```python
# With custom engilsh dictionary
from spell_checker.spellchecker import SpellChecker
from spell_checker.dictionary import Dictionary
custom_dictionary = Dictionary()
custom_dictionary.add_from_file('example_dict_es.txt')
sp = SpellChecker(dictionary=custom_dictionary)

print(sp.slice_n_check('holo'))
```
