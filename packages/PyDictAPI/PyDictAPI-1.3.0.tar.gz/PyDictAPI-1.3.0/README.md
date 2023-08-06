[![PyDictAPI](https://img.shields.io/badge/PyDictAPI-Stable-limegreen)](https://github.com/imshawan/PyDictAPI)
[![GitHub license](https://img.shields.io/github/license/imshawan/PyDictAPI)](https://github.com/imshawan/PyDictAPI/blob/master/LICENSE.txt)
[![Latest Version](http://img.shields.io/pypi/v/PyDictAPI.svg?style=flat-square)](https://pypi.python.org/pypi/PyDictAPI/)
[![Downloads](https://img.shields.io/pypi/dm/PyDictAPI.svg?style=flat-square)](https://pypi.python.org/pypi/PyDictAPI/)

# PyDictionaryAPI
### A simple web-scraping based Dictionary Module for Python

PyDictAPI is a Dictionary Module for Python 3+ to get a detailed and well-structured meanings of a queried word in JSON format. This module can also be used along with Flask/Django backends to make a full-fledged API server.<br><br>
PyDictAPI searches for the query on the web, if the query matches than it returns the Definitions/Examples/Synonyms/Antonyms as specified by the user. And incase of incorrect words, the response is returned as a suggestion of the correct word.
<br>

>  **Sources:** [Dictionary.com](https://www.dictionary.com/), [Thesaurus](https://www.thesaurus.com/), [Lexico](https://www.lexico.com/)

This module uses Requests and bs4 dependencies to scrape the web and find the definitions and return it in a well-structured JSON document

## Installation

PyDictAPI can be easily installed through [PIP](https://pip.pypa.io/en/stable/)

```
pip install PyDictAPI
```
### [View Changelog](https://github.com/imshawan/PyDictAPI/blob/master/CHANGELOG.md)

## Usage

PyDictAPI can be used by creating a Finder instance which can take a word as argument

For example,

```python
from PyDictAPI import Finder
Meanings = Finder()
print(Meanings.findMeanings('apple'))
```

This is will create a local instance of the MeaningsFinder class and will return a dictionary containing the meanings of the word. <br>
The Response can be seen as:

```
{
    'word': 'Apple', 
    'meanings': [
            {
                'partOfSpeech': 'Noun', 
                'definitions': [
                        {
                            'definition': 'The usually round, red or yellow, edible fruit of a small tree, Malus sylvestris, of the rose family.', 
                            'example': ''
                        }
                    ]
            }, 
            {
                'partOfSpeech': 'Noun', 
                'definitions': [
                    {
                        'definition': 'A rosaceous tree, Malus sieversii, native to Central Asia but widely cultivated in temperate regions in many varieties, having pink or white fragrant flowers and firm rounded edible fruits', 
                        'example': ''
                    }
                ]
            }
        ]
}                                                                       
```
## Exceptions

### Example - 1: If the word is spelt incorrectly

```python
print(Meanings.findMeanings('helloooo'))
```
Incase of incorrect words, the response is returned as a suggestion of the correct word <br>
The Response can be seen as:

```
{
    'message': 'Couldn't find results for helloooo, Did you mean hello?'
}
```

### Example - 2: If the word doesn't exist

```python
print(Meanings.findMeanings('abcdefghijkl'))
```
The Response can be seen as:

```
{
    'message': 'Couldn't find any results for ABCDEFGHIJKL, try searching the web...'
}
```
## Finding Examples, Synonyms and Antonyms

```python
print(Meanings.findUsage('help', 2)) #Finding Examples
# Here 2 defines the maximum number of examples to be included in the response, 
# by default it is set to 5

print(Meanings.findSynonyms('help', 4)) #Finding Synonyms
print(Meanings.findAntonyms('help', 4)) #Finding Antonyms

```

### Responses for Examples, Synonyms and Antonyms

Examples: <br>
```
{
    'help': ['She helped him find a buyer', 'Long-term funding is desperately being sought for a voluntary service that helps local victims of domestic violence.']
}
```

Synonyms: <br>
```
{'help': ['Advice', 'Aid', 'Benefit', 'Comfort']}
```

Antonyms: <br>
```
{'help': ['Blockage', 'Encumbrance', 'Handicap', 'Hindrance']}
```


## About

Copyright (c) 2021 Shawan Mandal.
