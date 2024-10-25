from PIL import Image
from pynput.mouse import Button, Controller
from ImageBoiClasses import SelectableColor, IndexInfo
import keyboard as kybrd
import time
import math

TOPLEFT = (665, 334)
BOTTOMRIGHT = (1574, 842)
WIDTH = 909
HEIGHT = 508
QUALITY = 8

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

print("Input the file")
filename = input()
img = Image.open(filename)
rgb_img = img.convert('RGB')
mouse = Controller()

imageRatio = img.width / img.height
frameRatio = WIDTH / HEIGHT

scale = 0
startPosition = (0, 0)
xScale = img.width / WIDTH
yScale = img.height / HEIGHT

scale = xScale if xScale > yScale else yScale

drawWidth = (img.width / scale) / QUALITY
drawHeight = (img.height / scale) / QUALITY

if imageRatio == frameRatio:
    scale = WIDTH / img.width
    drawWidth = WIDTH
    drawHeight = HEIGHT
    startPosition = (665, 334)
elif imageRatio > frameRatio:
    scale = WIDTH / img.width
    drawWidth = WIDTH
    drawHeight = round(img.height * scale)
    startPosition = (665, round(588 - drawHeight / 2))
else:
    scale = HEIGHT / img.height
    drawWidth = round(img.width * scale)
    drawHeight = HEIGHT
    startPosition = (round(1119.5 - drawWidth / 2), 334)

def GetPixel(x, y):
    r, g, b = rgb_img.getpixel((x, y))
    return (r, g, b)

#drawWidth = math.floor(drawWidth / QUALITY)
#drawHeight = math.floor(drawHeight / QUALITY)

### GENERATE BLACK AND WHITE GRID

print("Generating black and white grid")

black_and_white_grid = []

for x in range(0, (img.width // QUALITY) * QUALITY, QUALITY):
    column = []
    for y in range(0, (img.height // QUALITY) * QUALITY, QUALITY):
        sum = 0
        for tx in range(QUALITY):
            for ty in range(QUALITY):
                pixel = GetPixel((x + tx) / img.width * drawWidth, (y + ty) / img.height * drawHeight)
                sum += pixel[0] + pixel[1] + pixel[2]
        if sum / ((QUALITY ** 2) * 3) < 127.5:
            column.append(False)
        else:
            column.append(True)
    black_and_white_grid.append(column)

### GENERATE OUTLINES


print("Getting outlines")
outline = []

for x in range(drawWidth):
    column = []
    for y in range(drawHeight):
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

print("Ready to draw! Press enter to begin")
input()

### DRAW

def Click():
    mouse.click(Button.left)

def Move(position):
    mouse.position = position
    
def FormatPosition(startPosition, x, y):
    return (startPosition[0] + x, startPosition[1] + y)

def SelectColor(x, y):
    if not outline[x][y]:
        IndexInfo.selectColorIndex = 3
    else:
        IndexInfo.selectColorIndex = 0

def Draw(drawWidth, drawHeight, startPosition):
    for x in range(drawWidth):
        for y in range(drawHeight):
            SelectColor(x, y)

            if IndexInfo.selectColorIndex == 3:
                continue

            Move(FormatPosition(startPosition, x, y))
            Click()
            if kybrd.is_pressed('#'):
                return
            time.sleep(0.1)

Draw(drawWidth, drawHeight, startPosition)