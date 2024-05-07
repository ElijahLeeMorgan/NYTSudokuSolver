"""
A simple web scraper that takes the current Sudoku puzzles from the New York Times website.
This isn't the newest or prettiest implementation of Python web-scraping, but it's good to learn.
"""
from requests import get
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from numpy import matrix, empty, int8

class SudokuScrape:
    def __init__(self) -> None:
        self._modes = ('easy', 'medium', 'hard')
        opt = webdriver.FirefoxOptions()
        opt.add_argument("--headless")
        self.driver = Firefox(options=opt)
        self.driver.start_session

    def _scrapeCells(self, mode:int) -> list[any]: #FIXME Unsafe typing I know, but I'm having trouble pinning down the WebElement class.
        self.driver.get('https://www.nytimes.com/puzzles/sudoku/' + self._modes[mode])
        sudokuCells = [self.driver.find_element(By.XPATH, f"/html/body/div[3]/div[2]/div[2]/div[6]/div[3]/div/div/div[1]/div/div/div/div[{i}]") for i in range(1,82)]
        sudokuCells = self._turnToSoup(sudokuCells)
        sudokuCells = self._soupToMatrix(sudokuCells)
        return sudokuCells
    
    def _turnToSoup(self, elements:list) -> list[str]: #FIXME Bad typing I know, but I'm having trouble pinning down the WebElement class.
        for element in elements:
            element.click()
        soup = bs(self.driver.page_source, 'html.parser')
        self.driver.quit()
        return [soup.find("div", attrs={"data-cell": str(i)}) for i in range(0,81)]

    def _soupToMatrix(self, elements:list[str]) -> matrix[int8]:
        strConvert = {str(i):i for i in range(1,10)}
        strConvert["empty"] = 0
        puzzle = empty((9,9), int8)

        for element in elements:
            if element.has_attr("aria-label"):
                index = elements.index(element)
                value = strConvert[element["aria-label"]]
                puzzle[index // 9][index % 9] = value
            else:
                raise ValueError
        return puzzle

    def scrape(self, mode:int) -> matrix[int8]:
        if 3 < mode <= 0:
            raise ValueError
        return self._scrapeCells(mode)