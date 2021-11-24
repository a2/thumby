import math
import thumby
import time

# BITMAP: width: 23, height: 12
bitmapLarge = [0,128,128,64,67,45,57,50,50,100,100,72,72,80,80,32,32,64,64,128,128,0,0,3,2,2,2,2,14,10,10,10,10,10,6,6,6,6,6,6,2,2,2,2,3,2]

# BITMAP: width: 12, height: 7
bitmapSmol = [32,48,43,101,106,106,116,52,40,48,48,32]

# BITMAP: width: 12, height: 7
bitmapSmolFlip = [32,48,48,40,52,116,106,106,101,43,48,32]

def intro_animation():
    # intro animation
    start = time.ticks_ms()
    spriteW = 12
    spriteH = 7
    spriteX = -spriteW
    spriteY = 0.0
    textY = -24.0
    blinkTimer = 0
    flip = False

    while True:
        if thumby.buttonA.justPressed():
            return

        t0 = time.ticks_ms()

        # draw
        bitmap = bitmapSmolFlip if flip else bitmapSmol
        thumby.display.fill(0)
        if spriteY < thumby.DISPLAY_H:
            thumby.display.blit(bitmap, spriteX, int(spriteY), spriteW, spriteH)
        thumby.display.drawText("tiny plen", 0, int(textY))
        if blinkTimer > 60:
            thumby.display.drawText("press A", 8, thumby.DISPLAY_H - 8)
        thumby.display.update()

        # update
        # move plane down
        if spriteY < thumby.DISPLAY_H:
            spriteY += 1/8
            if flip: # move left
                spriteX -= 1
                if spriteX + spriteW < 0: # change direction
                    flip = False
            else: # move right
                spriteX += 1
                if spriteX > thumby.DISPLAY_W: # change direction
                    flip = True
        # move text down
        if textY < (thumby.DISPLAY_H - 8) // 2:
            textY += 1/8
        else:
            blinkTimer = (blinkTimer + 1) % 120

        # sleep (until 120 fps)
        t1 = time.ticks_ms()
        diff = time.ticks_diff(t0, t1)
        time.sleep_ms(1000 // 120 - diff)

while True:
    intro_animation()
