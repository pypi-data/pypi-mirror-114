[![PyDictAPI: Passing](https://img.shields.io/badge/PyDictAPI-Passing-limegreen)](https://github.com/imshawan/PyDictAPI)
[![GitHub license](https://img.shields.io/github/license/imshawan/PyDictAPI)](https://github.com/imshawan/PyDictAPI/blob/master/LICENSE.txt)
![Release: 1.1.0](https://img.shields.io/badge/Release-1.1.0-informational)

# PyDictionaryAPI
### A simple web-scraping based Dictionary Module for Python

PyDictAPI is a Dictionary Module for Python 3+ to get a detailed and well-structured meanings of a queried word in JSON format. This module can also be used along with Flask/Django backends to make a full-fledged API server.<br><br>
PyDictAPI searches for the query passed on the web, if the query matches than it returns the definations of that particular query. And incase of incorrect words, the response is returned as a suggestion of the correct word.

>  **Note** It uses Dictionary.com for extracting the meanings.

This module uses Requests, BeautifulSoup4 dependencies to scrape the web and find the definations and return it in a well-structured JSON document

## Installation

PyDictAPI can be easily installed through [PIP](https://pip.pypa.io/en/stable/)

```
pip install PyDictAPI
```

## Usage

PyDictAPI can be used by creating a MeaningsFinder instance which can take a word as argument

For example,

```python
from PyDictAPI import MeaningsFinder
Meanings = MeaningsFinder()
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
                'definations': [
                        {
                            'definition': 'The usually round, red or yellow, edible fruit of a small tree, Malus sylvestris, of the rose family.', 
                            'example': ''
                        }
                    ]
            }, 
            {
                'partOfSpeech': 'Noun', 
                'definations': [
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

## About

Current Version: 1.1.0 <br>
Copyright (c) 2021 Shawan Mandal.
