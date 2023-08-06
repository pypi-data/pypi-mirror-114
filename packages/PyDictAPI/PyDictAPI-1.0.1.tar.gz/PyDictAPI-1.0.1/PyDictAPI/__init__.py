
"""
----------------------
Python Dictionary API 
----------------------

PyDictAPI is library, written in Python, that can be used to fetch meanings of a word from the web.\n
Currently supports only English-English dictionary searches\n
Basic usage:

   >>> from PyDictAPI import MeaningsFinder
   >>> Meanings = MeaningsFinder()
   >>> print(Meanings.findMeanings('apple'))
Response:
   {
       'word': 'apple', 
       'meanings': [
           {'partOfSpeech': 'noun', 
           'definations': [
               {'definition': 'the usually round, red or yellow, edible fruit of a small tree, Malus sylvestris, of the rose family.', 
               'example': ''}
               ]
               }, 
               {'partOfSpeech': 'noun', 
                'definations': [
                    {'definition': 'a rosaceous tree, Malus sieversii, native to Central Asia but widely cultivated in temperate regions in many varieties, having pink or white fragrant flowers and firm rounded edible fruits', 
                    'example': ''}
                ]
            }
        ]
    }

Full documentation is at <https://github.com/imshawan/PyDictAPI>.

:copyright: (c) 2021 by Shawan mandal.
:license: MIT License, see LICENSE for more details.
"""
__author__ = "Shawan Mandal"
__version__ = "1.0.0"

try:
    from .scrape import *
except:
    from scrape import *

