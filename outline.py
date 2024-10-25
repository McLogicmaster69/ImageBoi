from PIL import Image
from pynput.mouse import Button, Controller
from ImageBoiClasses import SelectableColor, IndexInfo
import keyboard as kybrd
import time
import math

TOPLEFT = (665, 334)
BOTTOMRIGHT = (1574, 842)
WIDTH = BOTTOMRIGHT[0] - TOPLEFT[0]
HEIGHT = BOTTOMRIGHT[1] - TOPLEFT[1]

colors = [\
    SelectableColor(0, 0, 0, 517, 423, 1),\
    SelectableColor(102, 102, 102, 566, 423, 2),\
    SelectableColor(0, 80, 205, 608, 423, 1),\
    SelectableColor(255, 255, 255, 517, 474, 1),\
    SelectableColor(170, 170, 170, 566, 474, 2),\
    SelectableColor(38, 201, 255, 608, 474, 1),\
    SelectableColor(1, 116, 32, 517, 520, 1.5),\
    SelectableColor(153, 0, 0, 566, 520, 1),\
    SelectableColor(150, 65, 18, 608, 520, 1),\
    SelectableColor(17, 176, 60, 517, 559, 1),\
    SelectableColor(255, 0, 19, 566, 559, 1),\
    SelectableColor(255, 120, 41, 608, 559, 1),\
    SelectableColor(176, 112, 28, 517, 606, 1),\
    SelectableColor(153, 0, 78, 566, 606, 1),\
    SelectableColor(203, 90, 87, 608, 606, 1),\
    SelectableColor(255, 193, 38, 517, 661, 1),\
    SelectableColor(255, 0, 143, 566, 661, 1),\
    SelectableColor(254, 175, 168, 608, 661, 1),\
]

mouse = Controller()

def Click():
    mouse.click(Button.left)

def Move(position):
    mouse.position = position

def PositionSetup():
    print("Hover your mouse as close as you can to the top left")
    print("Do not worry if not exact, this can be changed to be made more precise")
    print("Press enter once happy with position")
    input()
    TOPLEFT = mouse.position

    print("Hover your mouse as close as you can to the bottom right")
    print("Do not worry if not exact, this can be changed to be made more precise")
    print("Press enter once happy with position")
    input()
    BOTTOMRIGHT = mouse.position

    print("You are now editing the top left position marker position x")
    print("Input how much you want to change the value by")
    print("Try and find the point where the mouse become the drawing cursor")
    print("Once found, leave the input blank and hit enter")

    while True:
        Move(TOPLEFT)
        inp = input()
        if inp == "":
            break
        else:
            try:
                nInp = int(inp)
                TOPLEFT = (TOPLEFT[0] + nInp, TOPLEFT[1])
            except:
                pass
    print("You are now editing the top left position marker position y")
    print("Input how much you want to change the value by")
    print("Try and find the point where the mouse become the drawing cursor")
    print("Once found, leave the input blank and hit enter")

    while True:
        Move(TOPLEFT)
        inp = input()
        if inp == "":
            break
        else:
            try:
                nInp = int(inp)
                TOPLEFT = (TOPLEFT[0], TOPLEFT[1] + nInp)
            except:
                pass

    print("You are now editing the bottom right position marker position x")
    print("Input how much you want to change the value by")
    print("Try and find the point where the mouse become the drawing cursor")
    print("Once found, leave the input blank and hit enter")

    while True:
        Move(BOTTOMRIGHT)
        inp = input()
        if inp == "":
            break
        else:
            try:
                nInp = int(inp)
                BOTTOMRIGHT = (BOTTOMRIGHT[0] + nInp, BOTTOMRIGHT[1])
            except:
                pass
    print("You are now editing the bottom right position marker position y")
    print("Input how much you want to change the value by")
    print("Try and find the point where the mouse become the drawing cursor")
    print("Once found, leave the input blank and hit enter")

    while True:
        Move(BOTTOMRIGHT)
        inp = input()
        if inp == "":
            break
        else:
            try:
                nInp = int(inp)
                BOTTOMRIGHT = (BOTTOMRIGHT[0], BOTTOMRIGHT[1] + nInp)
            except:
                pass

    print("Setup is complete")
    print(f"Top left position is {TOPLEFT}")
    print(f"Bottom right position is {BOTTOMRIGHT}")
    print("If you wish for these to be saved, change the values in the code to reflect the above values")


### SETUP

print("Play gartic phone at https://garticphone.com/")
print("Setting up frame")
print("Use code default values (0) run set up process (1)")

while True:
    inp = input()
    if inp == "0":
        pass
    elif inp == "1":
        PositionSetup()
    else:
        print("Invalid input")
        continue
    break

### FILE AND SCALE

print("Input the file")
filename = input()
img = Image.open(filename)
rgb_img = img.convert('RGB')
print("Input quality")
quality = int(input())

imageRatio = img.width / img.height
frameRatio = WIDTH / HEIGHT

scale = 0
startPosition = (0, 0)
xScale = img.width / WIDTH
yScale = img.height / HEIGHT

