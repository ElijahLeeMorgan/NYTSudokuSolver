"""
A simple web scraper that takes the current Sudoku ouzzles from the New York Times website.
This isn't the newest or prettiest implementation of Python web-scraping, but it's good to learn.
"""
from requests import get
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver import Chrome
from numpy import matrix


class SudokuScrape:
    def __init__(self) -> None:
        self._modes = ('easy', 'medium', 'hard')

    def _downloadPage(self, mode:int) -> str:
        self.puzzleURL = get('https://www.nytimes.com/puzzles/sudoku/' + self._modes[mode])
        self.puzzleURL.raise_for_status()
        return self.puzzleURL.text

    def scrape(self, mode:int) -> list[np.matrix]:
        if 3 < mode < 0:
            raise ValueError
        trimmedHTML = bs(self._downloadPage(mode), 'html.parser').find_all() #FIXME Bs4 cannot search client-rendered tags on it's own.   
        #<div data-cell="0" aria-label="6" class="su-cell selected prefilled" style="top: 0px; left: 0px; width: 51px; height: 51px;">

        puzzle = matrix()
        return puzzle


a = SudokuScrape()
a.scrape(0) #Scrape the easy puzzle.