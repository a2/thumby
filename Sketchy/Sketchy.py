import time
import thumby
import math
from collections import namedtuple

MenuItem = namedtuple("MenuItem", ("title", "action"))

class Cursor:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Screen:
    def __init__(self, w, h):
        bitmapLen = (h // 8) * w
        self._bitmap = [0] * bitmapLen 
        self._width = w
        self._height = h
        self.cursor = Cursor(0, 0)

    @property 
    def bitmap(self):
        return self._bitmap

    @property
    def width(self):
        return self._width
        
    @property
    def height(self):
        return self._height
    
    def getPixel(self, x, y):
        idx = self._width * (y // 8) + x
        bit = 1 << (y % 8)
        return 1 if self._bitmap[idx] & bit else 0

    def setPixel(self, x = -1, y = -1, color = 1):
        if x == -1:
            x = self.cursor.x
        elif x >= self.width:
            return
        if y == -1:
            y = self.cursor.y
        elif y >= self.height:
            return

        idx = self._width * (y // 8) + x
        bit = 1 << (y % 8)
        if color:
            self._bitmap[idx] |= bit
        else:
            self._bitmap[idx] &= ~bit
            
    def clear(self):
        self._bitmap = [0] * len(self._bitmap)

def update():
    global clearingScreen, cursorColor, lastBlink, lastUpdate, menu, menuSelection, menuY, menuYHidden, menuYVisible, screen

    if clearingScreen > 0:
        clearingScreen -= 1
        if clearingScreen == 0:
            screen.clear()
        return
    
    cursorColor = 1 if time.ticks_diff(lastBlink, lastUpdate) % 1000 >= 500 else 0

    if menu:
        if menuY < menuYVisible:
            menuY += 1
        if thumby.buttonB.justPressed():
            menu = False
            menuY = menuYHidden
    elif thumby.buttonA.justPressed():
        menu = True

    if menu:
        if thumby.buttonU.justPressed():
            count = len(menuItems())
            menuSelection = (menuSelection + count - 1) % count
        if thumby.buttonD.justPressed():
            menuSelection = (menuSelection + 1) % len(menuItems())
        if thumby.buttonA.justPressed():
            menuItems()[menuSelection].action()
            
            menu = False
            menuY = menuYHidden
            menuSelection = 0
    elif thumby.dpadPressed():
        screen.setPixel()

        cursor = screen.cursor
        if thumby.buttonL.pressed():
            cursor.x = max(0, cursor.x - 1)
        if thumby.buttonR.pressed():
            cursor.x = min(thumby.DISPLAY_W - 1, cursor.x + 1)
        if thumby.buttonU.pressed():
            cursor.y = max(0, cursor.y - 1)
        if thumby.buttonD.pressed():
            cursor.y = min(thumby.DISPLAY_H - 1, cursor.y + 1)

        lastBlink = lastUpdate

def noop():
    pass

def clear():
    global clearingScreen, cursorColor, screen
    clearingScreen = 10
    cursorColor = 0

def menuItems():
    return [
        MenuItem("Menu", noop),
        MenuItem("Clear", clear),
    ]

def draw():
    thumby.display.fill(0)

    x = 0 if clearingScreen <= 0 else (5 * abs((clearingScreen - 1) % 4 - 2) - 5)
    thumby.display.blit(screen.bitmap, x, 0, thumby.DISPLAY_W, thumby.DISPLAY_H)

    if menu:
        thumby.display.fillRect(0, menuY, thumby.DISPLAY_W, 11, 0)
        thumby.display.rect(0, menuY, thumby.DISPLAY_W, 11, 1)
        thumby.display.drawText(menuItems()[menuSelection].title, 1, menuY + 2)
    elif clearingScreen <= 0:
        thumby.display.setPixel(screen.cursor.x, screen.cursor.y, cursorColor)

    thumby.display.update()

def main():
    global clearingScreen, cursorColor, lastBlink, lastUpdate, menu, menuSelection, menuY, menuYHidden, menuYVisible, screen

    clearingScreen = -1
    screen = Screen(thumby.DISPLAY_W, thumby.DISPLAY_H)
    lastBlink = -1
    cursorColor = 1
    menu = False
    menuSelection = 0
    menuYHidden = -10
    menuYVisible = 0
    menuY = menuYHidden

    while True:
        lastUpdate = time.ticks_ms()
        update()
        draw()
        time.sleep_ms(1000 // 30 - time.ticks_diff(time.ticks_ms(), lastUpdate))

main()
