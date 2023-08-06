
"""
----------------------
Python Dictionary API 
----------------------

PyDictAPI is library, written in Python, that can be used to fetch meanings of a word from the web.

Currently supports only English-English dictionary searches

Basic usage:

   >>> from PyDictAPI import Finder
   >>> Meanings = Finder()
   >>> print(Meanings.findMeanings('apple'))

Response:

    {
        'word': 'apple', 
        'meanings': [
            {
                'partOfSpeech': 'noun', 
                'definitions': [
                    {
                        'definition': 'the usually round, red or yellow, edible fruit of a small tree, Malus sylvestris, of the rose family.', 
                        'example': ''
                    }
                ]
            }, 
            {
                'partOfSpeech': 'noun', 
                'definitions': [
                    {
                        'definition': 'a rosaceous tree, Malus sieversii, native to Central Asia but widely cultivated in temperate regions in many varieties, having pink or white fragrant flowers and firm rounded edible fruits', 
                        'example': ''
                    }
                ]
            }
        ]
    }
---------------------------------------    
Finding Examples, Synonyms and Antonyms
---------------------------------------

   >>> print(Meanings.findUsage('help', 2)) #Finding Examples
   
    # Here 2 defines the maximum number of examples to be included in the response, 
    # by default it is set to 5

   >>> print(Meanings.findSynonyms('help', 4)) #Finding Synonyms
   >>> print(Meanings.findAntonyms('help', 4)) #Finding Antonyms
 

Full documentation is at <https://github.com/imshawan/PyDictAPI>.

copyright: (c) 2021 by Shawan Mandal.

license: MIT License, see LICENSE for more details.
"""
__author__ = "Shawan Mandal"
__version__ = "1.3.0"

try:
    from .scrape import *
except:
    from scrape import *