scale = xScale if xScale > yScale else yScale

drawWidth = math.floor((img.width / scale) / quality)
drawHeight = math.floor((img.height / scale) / quality)
startPosition = (math.floor(1119.5 - (drawWidth * quality) / 2), math.floor(588 - (drawHeight * quality) / 2))
Move(startPosition)

def GetPixel(x, y):
    r, g, b = rgb_img.getpixel((x, y))
    return (r, g, b)

### GENERATE BLACK AND WHITE GRID

print("Generating black and white grid")

black_and_white_grid = []

for x in range(drawWidth):
    column = []
    print(f"{round((x) / (drawWidth) * 100, 2)}% at x position of {math.floor(x * quality * scale)} out of {img.width}", end = "\r")
    for y in range(drawHeight):
        sum = 0
        for tx in range(math.floor(quality * scale)):
            for ty in range(math.floor(quality * scale)):
                pixel = GetPixel(math.floor(x * quality * scale + tx), math.floor(y * quality * scale + ty))
                sum += pixel[0] + pixel[1] + pixel[2]
        column.append(False if sum / ((quality ** 2) * 3) < 127.5 else True)
    black_and_white_grid.append(column)

### GENERATE OUTLINES

print(f"Completed! Generated grid of {drawWidth} width and {drawHeight} height                               ")
print("Getting outlines and visited grid")
outline = []
visited = []

for x in range(drawWidth):
    print(f"{round((x) / (drawWidth) * 100, 2)}% completed", end = "\r")
    column = []
    vColumn = []
    for y in range(drawHeight):
        vColumn.append(False)
        if not black_and_white_grid[x][y]:
            column.append(False)
            continue
        if x > 0:
            if not black_and_white_grid[x - 1][y]:
                column.append(True)
                continue
        if x < drawWidth - 1:
            if not black_and_white_grid[x + 1][y]:
                column.append(True)
                continue
        if y > 0:
            if not black_and_white_grid[x][y - 1]:
                column.append(True)
                continue
        if y < drawHeight - 1:
            if not black_and_white_grid[x][y + 1]:
                column.append(True)
                continue
        column.append(False)
    outline.append(column)
    visited.append(vColumn)

print("Completed! Outlines have been created")
print("Ready to draw! Press enter to begin")
input()

### DRAW
    
def FormatPosition(startPosition, x, y):
    return (startPosition[0] + x * quality, startPosition[1] + y * quality)

def SelectColor(x, y):
    if not outline[x][y]:
        IndexInfo.selectColorIndex = 3
    else:
        IndexInfo.selectColorIndex = 0

def SelectDirection(x, y):
    xInUpperBound = x < drawWidth - 1
    xInLowerBound = x > 0
    yInUpperBound = y < drawHeight - 1
    yInLowerBound = y > 0

    if xInUpperBound:
        if visited[x + 1][y] == False and outline[x + 1][y] == True:
            return (x + 1, y), 0
    if yInUpperBound:
        if visited[x][y + 1] == False and outline[x][y + 1] == True:
            return (x, y + 1), 1
    if xInLowerBound:
        if visited[x - 1][y] == False and outline[x - 1][y] == True:
            return (x - 1, y), 2
    if yInLowerBound:
        if visited[x][y - 1] == False and outline[x][y - 1] == True:
            return (x, y - 1), 3
    if xInUpperBound and yInUpperBound:
        if visited[x + 1][y + 1] == False and outline[x + 1][y + 1] == True:
            return (x + 1, y + 1), 4
    if xInLowerBound and yInUpperBound:
        if visited[x - 1][y + 1] == False and outline[x - 1][y + 1] == True:
            return (x - 1, y + 1), 5
    if xInLowerBound and yInLowerBound:
        if visited[x - 1][y - 1] == False and outline[x - 1][y - 1] == True:
            return (x - 1, y - 1), 6
    if xInUpperBound and yInLowerBound:
        if visited[x + 1][y - 1] == False and outline[x + 1][y - 1] == True:
            return (x + 1, y - 1), 7
    return (-1, -1), -1

def DrawSegment(x, y):
    cx = x
    cy = y
    previousDirection = -2
    Move(FormatPosition(startPosition, cx, cy))
    mouse.press(Button.left)
    while True:
        newPos, direction = SelectDirection(cx, cy)

        if direction != previousDirection:            
            Move(FormatPosition(startPosition, cx, cy))
            time.sleep(0.02)

        cx = newPos[0]
        cy = newPos[1]

        previousDirection = direction

        if direction == -1:
            break
        else:
            visited[cx][cy] = True
        
    mouse.release(Button.left)
    

def Draw(drawWidth, drawHeight, startPosition):
    for x in range(drawWidth):
        for y in range(drawHeight):
            if visited[x][y]:
                continue
            visited[x][y] = True
            SelectColor(x, y)
            if IndexInfo.selectColorIndex == 3:
                continue

            DrawSegment(x, y)

            if kybrd.is_pressed('#'):
                return

Draw(drawWidth, drawHeight, startPosition)