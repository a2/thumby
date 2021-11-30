from collections import namedtuple
import math
import random
import thumby
import time

Sprite = namedtuple("Sprite", ["data", "angle", "w", "h"])
Block = namedtuple("Block", ["x", "y", "w", "h"])

sprites = (
    Sprite(data=(16, 24, 24, 20, 20, 26, 58, 49, 53, 27, 24, 16), angle=-90.0, w=12, h=6),
    Sprite(data=(64, 96, 80, 72, 52, 42, 41, 39, 24, 16, 16), angle=-67.5, w=11, h=7),
    Sprite(data=(64, 176, 76, 83, 41, 38, 20, 12, 8), angle=-45.0, w=9, h=8),
    Sprite(data=(255, 161, 90, 38, 18, 10, 6, 1, 0, 0, 0, 0, 0, 0), angle=-22.5, w=7, h=9),
    Sprite(data=(7, 25, 98, 154, 98, 25, 7), angle=0.0, w=7, h=8),
    Sprite(data=(6, 10, 18, 38, 90, 161, 255, 0, 0, 0, 0, 0, 0, 1), angle=22.5, w=7, h=9),
    Sprite(data=(8, 12, 20, 38, 41, 83, 76, 176, 64), angle=45.0, w=9, h=8),
    Sprite(data=(16, 16, 24, 39, 41, 42, 52, 72, 80, 96, 64), angle=67.5, w=11, h=7),
    Sprite(data=(16, 24, 27, 53, 49, 58, 26, 20, 20, 24, 24, 16), angle=90.0, w=12, h=6),
)

# returns the sprite whose angle is closest to the argument
def sprite_for_angle(angle):
    sprite = sprites[0]
    for candidate in sprites[1:]:
        if abs(candidate.angle - angle) < abs(sprite.angle - angle):
            sprite = candidate
    return sprite


# intro animation
def intro_animation():
    spriteX = 7.0
    spriteY = 2.0
    timer = 0

    while not thumby.buttonA.justPressed():
        timer += 1
        t0 = time.ticks_ms()

        # update
        angleDesired = 90 * math.sin(timer / 12)
        sprite = sprite_for_angle(angleDesired)
        if spriteY - sprite.h / 2 < thumby.DISPLAY_H:
            angleSprite = (90 - sprite.angle) * math.pi / 180.0
            spriteX += 2 * math.cos(angleSprite)
            spriteY += 0.1 + 2 * math.sin(angleSprite)

        # draw
        thumby.display.fill(0)

        if spriteY - sprite.h / 2 < thumby.DISPLAY_H:
            thumby.display.blit(sprite.data, int(spriteX - sprite.w / 2), int(spriteY - sprite.h / 2), sprite.w, sprite.h)
        elif int(timer / 30) % 2 == 0:
            thumby.display.drawText("start", 16, 32)

        title = "TinyPlane"
        titleEnd = timer // 5
        thumby.display.drawText(title[:titleEnd], 0, 16)

        thumby.display.update()

        # sleep (until 30 fps)
        t1 = time.ticks_ms()
        diff = time.ticks_diff(t0, t1)
        time.sleep_ms(1000 // 30 - diff)


def game():
    score = 0
    cameraY = 0.0
    spriteX = 0.0
    spriteY = 2.0
    spriteA = 90.0

    blockH = 5
    blockGap = 20
    blockMinW = 20
    blockMaxW = thumby.DISPLAY_W - 20
    blocks = [Block(x=0, y=20, w=thumby.DISPLAY_W // 2, h=blockH)]

    while True:
        t0 = time.ticks_ms()

        # update sprite
        if thumby.buttonL.pressed():
            spriteA = max(-90, spriteA - 45 / 4)
        if thumby.buttonR.pressed():
            spriteA = min(90, spriteA + 45 / 4)

        sprite = sprite_for_angle(spriteA)
        angle = (90 - sprite.angle) * math.pi / 180.0
        spriteX += math.cos(angle)
        dy = 0.1 + 2 * math.sin(angle)
        spriteY += dy
        if spriteY >= int(20 - sprite.h / 2 + 0.5):
            cameraY += dy

        if spriteX <= 0:
            spriteX = 0
            spriteA = 0
        elif spriteX >= thumby.DISPLAY_W:
            spriteX = thumby.DISPLAY_W
            spriteA = 0

        # update blocks
        for block in blocks:
            if block.y + block.h < cameraY:
                score += 1
                blocks.remove(block)
            else:
                withinX = (spriteX + 2) >= block.x and (spriteX - 2) <= block.x + block.w
                withinY = (spriteY + 2) >= block.y and (spriteY - 2) <= block.y + block.h
                if withinX and withinY:
                    # game over
                    return

        # add new blocks
        lastBlock = blocks[-1]
        while lastBlock.y + lastBlock.h < cameraY + thumby.DISPLAY_H:
            dx = random.randint(-10, 10)
            x = 0
            y = lastBlock.y + lastBlock.h + blockGap
            w = min(blockMaxW, max(blockMinW, lastBlock.x + dx))

            if lastBlock.x == 0:
                w = min(blockMaxW, max(blockMinW, thumby.DISPLAY_W - lastBlock.w + dx))
                x = thumby.DISPLAY_W - w

            lastBlock = Block(x, y, w, blockH)
            blocks.append(lastBlock)

        # draw
        thumby.display.fill(0)
        thumby.display.blit(sprite.data, int(spriteX - sprite.w / 2), int(spriteY - sprite.h / 2 - cameraY), sprite.w, sprite.h)

        for block in blocks:
            x, y, w, h = block

            # extend outer edge beyond screen
            if x == 0:
                x -= 1
                w += 1
            if x + w == thumby.DISPLAY_W:
                w += 1

            thumby.display.rect(x, int(y - cameraY), w, h, 1)

        thumby.display.drawText(str(score), 0, 0)
        thumby.display.update()

        # sleep (until 30 fps)
        t1 = time.ticks_ms()
        diff = time.ticks_diff(t0, t1)
        time.sleep_ms(1000 // 30 - diff)


while True:
    intro_animation()
    game()
