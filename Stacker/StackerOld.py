import math
import machine
import thumby
import time

class Game:
    def __init__(self):
        self.board = [[0] * 11] * 15
        self.cameraY = 0
        self.animTick = None
        self.animFrame = 0
        self.animDir = 1
        self.playerLives = 3
        self.playerLevel = 0

    def running(self):
        return self.playerLevel < 15 and self.playerLives > 0

    def __updateAction(self):
        for col in range(11):
            if self.board[self.playerLevel][col] and (col < 2 or col > 8 or (self.playerLevel > 0 and not self.board[self.playerLevel - 1][col])):
                # TODO: Some kind of falling block animation?
                self.board[self.playerLevel][col] = 0
                self.playerLives -= 1

        if self.playerLives <= 0:
            # Game Over
            pass
        
        self.playerLevel += 1

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
        if self.animTick is None:
            self.animTick = time.ticks_ms()

        if time.ticks_diff(time.ticks_ms(), self.animTick) < 1000/15:
            return
        
        self.animTick = None
        
        row = [0] * 11
        row[self.animFrame:(self.animFrame + self.playerLives)] = [1] * self.playerLives
        self.board[self.playerLevel] = row
        
        if self.animDir > 0:
            self.animFrame += 1
            if self.animFrame >= 8:
                self.animDir = -1
        else:
            self.animFrame -= 1
            if self.animFrame <= 3 - self.playerLives:
                self.animDir = 1

    def __updateCamera(self):
        if thumby.buttonU.pressed():
            self.cameraY = min(44, self.cameraY + 1)

        if thumby.buttonD.pressed():
            self.cameraY = max(0, self.cameraY - 1)

    def update(self):
        self.__updateCamera()
        self.__updateAnimation()

        if thumby.actionJustPressed():
            self.__updateAction()
    
    def draw(self):
        thumby.display.fill(0)
        
        # static, no camera effect
        thumby.display.fillRect(14, 0, 4, thumby.DISPLAY_H, 1) # Left side-block
        thumby.display.fillRect(54, 0, 4, thumby.DISPLAY_H, 1) # Right side-block
        # /static
        
        # bottom side-block
        if self.cameraY < 4:
            thumby.display.fillRect(14, thumby.DISPLAY_H - 4 + self.cameraY, 40, 4, 1)
        # top side-block
        if self.cameraY > 40:
            thumby.display.fillRect(14, thumby.DISPLAY_H - 84 + self.cameraY, 40, 4, 1)
        
        # scrubber
        scrubberHeight = 40 * 44 / 84
        scrubberOffset = (40 - scrubberHeight) * self.cameraY / 44
        thumby.display.fillRect(thumby.DISPLAY_W - 1, int(round(thumby.DISPLAY_H - scrubberOffset - scrubberHeight)), 1, int(math.ceil(scrubberHeight)), 1)
        # /scrubber
        
        # scroll indicator
        currentRowY = thumby.DISPLAY_H - (9 + 5 * self.playerLevel) + self.cameraY
        if currentRowY < 0:
            # row is not visible (too high)
            thumby.display.drawText("^", 0, 0, 1)
        elif currentRowY + 4 > thumby.DISPLAY_H:
            # row is not visible (too low)
            thumby.display.drawText("v", 0, 32, 1)
        # /scroll indicator

        # blocks
        for row, array in enumerate(self.board):
            for col, bit in enumerate(array[2:-2]):
                if bit:
                    # regular
                    rowY = thumby.DISPLAY_H - (9 + 5 * row) + self.cameraY
                    if rowY > 0 and rowY +4 < thumby.DISPLAY_H:
                        thumby.display.fillRect(19 + 5 * col, thumby.DISPLAY_H - (9 + 5 * row) + self.cameraY, 4, 4) 

                    # mini map blocks
                    thumby.display.setPixel(thumby.DISPLAY_W - 11 + col, thumby.DISPLAY_H - (3 + row)) 
        # /blocks

        # mini-map border
        thumby.display.rect(thumby.DISPLAY_W - 13, thumby.DISPLAY_H - 19, 11, 19, 1) 

        thumby.display.update()

while True:
    game = Game()
    while game.running():
        game.update()
        game.draw()
