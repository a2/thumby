from collections import namedtuple
import math
import thumby
import time

Sprite = namedtuple("Sprite", ["data", "angle", "w", "h"])

sprites = [
    Sprite(data=(16, 24, 24, 20, 20, 26, 58, 49, 53, 27, 24, 16), angle=-90.0, w=12, h=6),
    Sprite(data=(64, 96, 80, 72, 52, 42, 41, 39, 24, 16, 16), angle=-67.5, w=11, h=7),
    Sprite(data=(64, 176, 76, 83, 41, 38, 20, 12, 8), angle=-45.0, w=9, h=8),
    Sprite(data=(255, 161, 90, 38, 18, 10, 6, 1, 0, 0, 0, 0, 0, 0), angle=-22.5, w=7, h=9),
    Sprite(data=(7, 25, 98, 154, 98, 25, 7), angle=0.0, w=7, h=8),
    Sprite(data=(6, 10, 18, 38, 90, 161, 255, 0, 0, 0, 0, 0, 0, 1), angle=22.5, w=7, h=9),
    Sprite(data=(8, 12, 20, 38, 41, 83, 76, 176, 64), angle=45.0, w=9, h=8),
    Sprite(data=(16, 16, 24, 39, 41, 42, 52, 72, 80, 96, 64), angle=67.5, w=11, h=7),
    Sprite(data=(16, 24, 27, 53, 49, 58, 26, 20, 20, 24, 24, 16), angle=90.0, w=12, h=6)
]

# intro animation
def intro_animation():
    spriteX = 0.0
    spriteY = -10.0
    tStart = time.ticks_ms()
    titleEnd = 0

    while not thumby.buttonA.justPressed():
        t0 = time.ticks_ms()

        # update
        tdiff = time.ticks_diff(t0, tStart) / 1000
        if spriteY < thumby.DISPLAY_H:
            angleDesired = 2 * math.sin(tdiff) / math.pi * 180.0
            sprite = sprites[0]
            for candidate in sprites[1:]:
                if abs(candidate.angle - angleDesired) < abs(sprite.angle - angleDesired):
                    sprite = candidate

            angleSprite = sprite.angle * math.pi / 180.0
            spriteX += 0.64 * math.sin(angleSprite)
            spriteY += 0.05 + math.cos(angleSprite)

        # draw
        thumby.display.fill(0)

        title = "lil plane"
        titleEnd = max(titleEnd, int((spriteX / 8) + max((spriteY - 20) / 8, 0)))

        if spriteY + sprite.h / 2 < thumby.DISPLAY_H:
            thumby.display.blit(sprite.data, int(spriteX), int(spriteY + sprite.h / 2), sprite.w, sprite.h)
        elif int(tdiff) % 2 == 0:
            thumby.display.drawText("start", 16, 32)

        thumby.display.drawText(title[:titleEnd], 0, 16)
        thumby.display.update()

        # sleep (until 60 fps)
        t1 = time.ticks_ms()
        diff = time.ticks_diff(t0, t1)
        time.sleep_ms(1000 // 60 - diff)

while True:
    intro_animation()
