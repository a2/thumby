import time
import thumby
import math

# BITMAP: width: 23, height: 12
bitmapLarge = [0,128,128,64,67,45,57,50,50,100,100,72,72,80,80,32,32,64,64,128,128,0,0,
           3,2,2,2,2,14,10,10,10,10,10,6,6,6,6,6,6,2,2,2,2,3,2]

# BITMAP: width: 12, height: 7
bitmapSmol = [32,48,43,101,106,106,116,52,40,48,48,32]

# BITMAP: width: 12, height: 7
bitmapSmolFlip = [32,48,48,40,52,116,106,106,101,43,48,32]

small = True

start = time.ticks_ms()
while True:
    t0 = time.ticks_ms()
    diff = time.ticks_diff(t0, start)
    aniX = -(thumby.DISPLAY_W + 25) + (diff // 30)

    bobRate = 250 # ms
    bobRange = 2
    bobOffset = 2 * math.sin(t0 / 250)

    sprite = bitmapSmol if small else bitmapLarge
    spriteW = 12 if small else 23
    spriteH = 7 if small else 12
    spritePad = 4
    spriteX = aniX + thumby.DISPLAY_W + spritePad
    spriteY = int(round((thumby.DISPLAY_H/2) - (spriteH/2) + bobOffset))

    thumby.display.fill(0)
    thumby.display.drawText("tiny plen", min(0, aniX), (thumby.DISPLAY_H - 8) // 2, 1)

    if spriteX - spritePad < thumby.DISPLAY_W:
        thumby.display.blit(sprite, spriteX, spriteY, spriteW, spriteH)
    elif aniX % 32 < 16:
        thumby.display.drawText("(A)", (thumby.DISPLAY_W - 24) // 2, thumby.DISPLAY_H - 8, 1)

    thumby.display.update()
