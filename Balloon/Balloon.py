# Balloon
# by a2

import machine
import math
import thumby
import time

W = thumby.DISPLAY_W
H = thumby.DISPLAY_H

balloonCache = []
shineCache = []


def drawBalloon(x0, y0, radius, color=1):
    global balloonCache
    global shineCache

    if not balloonCache:
        for degrees in range(-90, 91, 10):  # 91 to go "through" 90
            theta = math.radians(degrees)
            r = (1 + 0.375 / math.cosh(2.75 * (theta + math.pi / 2))) / 1.375
            x = r * math.cos(theta)
            y = r * math.sin(theta)
            balloonCache.append((x, y))

            if degrees >= 20 and degrees < 60:
                shineCache.append((0.5 * math.cos(theta), 0.5 * math.sin(theta)))

    # shine is distinct from the border
    if radius >= 7:
        shine = [(round(x * radius), round(y * radius)) for x, y in shineCache]
        for i in range(len(shine) - 1):
            (x1, y1) = shine[i]
            (x2, y2) = shine[i + 1]
            thumby.display.drawLine(x0 + x1, y0 - y1, x0 + x2, y0 - y2, color)

    balloon = [(round(x * radius), round(y * radius)) for x, y in balloonCache]
    for i in range(len(balloon) - 1):
        (x1, y1) = balloon[i]
        (x2, y2) = balloon[i + 1]
        thumby.display.drawLine(x0 - x1, y0 - y1, x0 - x2, y0 - y2, color)
        thumby.display.drawLine(x0 + x1, y0 - y1, x0 + x2, y0 - y2, color)


def main():
    time.sleep_ms(1)  # Why does this fix everything?
    thumby.display.fill(0)
    thumby.display.drawText("Balloon", 8, 0, 1)
    thumby.display.drawText("Press A+B", 0, 32, 1)
    thumby.display.update()

    # Wait for the user to start
    while thumby.actionPressed():
        pass
    while not thumby.actionPressed():
        pass

    size = 1
    t0 = time.ticks_ms()
    d0 = 5 * 1000
    waitingForA = True

    # Repeat for 5 seconds
    while time.ticks_diff(time.ticks_ms(), t0) < d0:
        thumby.display.fill(0)
        thumby.display.drawLine(
            0, H - 1, W - int(W * time.ticks_diff(time.ticks_ms(), t0) / d0), H - 1, 1
        )
        thumby.display.drawText(str(size), 0, H - 10, 1)
        drawBalloon(W // 2 - 1, H - 5 - size, size, 1)
        thumby.display.update()

        if waitingForA:
            if thumby.buttonA.pressed() and not thumby.buttonB.pressed():
                waitingForA = False
                size += 1
        else:
            if thumby.buttonB.pressed() and not thumby.buttonA.pressed():
                waitingForA = True
                size += 1

    t1 = time.ticks_ms()
    d1 = 7 * 1000

    dx = 0
    dy = 0

    # Repeat for 7 seconds
    while time.ticks_diff(time.ticks_ms(), t1) < d1:
        thumby.display.fill(0)
        drawBalloon(W // 2 - 1 + int(dx), H - 5 - size + dy, size, 1)
        thumby.display.drawLine(
            W // 2 - 1 + int(dx),
            H - 5 - size + dy + size,
            W // 2 - 1 + int(dx),
            H + 10 + dy,
            1,
        )

        x = int(W / 2) - 4
        if size >= 10:
            x -= 4
        thumby.display.drawText(str(size), x, max(H + 10 + 4 + dy, H // 2 - 4), 1)
        thumby.display.update()

        dx += math.cos(math.pi * dy * 4 / 70) / 2
        dy -= 1
        time.sleep_ms(100)

    # Ask to play again
    thumby.display.fill(0)
    thumby.display.drawText("Again?", 12, 0, 1)
    thumby.display.drawText("B:N A:Y", 8, 32, 1)
    thumby.display.update()

    while not thumby.actionPressed():
        pass

    if thumby.buttonB.pressed():
        while thumby.buttonB.pressed():
            pass
        machine.reset()


while True:
    main()
