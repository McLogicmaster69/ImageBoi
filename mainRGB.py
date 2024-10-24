from PIL import Image
from pynput.mouse import Button, Controller
from pynput.keyboard import Key
from pynput.keyboard import Controller as ky
import keyboard as kybrd
import time
import math

TOPLEFT = (665, 334)
BOTTOMRIGHT = (1574, 842)
COLORPICKER = (566, 719)
WIDTH = 909
HEIGHT = 508
QUALITY = 6

class SelectableColor:
    def __init__(self, r, g, b, x, y, multi):
        self.r = r
        self.g = g
        self.b = b
        self.x = x
        self.y = y
        self.multi = multi

class IndexInfo:
    selectColorIndex = -1

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
keyboard = ky()

def Click():
    mouse.click(Button.left)

def Move(position):
    mouse.position = position

def PressKey(key):
    keyboard.press(key)
    keyboard.release(key)

def FormatPosition(startPosition, x, y):
    return (startPosition[0] + x, startPosition[1] + y)

def GetPixel(x, y):
    r, g, b = rgb_img.getpixel((x, y))
    return (r, g, b)

def GetColorDistance(colorA, colorB):
    total = (colorA[0] - colorB[0]) ** 2
    total += (colorA[1] - colorB[1]) ** 2
    total += (colorA[2] - colorB[2]) ** 2
    return math.sqrt(total)

def GetClosestColor(color):
    closestIndex = 0
    closestDistance = GetColorDistance((colors[0].r, colors[0].g, colors[0].b), color) * colors[0].multi
    currentIndex = 1
    while currentIndex < len(colors):
        c = colors[currentIndex]
        distance = GetColorDistance((c.r, c.g, c.b), color) * c.multi
        if distance < closestDistance:
            closestIndex = currentIndex
            closestDistance = distance
        currentIndex += 1
    return closestIndex

def SelectColor(x, y):
    pixelColor = GetPixel(x, y)
    index = GetClosestColor(pixelColor)
    if IndexInfo.selectColorIndex != index:
        c = colors[index]
        IndexInfo.selectColorIndex = index
        Move((c.x, c.y))
        Click()

def Draw(drawWidth, drawHeight, startPosition):
    x = 0
    while x < drawWidth:
        y = 0
        while y < drawHeight:
            SelectColor((x / drawWidth) * img.width, (y / drawHeight) * img.height)
            Move(FormatPosition(startPosition, x, y))
            Click()
            y += QUALITY
            if kybrd.is_pressed('#'):
                return
        time.sleep(0.1)
        x += QUALITY

imageRatio = img.width / img.height
frameRatio = WIDTH / HEIGHT

scale = 0
drawWidth = 0
drawHeight = 0
startPosition = (0, 0)

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

Draw(drawWidth, drawHeight, startPosition)

# 504 293
# 1417 802