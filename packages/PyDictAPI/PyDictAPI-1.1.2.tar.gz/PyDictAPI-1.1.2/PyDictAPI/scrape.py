"""
Author: Shawan Mandal
    
MIT License, see LICENSE for more details.
Copyright (c) 2021 Shawan Mandal

"""

import sys
try:
    from utils import handleRequests, getSoupObj
except:
    from .utils import handleRequests, getSoupObj

class PythonVersionError(Exception):
    pass

class MeaningsFinder(object):
    """
    MeaningsFinder
    Usage:
        >>> Meanings = MeaningsFinder()
        >>> print(Meanings.findMeanings('apple'))
    """
    def __init__(self):
        self.isPython3 = True
        if (sys.version_info.major) < 3:
            self.isPython3 = False
        else:
            pass

    def findMeanings(self, word):
        '''
        Searches for a word and returns response in a python Dictionary Obj,
        Alternatively searches for any possible matches incase the queried word is not found
        '''
        if (self.isPython3):
            pass
        else:
            raise PythonVersionError("Python version 3 or newer is required")

        def IfnotFound(word):
            '''
            1.  Returns any possible matches incase if the queried word is not found
            2.  Returns a resolution incase if nothing is found
            '''
            resolution = {"message": f"Couldn't find any results for {word.upper()}, try searching the web..."}

            res = handleRequests(word)
            soup = getSoupObj(res)

            try:
                suggestedContent = soup.find(attrs={'class': 'spell-suggestions-subtitle css-ycbn4w e19m0k9k5'})
                suggestedWord = suggestedContent.find('a')
                return {"message": f"Couldn't find results for {word}, Did you mean {suggestedWord.text}?"}
            except:
                return resolution


        res = handleRequests(word)
        soup = getSoupObj(res)
        dataItems = {
            "word": word.title(),
            "meanings": []
        }

        contents = soup.findAll(attrs={'class': 'css-pnw38j e1hk9ate4'})
        for each in contents:
            defFound = True
            json_contents = {}
            partOfSpeech = each.find(attrs={'class': 'css-18hgvva e1hk9ate3'})
            for pos in partOfSpeech.find_all("span", {'class':'luna-inflected-form'}):
                    pos.replaceWith('')
            for pos1 in partOfSpeech.find_all("span", {'class':'inflected-form'}):
                    pos1.replaceWith('')
            for pos2 in partOfSpeech.find_all("span", {'class':'luna-pronset'}):
                    pos2.replaceWith('')
            partOfSpeech = partOfSpeech.get_text().title()
            json_contents = {
                "partOfSpeech": partOfSpeech,
                "definitions": []
            }
            definitions = each.findAll(attrs={'class': 'css-1uqerbd e1hk9ate0'})
            def_list = ""
            for definition in definitions:
                def_content = definition.find(attrs={'class': 'e1q3nk1v1'})
            
                if def_content:
                    for tag in def_content.find_all("span", {'class':'luna-example'}):
                        tag.replaceWith('')
                    def_content = def_content.get_text().replace('(', '').replace(')', '').replace(':', '').strip()
                    def_content = def_content[0].upper() + def_content[1:]
                else:
                    def_content = ''
            
                try:
                    example = definition.find(attrs={'class': 'luna-example'}).text
                except:
                    example = ""

                def_list += def_content
                def_list = def_list.strip()
            if def_list == "":
                defFound = False
            else:
                json_content = {
                    "definition": def_list,
                    "example": example
                }
            if defFound:
                json_contents['definitions'].append(json_content)
                dataItems['meanings'].append(json_contents)
            else:
                pass
        if dataItems['meanings']:
            return dataItems
        else:
            suggestions = IfnotFound(word)
            return suggestions
        #return word, dataItems