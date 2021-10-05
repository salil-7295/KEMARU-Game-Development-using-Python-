import pygame, sys

from grid_developer import generate_grid
from settings import *
from kemaru_puzzles import getPuzzleIntVals, getPuzzleBlocks, getPuzzleSol
from helper import Helper


class App:
    def __init__(self):
        pygame.init()

        # Display KEMARU on game interface
        pygame.display.set_caption("KEMARU")

        # create the display surface object of specific dimension(X, Y).
        self.window = pygame.display.set_mode((WIDTH, HEIGHT + 100))

        # create a font object.
        self.font = pygame.font.SysFont(font, fontSize)

        self.running = True
        self.grid = None
        self.grid_blocks = None
        self.helper = None
        self.initPuzzle()

        # to store the arranged cells(x,y) to genearte grid
        self.blockIndex = []

        # to store the static cell values and to make not editable
        self.lockedCells = []

        # to store the cells entered incorrect and to produce them on all cells entered
        self.errorCells = []

        # to indicate the selected cell
        self.selected = None

        # to store the mouse position
        self.mousePos = None

        # to indicate whether all the cells are done or not
        self.finished = False

        # to indicate whether  the current puzzle is the second one or not
        self.second_puzzle_flag = False

    def run(self, puzzle_no):

        # NOte : next puzzle load only if the first completed sucessfully
        message = 'Complete current puzzle to load next puzzle'
        if puzzle_no == 2:
            message = 'Once you comlete the puzzle, the game quits '
            self.second_puzzle_flag = True

        # create a text suface object,on which text is drawn on it.
        self.messageTextFontStyle = self.font.render(message, True, ERROR_RED)

        # create a rectangular object for the text surface object
        self.messageTextInfoRect = self.messageTextFontStyle.get_rect()

        # set the center of the rectangular object.
        self.messageTextInfoRect.center = (300, HEIGHT - 10)

        # create a text surface object on which text is drawn on it.
        self.puzzleNoFontStyle = self.font.render('Puzzle ' + str(puzzle_no), True, ERROR_RED)

        # create a rectangular object for the text surface object
        self.puzzleNoInfoRect = self.puzzleNoFontStyle.get_rect()

        # set the center of the rectangular object.
        self.puzzleNoInfoRect.center = (300, HEIGHT - 550)

        # retrieves the puzzle from kemaru puzzles w.r.t to the given puzzle no.
        self.puzzle = self.getPuzzle(puzzle_no)

        # stores the static cell values to lockedCells
        self.setLockedCells()

        # stores the arranged cells to blockIndex
        self.getBlocksIndex()

        while self.running:
            # for events
            self.events()

            # to update the changes through out the program
            self.update()

            # draws the grid, cells,
            self.draw()

        pygame.quit()
        sys.exit()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # User Clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                selected = self.mouseOnGrid()
                if selected:
                    self.selected = selected
                else:
                    self.selected = None

            # User Types
            if event.type == pygame.KEYDOWN:
                if self.selected != None and self.selected not in self.lockedCells:
                    if self.isInt(event.unicode):
                        self.grid[self.selected[1]][self.selected[0]] = int(event.unicode)
                        x = int(str(self.sol[self.selected[1]][self.selected[0]]))
                        errorIndex = (self.selected[0], self.selected[1])
                        if x != int(event.unicode):
                            if errorIndex not in self.errorCells:
                                self.errorCells.append(errorIndex)
                        if x == int(event.unicode) or int(event.unicode) == 0:
                            if errorIndex in self.errorCells:
                                self.errorCells.remove(errorIndex)

    def update(self):
        # mouse position
        self.mousePos = pygame.mouse.get_pos()

    def draw(self):
        self.window.fill(WHITE)
        self.window.blit(self.messageTextFontStyle, self.messageTextInfoRect)  # adds the rendered text to screen
        self.window.blit(self.puzzleNoFontStyle, self.puzzleNoInfoRect)  # adds the rendered text to screen

        if self.allCellsDone():
            self.finished = True
            if not self.errorCells:
                if self.second_puzzle_flag == True:
                    self.running = False
                else:
                    # if puzzle 1 is correct move to next puzzle
                    app = App()
                    app.run(2)

            # indicates the incorrect cells
            self.shadeErrorCells(self.window, self.errorCells)

        if self.selected:
            # indicates the current selected cell
            self.drawSelection(self.window, self.selected)

        # indicates the  locked cells of current puzzle
        self.shadeLockedCells(self.window, self.lockedCells)

        # draws numbers to  (locked)cells  that are given
        self.drawNumbers(self.window)

        # develops grids  from arranged blockIndex
        self.developGridsFromArrangedBlockIndexes(self.window, self.blockIndex)

        # draws the simple 9 *9 grid
        self.drawGrid(self.window)

        pygame.display.update()

    def drawGrid(self, window):
        pygame.draw.rect(window, BLACK, (gridPos[0], gridPos[1], WIDTH - 150, HEIGHT - 150), 2)
        for x in range(NO_OF_CELLS):
            pygame.draw.line(window, BLACK, (gridPos[0] + (x * cellSize), gridPos[1]),
                             (gridPos[0] + (x * cellSize), gridPos[1] + 450))
            pygame.draw.line(window, BLACK, (gridPos[0], gridPos[1] + (x * cellSize)),
                             (gridPos[0] + 450, gridPos[1] + (x * cellSize)))

    def mouseOnGrid(self):
        if self.mousePos[0] < gridPos[0] or self.mousePos[1] < gridPos[1]:
            return False
        if self.mousePos[0] > gridPos[0] + gridSize or self.mousePos[1] > gridPos[1] + gridSize:
            return False
        return ((self.mousePos[0] - gridPos[0]) // cellSize, (self.mousePos[1] - gridPos[1]) // cellSize)

    def drawSelection(self, window, position):
        pygame.draw.rect(window, SELECTION_COLOR, (
            (position[0] * cellSize) + gridPos[0], (position[1] * cellSize) + gridPos[1], cellSize, cellSize))

    def drawNumbers(self, window):
        for yindx, row in enumerate(self.grid):
            for xindx, num in enumerate(row):
                if num != 0:
                    pos = [(xindx * cellSize) + gridPos[0], (yindx * cellSize) + gridPos[1]]
                    self.textToScreen(window, str(num), pos)

    def textToScreen(self, window, text, pos):
        font = self.font.render(text, False, BLACK)

        fontWidth = font.get_width()
        pos[0] += (cellSize - fontWidth) // 2
        fontHeight = font.get_height()
        pos[1] += (cellSize - fontHeight) // 2

        window.blit(font, pos)

    def shadeLockedCells(self, window, locked):
        for cell in locked:
            pygame.draw.rect(window, ASH,
                             (cell[0] * cellSize + gridPos[0], cell[1] * cellSize + gridPos[1], cellSize, cellSize))

    def isInt(self, stringNumber):
        try:
            int(stringNumber)
            return True
        except:
            return False

    def setLockedCells(self):
        for yindx, row in enumerate(self.grid):
            for xindx, num in enumerate(row):
                if num != 0:
                    # setting locked cells from originalboard
                    self.lockedCells.append((xindx, yindx))

    def getBlocksIndex(self):
        self.helper = Helper(self.grid_blocks, self.grid)
        blockIndex = [None] * self.helper.getBlockNumber()
        for yindx, row in enumerate(self.grid_blocks):
            for i in range(1, self.helper.getBlockNumber() + 1):
                if yindx % 2 == 0:
                    for xindx, num in enumerate(row):
                        if num == i:
                            if blockIndex[i - 1] is None:
                                blockIndex[i - 1] = [(xindx, yindx)]
                            else:
                                blockIndex[i - 1].append((xindx, yindx))
                else:
                    for xindx, num in reversed(list(enumerate(row))):
                        if num == i:
                            if blockIndex[i - 1] is None:
                                blockIndex[i - 1] = [(xindx, yindx)]
                            else:
                                blockIndex[i - 1].append((xindx, yindx))
        self.blockIndex = blockIndex

    def shadeErrorCells(self, window, errorCells):
        for cell in errorCells:
            pygame.draw.rect(window, ERROR_RED,
                             (cell[0] * cellSize + gridPos[0], cell[1] * cellSize + gridPos[1], cellSize, cellSize))

    def developGridsFromArrangedBlockIndexes(self, window, blockIndex):
        # for no. of blocks indexes
        # contains the corresponding
        # blocks cells indexes
        for block in blockIndex:
            generate_grid(window, block)

    # to check wheteher all cell
    # contains some numeric value (not zero)
    def allCellsDone(self):
        for row in self.grid:
            for number in row:
                if number == 0:
                    return False
        return True

    def getPuzzle(self, puzzle_no):
        self.grid = getPuzzleIntVals(puzzle_no)
        self.grid_blocks = getPuzzleBlocks(puzzle_no)
        self.sol = getPuzzleSol(puzzle_no)

    def initPuzzle(self):
        self.grid = getPuzzleIntVals(0)
        self.grid_blocks = getPuzzleBlocks(0)
        self.sol = getPuzzleSol(0)
