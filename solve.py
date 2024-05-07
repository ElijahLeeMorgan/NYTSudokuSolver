from scrape import SudokuScrape
from numpy import matrix, int8, unique, isin, argwhere
from sys import exit

class sudokuSolver:
    def __init__(self, difficulty:int) -> None:
        self._setPuzzle(difficulty)

    def UI(self) -> int:
        #TODO Add a GUUI, and make CLI optional.
        #TODO Change CLI to just be system argument inputs.
        _difficulties = {'easy':0, 'medium':1, 'hard':2, 'all':3, '0':0, '1':1, '2':2, '3':3}
        self.difficulty = -1
        
        while self.difficulty <= 0:
            userinput = input("Please type which puzzle you'd like to solve.\nYour options are: easy, medium, hard, and all.\nIf you'd like to quit, type 'quit'").lower()
            if userinput in _difficulties.keys():
                self.difficulty = _difficulties[self.difficulty]
            elif userinput == 'quit':
                print("Exiting...")
                exit(0)
            else:
                print("Invalid input, please try again.\n")
        return self.difficulty
    
    def _setPuzzle(self, difficulty:int) -> bool:
        scraper = SudokuScrape()
        self.puzzle = scraper.scrape(difficulty)
        return True
    
    def _getPuzzle(self) -> matrix[int8]:
        return self.puzzle
    
    def _valueInRow(self, value:int, row:int) -> bool:
        return isin(value, self.puzzle[row, :]).any()

    def _valueInCollumn(self, value:int, col:int) -> bool:
        return isin(value, self.puzzle[:, col]).any()
    
    def _roundindex(self, row:int, col:int) -> tuple[int]:
        #Rounds the index of a cell to the top left cell index of it's box
        return (min((0,3,6), key=lambda x: abs(row - x - 1)), 
                min((0,3,6), key=lambda x: abs(col - x - 1)))

    def _valueInBox(self, value:int, row:int, col:int):
        boxPos = self._roundindex(row, col)
        submatrix = self.puzzle[boxPos[0]:boxPos[0]+3, boxPos[1]:boxPos[1]+3]
        return (submatrix == value).any()
    
    def _isValidMove(self, value:int, row:int, col:int) -> bool:
        return not self._valueInRow(value, row) \
                and not self._valueInCollumn(value, col) \
                and not self._valueInBox(value, row, col)

    def solvePuzzle(self) -> matrix[int8]:
        #If I return to this project, I'd like to use the algorithm in this paper: https://www.ams.org/notices/200904/tx090400460p.pdf
        self.puzzle = self._getPuzzle()
        emptyCells = argwhere(self.puzzle == 0)

        for cell in emptyCells:
            for value in range(1,10):
                if self._isValidMove(value, cell[0], cell[1]):
                    self.puzzle[cell[0], cell[1]] = value
                    print(self.puzzle)
                    if self.solvePuzzle().any():
                        return self.puzzle
                    self.puzzle[cell[0], cell[1]] = 0
        return self.puzzle

    def __str__(self) -> str:
        return f"Easy:\n{self.solvePuzzle(0)}\nMedium:\n{self.solvePuzzle(1)}\nHard:\n{self.solvePuzzle(3)}"

if __name__ == "__main__":
    solver = sudokuSolver(0)
    print(solver.solvePuzzle())
    exit(0)