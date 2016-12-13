'''Allows to import articles from Wikipedia'''

import wikipedia

import logging

logging.basicConfig(filename='encyclopedia.log', format='[%(asctime)s] %(message)s\n\n',
                    level=logging.ERROR)

class Encyclopedia:
    '''Allows to import articles from Wikipedia'''
    
    def __init__(self, text=None, lang='ru'):
        '''Contructor
        Args:
            text: text for searching theme
            lang: wiki(text) language
        '''
        
        self.text = text
        self.lang = lang

    def set_text(self, text):
        '''Sets text'''
        self.text = text

    def set_lang(self, lang):
        '''Sets language'''
        self.lang = lang

    def get_article(self):
        '''Gets article from Wikipedia'''
        try:
        	wikipedia.set_lang(self.lang)
        	return wikipedia.page(self.text)
        except Exception as e:
        	logging.error(str(e))
        	return None

    def get_summary(self):
        '''Gets summary from Wikipedia'''
        try:
        	wikipedia.set_lang(self.lang)
        	return wikipedia.summary(self.text, sentences=3)
        except Exception as e:
        	logging.error(str(e))
        	return None

