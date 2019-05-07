import sys
import os
import pygame as pg
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))
from GameObjects.Title import Title


TITLE_WIDTH = 50
TITLE_HEIGHT = 35


class Map:
    def __init__(self, lines_list, reestablish_list, pics):
        self.images_path = "../Images/"
        self.char_picture_dict = {'1': "Yellow.png",
                                  '2': "Orange.png",
                                  '3': "Red.png",
                                  '-': "Grey.png"}
        self.char_power_dict = {'1': 1,
                                '2': 2,
                                '3': 3,
                                '-': sys.maxsize}
        self.pics = pics
        self.map_list = lines_list
        self.map_list_copy = reestablish_list
        self.titles = []
        self.count_titles = 0
        for row in self.map_list:
            for column in row:
                if column.isdigit():
                    self.count_titles += 1

    def reestablish(self):
        self.map_list = self.map_list_copy.copy()

    def build_map(self):
        pos_dict = {}
        x = y = 0
        for i in range(len(self.map_list)):
            row = self.map_list[i]
            for j in range(len(row)):
                symbol = row[j]
                if symbol.isdigit() or symbol == '-':
                    picture = self.pics[symbol]
                    title = Title(self.char_power_dict[symbol],
                                  picture, x, y, self.map_list, i, j)
                    pos_dict[(i, j)] = title
                    if i > 0 and self.map_list[i-1][j] != ' ':
                        pos_dict[(i-1, j)].down = title
                        title.up = pos_dict[(i-1, j)]
                    if j > 0 and self.map_list[i][j-1] != ' ':
                        pos_dict[(i, j-1)].right = title
                        title.left = pos_dict[(i, j-1)]
                    self.titles.append(title)
                x += TITLE_WIDTH
            y += TITLE_HEIGHT
            x = 0

    def draw(self, screen):
        self.build_map()
        for title in self.titles:
            title.draw(screen)

# кпв
# альт издержки
# равноывесие на рынке
# излишки
# вмешательство государства на рынок

# НАСРАТЬ НА ПОВЕДЕНИЕ ПОТРЕБИТЕЛЯ

# МОНОПОЛИЯ, конкуренция монопсония
# структура издержкек фирмы (точку входа/вызода фирмы)
# предельный, средний, общий продукт фирмы
