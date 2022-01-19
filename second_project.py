from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import pygame
from random import *
import sys
import os.path
import math

black = (0, 0, 0)
white = (255, 255, 255)
gray_yellow = (255, 196, 155)
beige = (255, 167, 108)
deep_purple = (103, 58, 183)
blue = (33, 150, 243)
light_yellow = (255, 255, 74)
light_red = (255, 57, 57)
red = (255, 0, 0)
light_orange = (255, 133, 51)
pink = (255, 87, 45)
grey = (150, 150, 150)
light_grey = (192, 192, 192)
yellow = (255, 255, 128)
dark_yellow = (204, 204, 0)
orange = (251, 82, 0)
brown = (193, 63, 0)


color_dict = {
    0: light_grey,
    2: white,
    4: gray_yellow,
    8: beige,
    16: light_orange,
    32: pink,
    64: light_red,
    128: light_yellow,
    256: dark_yellow,
    512: orange,
    1024: yellow,
    2048: brown,
    4096: red,
}


def get_color(i):
    if i in color_dict:
        return color_dict[i]
    else:
        return red


points = 0
board_size = 4
matrix = [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
]
last_matrix = []