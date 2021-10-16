# Stacker
# by a2

import machine
import math
import random
import thumby
import time

class FallingBlock:
    def __init__(self, column, row, endRow):
        self.column = column
        self.row = row
        self.endRow = endRow

    @property
    def landed(self):
        return self.row <= self.endRow

class Game:
    def __init__(self):
        self.board = [[0] * 11] * 15
        self.animTick = 0
        self.animFrame = 0
        self.animDir = 1
        self.animGameOver = False
        self.playerLives = 3
        self.playerLevel = 0
        self.fallingBlocks = []
        self.fallingFinishDelay = None

    @property
    def running(self):
        if self.fallingBlocks:
            return True
        return self.playerLevel < 15 and self.playerLives > 0

    def __updateAction(self):
        for col in range(11):
            if self.board[self.playerLevel][col] and (col < 2 or col > 8 or (self.playerLevel > 0 and not self.board[self.playerLevel - 1][col])):
                # Add falling block if column is in visible range (2 to 8)
                if col >= 2 and col <= 8:
                    endRow = 0
                    while self.board[endRow][col]:
                        endRow += 1
                    self.fallingBlocks.append(FallingBlock(col, self.playerLevel, endRow))

                self.board[self.playerLevel][col] = 0
                self.playerLives -= 1

        if self.playerLives <= 0:
            # Game Over
            for fallingBlock in self.fallingBlocks:
                fallingBlock.endRow = fallingBlock.row
            
            self.animGameOver = True

            for row in range(self.playerLevel, -1, -1):
                for col in range(2, 9):
                    if self.board[row][col]:
                        self.fallingBlocks.append(FallingBlock(col, row, -1))
                        self.board[row][col] = 0
        
        self.playerLevel += 1
        self.animFrame = random.randrange(8)
        self.animDir = random.randrange(-1, 1, 2)

        if self.playerLevel == 15:
            # Win Grand Prize?
            pass

        # Reduce player's lives to increase difficulty
        if self.playerLevel > 2 and self.playerLevel <= 5:
            if self.playerLives > 2:
                self.playerLives = 2
        elif self.playerLevel > 8 and self.playerLevel <= 11:
            if self.playerLives > 1:
                self.playerLives = 1

    def __updateAnimation(self):
        move = False
        
        self.animTick += 1
        if self.playerLevel < 3:
            move = self.animTick > 7
        elif self.playerLevel < 6:
            move = self.animTick > 6
        elif self.playerLevel < 9:
            move = self.animTick > 5
        elif self.playerLevel < 12:
            move = self.animTick > 4
        else:
            move = self.animTick > 3
        
        if move and self.playerLevel < 15:
            self.animTick = 0
            
            if self.animDir > 0:
                self.animFrame += 1
                if self.animFrame >= 8:
                    self.animDir = -1
            else:
                self.animFrame -= 1
                if self.animFrame <= 3 - self.playerLives:
                    self.animDir = 1

            row = [0] * 11
            if not self.fallingBlocks:
                row[self.animFrame:(self.animFrame + self.playerLives)] = [1] * self.playerLives
            self.board[self.playerLevel] = row
        
        if self.fallingBlocks:
            if self.animGameOver and self.fallingBlocks:
                fallingBlock = self.fallingBlocks[-1]
                if fallingBlock.row > fallingBlock.endRow:
                    fallingBlock.row -= 1
                else:
                    del self.fallingBlocks[-1]
            else:
                for fallingBlock in self.fallingBlocks:
                    if fallingBlock.row > fallingBlock.endRow:
                        fallingBlock.row -= 1

            # Have all blocks landed?
            if all(fallingBlock.landed for fallingBlock in self.fallingBlocks):
                if self.fallingFinishDelay is None:
                    self.fallingFinishDelay = 28
                elif self.fallingFinishDelay > 0:
                    self.fallingFinishDelay -= 1
                else:
                    self.fallingFinishDelay = None
                    self.fallingBlocks = []

    def update(self):
        self.__updateAnimation()

        if not self.fallingBlocks and thumby.actionJustPressed():
            self.__updateAction()
    
    def __drawBlock(self, column, row):
        thumby.display.fillRect(29 + 2 * column, thumby.DISPLAY_H - 7 - 2 * row, 2, 2) 
    
    def drawOnce(self):
        thumby.display.fill(0)
        
        # Draws checkerboard background
        # for x in range(thumby.DISPLAY_W):
        #     for y in range(thumby.DISPLAY_H):
        #         if (x ^ y) & 1 == 0:
        #             thumby.display.setPixel(x, y, 1)
        
        thumby.display.fillRect(25, 1, 22, 38, 1)

    def draw(self):
        thumby.display.fillRect(27, 3, 18, 34, 0)

        for row, array in enumerate(self.board):
            for col, bit in enumerate(array[2:-2]):
                if bit:
                    self.__drawBlock(col, row)

        if self.animGameOver or self.fallingFinishDelay is None or self.fallingFinishDelay % 8 >= 4:
            for fallingBlock in self.fallingBlocks:
                if fallingBlock.row >= 0: # Game over falls have `endRow == -1`
                    # Subtract 2 from column because column includes the 0,1 hidden columns
                    self.__drawBlock(fallingBlock.column - 2, fallingBlock.row) 

        thumby.display.update()

while True:
    game = Game()
    game.drawOnce()

    while game.running:
        start = time.ticks_ms()
        game.update()
        duration = time.ticks_diff(time.ticks_ms(), start)
        time.sleep_ms(1000//60 - duration)
        game.draw()
