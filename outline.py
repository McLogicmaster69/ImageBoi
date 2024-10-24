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
QUALITY = 4

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