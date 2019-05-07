import pygame as pg
import math
import random


RADIUS = 15


class Ball(pg.sprite.Sprite):
    def __init__(self, x, y, speed, image):
        pg.sprite.Sprite.__init__(self)
        self.start_x = x
        self.start_y = y
        self.current_x = x
        self.current_y = y
        self.image = image
        # self.image.set_colorkey((255, 255, 255))
        self.rect = pg.Rect((self.current_x, self.current_y),
                            (2*RADIUS, 2*RADIUS))
        self.is_moving = False
        self.x_projection = 0
        self.y_projection = 0
        self.speed = speed
        self.last_conflict_x = 0

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def passive_move(self, new_x):
        self.current_x = self.last_conflict_x = new_x - RADIUS

    def active_move(self, speed):
        if speed == self.speed:
            self.is_moving = True
            if self.x_projection == 0:
                self.x_projection = random.uniform(0, 5)
                self.y_projection = math.sqrt(
                    speed ** 2 - self.x_projection ** 2)
                if random.randint(0, 1) == 0:
                    self.x_projection *= -1
        else:
            self.x_projection *= speed / self.speed
            self.y_projection *= speed / self.speed
            self.speed = speed
        self.current_x -= self.x_projection
        self.current_y -= self.y_projection

    def update(self):
        self.rect = pg.Rect((self.current_x, self.current_y),
                            (2 * RADIUS, 2 * RADIUS))

    def choose_title(self, conflicted):
        if self.current_x + RADIUS < conflicted[0].x + conflicted[0].width:
            return conflicted[0]
        return conflicted[1]

    def change_direction(self, element, mode):

        def compare_width_height(width, height):
            if height > width:
                self.x_projection *= -1
            else:
                self.y_projection *= -1

        def check_neighbour(neighbour):
            if neighbour is not None:
                self.x_projection *= -1
            else:
                self.y_projection *= -1

        if mode == 'title':
            if self.x_projection < 0 and self.y_projection > 0:
                if self.current_y > element.y:
                    intersection_height = element.height - (
                            self.current_y - element.y)
                    intersection_width =\
                        self.current_x + 2 * RADIUS - element.x
                    compare_width_height(intersection_width,
                                         intersection_height)
                else:
                    check_neighbour(element.up)
            elif self. x_projection < 0 and self.y_projection < 0:
                if self.current_y < element.y:
                    intersection_height = element.height - (
                        element.y + element.height - (
                            self.current_y + 2 * RADIUS))
                    intersection_width = \
                        self.current_x + 2 * RADIUS - element.x
                    compare_width_height(intersection_width,
                                         intersection_height)
                else:
                    check_neighbour(element.down)
            elif self.x_projection > 0 and self.y_projection < 0:
                if self.current_y < element.y:
                    intersection_height = element.height - (
                        element.y + element.height - (
                            self.current_y + 2 * RADIUS))
                    intersection_width = element.x + element.width
                    - self.current_x
                    compare_width_height(intersection_width,
                                         intersection_height)
                else:
                    check_neighbour(element.down)
            elif self.x_projection > 0 and self.y_projection > 0:
                if self.current_y > element.y:
                    intersection_height = element.height
                    - (self.current_y - element.y)
                    intersection_width = element.x
                    + element.width - self.current_x
                    compare_width_height(intersection_width,
                                         intersection_height)
                else:
                    check_neighbour(element.up)
        if mode == 'deck':
            self.last_conflict_x = self.current_x
            ball_mid = self.current_x + RADIUS / 2
            r = RADIUS
            pi = math.pi
            a = pi/2 - math.atan((
                ball_mid - RADIUS / 2 - element.x - element.width / 2) / (
                    0.8 * r))
            b = math.atan(self.y_projection / self.x_projection)
            c = a - b
            self.x_projection = self.speed * math.cos(
                c) ** 2 * self.x_projection / math.fabs(
                self.x_projection)
            self.y_projection = math.sqrt(
                self.speed ** 2 - self.x_projection ** 2)
