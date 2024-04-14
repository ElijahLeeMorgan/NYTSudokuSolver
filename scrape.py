"""
This probably isn't the newest or prettiest implementation of Python web-scraping, but for my purposes it's good enougth.
Tutorial:
https://automatetheboringstuff.com/2e/chapter12/
"""

# Well there goes one idea: https://stackoverflow.com/a/1732454/1893164/
from requests import get
from bs4 import BeautifulSoup

class SuddokuScrape:
    def __init__(self) -> None:
        self.puzzleHTML = tuple(get('https://www.nytimes.com/puzzles/sudoku/' + i) for i in ('easy', 'medium', 'hard'))
        self._downloadPages()


    def _downloadPages(self) -> None:
        for request in self.puzzleHTML:
            request.raise_for_status()

            fileName = request.url.removeprefix('https://www.nytimes.com/puzzles/sudoku/') + '.txt'
            webpage = open(fileName, 'wb')
            
            for chunk in request.iter_content():
                webpage.write(chunk)
            
            webpage.close()
        return None
    



a = SuddokuScrape()
a._downloadPages()