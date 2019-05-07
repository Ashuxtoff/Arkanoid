import pygame as pg


class Deck(pg.sprite.Sprite):
    def __init__(self, height, width, x, y, image):
        pg.sprite.Sprite.__init__(self)
        self.height = height
        self.width = width
        self.start_x = x
        self. start_y = y
        self.x = x
        self.color = (176, 224, 230)
        self.image = image
        self.rect = pg.Rect((self.x, self.start_y), (self.width, self.height))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def move(self, new_x):
        self.x = new_x - self.width//2

    def update(self):
        self.rect = pg.Rect((self.x, self.start_y), (self.width, self.height))
