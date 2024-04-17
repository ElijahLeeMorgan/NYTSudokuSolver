"""
A simple web scraper that takes the current Sudoku ouzzles from the New York Times website.
This isn't the newest or prettiest implementation of Python web-scraping, but it's good to learn.
"""
from requests import get
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from numpy import matrix


class SudokuScrape:
    def __init__(self) -> None:
        self._modes = ('easy', 'medium', 'hard')
        opt = webdriver.FirefoxOptions()
        opt.add_argument("--headless")
        self.driver = Firefox(options=opt)
        self.driver.start_session

    def _scrapeCells(self, mode:int) -> list[any]: #FIXME Bad typing I know, but I'm having trouble pinning down the WebElement class.
        self.driver.get('https://www.nytimes.com/puzzles/sudoku/' + self._modes[mode])
        #sudokuCells = [self.driver.find_element(By.CSS_SELECTOR, f"div.su-cell:nth-child({i})") for i in range(1,82)]
        sudokuCells = [self.driver.find_element(By.XPATH, f"/html/body/div[3]/div[2]/div[2]/div[6]/div[3]/div/div/div[1]/div/div/div/div[{i}]") for i in range(1,82)]
        sudokuCells = self._turnToSoup(sudokuCells)
        return sudokuCells
    
    def _turnToSoup(self, elements:list) -> list[str]: #FIXME Bad typing I know, but I'm having trouble pinning down the WebElement class.
        for element in elements:
            element.click()
        soup = bs(self.driver.page_source, 'html.parser')
        self.driver.quit()

        strainedSoup = [soup.find("div", attrs={"data-cell": str(i)}) for i in range(0,81)]
        #TODO continue from here.
    
        return soup


    def _soupToWaffle(self, noodles:list[str]) -> matrix[int]:
        ...

    def scrape(self, mode:int) -> matrix:
        if 3 < mode < 0:
            raise ValueError
        sudokuCells = self._scrapeCells(mode)

        puzzle = matrix([0,0,0,0]) #TODO Populate with values from scraped page.
        return puzzle


a = SudokuScrape()
a.scrape(0)