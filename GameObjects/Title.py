import pygame as pg


class Title(pg.sprite.Sprite):
    def __init__(self, power, picture,
                 x, y, map_list, map_row, map_column):
        pg.sprite.Sprite.__init__(self)
        self.power = power
        self.x = x
        self.y = y
        self.height = 35
        self.width = 56
        self.map_row = map_row
        self.map_column = map_column
        self.map = map_list
        self.image = picture
        self.rect = pg.Rect((self.x, self.y), (self.width, self.height))
        self.is_diaphanous = False
        self.up = None
        self.down = None
        self.left = None
        self.right = None

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def hit(self):
        self.power -= 1
        if self.power == 2:
            self.map[self.map_row] = self.map[self.map_row][
                :self.map_column] + '2' + self.map[self.map_row][
                    1 + self.map_column:]
        if self.power == 1:
            self.map[self.map_row] = self.map[self.map_row][
                :self.map_column] + '1' + self.map[self.map_row][
                    1 + self.map_column:]
        if self.power == 0:
            self.map[self.map_row] = self.map[self.map_row][
                :self.map_column] + ' ' + self.map[self.map_row][
                    1 + self.map_column:]
            self.is_diaphanous = True
