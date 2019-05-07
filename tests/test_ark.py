import unittest
import pygame as pg
import math
import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))
from GameObjects.Map import Map
from GameObjects.Arkanoid import Arkanoid
from GameObjects.Menu import Menu
from GameObjects.Button import Button
from GameObjects.Game import Game
from GameObjects.Ball import Ball
from GameObjects.Title import Title
from GameObjects.Deck import Deck


class Tester(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        with open("../Levels/Level2.txt") as f:
            self.lines_list = [line for line in f]
        self.lines_list_copy = self.lines_list.copy()
        pic = {'1': None,
               '2': None,
               '3': None,
               '-': None}
        self.map = Map(self.lines_list, self.lines_list_copy, pic)
        self.map.build_map()
        self.title = self.map.titles[48]
        self.deck = Deck(20, 90, 100, 100, None)
        self.ark = Arkanoid('Level2.txt', 6, 4)
        self.buttons = [Button((400, 150), (150, 50),
                               "Start", (255, 255, 255), (186, 85, 211), 0),
                        Button((400, 250), (150, 50),
                               "Choose name", (255, 255, 255), (155, 10, 170),
                               1),
                        Button((400, 350), (150, 50),
                               "Difficulty : Light", (255, 255, 255),
                               (148, 0, 211),
                               2),
                        Button((400, 450), (150, 50),
                               "Records Table", (255, 255, 255), (139, 0, 139),
                               3),
                        Button((400, 550), (150, 50),
                               "Quit", (255, 255, 255), (128, 0, 128), 4)]
        self.menu = Menu(self.buttons, self.game)
        self.ball = Ball(100, 100, 5, None)
        self.ball.x_projection = 3
        self.ball.y_projection = 4
        self.images_path = "../Images/"

    def test_title_hit(self):
        self.title.hit()
        self.assertEqual(self.title.power, 2)
        self.assertEqual(
            self.title.map[self.title.map_row][self.title.map_column], '2')
        self.title.hit()
        self.assertEqual(self.title.power, 1)
        self.assertEqual(
            self.title.map[self.title.map_row][self.title.map_column], '1')
        self.title.hit()
        self.assertEqual(self.title.power, 0)
        self.assertEqual(
            self.title.map[self.title.map_row][self.title.map_column], ' ')
        self.assertEqual(self.title.is_diaphanous, True)
        self.map.reestablish()

    def test_deck_move(self):
        self.deck.move(400)
        self.assertEqual(self.deck.x, 355)

    def test_deck_update(self):
        self.deck.move(400)
        self.deck.update()
        self.assertEqual(self.deck.rect.x, 355)
        self.assertEqual(self.deck.rect.y, self.deck.start_y)

    def test_akranoid_reestablish(self):
        self.ark.username = "aa"
        self.ark.current_score = 12
        self.ark.lives = 0
        self.was_result_recorded = True
        self.cheats = True
        self.ark.reestablish()
        self.assertEqual(self.ark.username, 'Player')
        self.assertEqual(self.ark.current_score, 0)
        self.assertEqual(self.ark.lives, 1)
        self.assertEqual(self.ark.was_result_recorded, False)
        self.assertEqual(self.ark.cheats, False)
        self.assertEqual(self.ark.speed, 6)
        self.assertEqual(self.ark.hit_score, 20)
        self.assertEqual(self.ark.file, 'Level2.txt')

    def test_menu_build_records_table(self):
        lines = self.menu.build_records_table()
        self.assertEqual(len(lines), 10)

    def test_ball_change_direction_deck(self):
        speed = self.ball.speed
        deck = Deck(20, 90, 70, 130, None)
        self.ball.change_direction(deck, 'deck')
        self.assertAlmostEqual(math.sqrt(
            self.ball.x_projection ** 2 + self.ball.y_projection ** 2), speed)

    def test_ball_active_move(self):
        self.ball.is_moving = True
        self.ball.active_move(10)
        self.assertAlmostEqual(math.sqrt(
            self.ball.x_projection ** 2 + self.ball.y_projection ** 2), 10)
        self.ball.x_projection = 0
        self.ball.y_projection = 0
        self.ball.active_move(10)
        self.assertAlmostEqual(math.sqrt(
            self.ball.x_projection ** 2 + self.ball.y_projection ** 2), 10)

    def test_ball_passive_move(self):
        self.ball.passive_move(100)
        self.assertEqual(self.ball.current_x, 85)

    def test_choose_title(self):
        conflicted = [Title(1, self.images_path + "Yellow.png",
                            70, 130, [], 1, 1),
                      Title(1, self.images_path + "Yellow.png",
                            120, 130, [], 1, 1)]
        self.assertEqual(self.ball.choose_title(conflicted), conflicted[0])
        conflicted = [Title(1, self.images_path + "Yellow.png",
                            55, 130, [], 1, 1),
                      Title(1, self.images_path + "Yellow.png",
                            105, 130, [], 1, 1)]
        self.assertEqual(self.ball.choose_title(conflicted), conflicted[1])

    def test_ball_change_direction_title(self):

        def change_projections(x, y):
            self.ball.x_projection = x
            self.ball.y_projection = y

        title1 = Title(1, self.images_path + "Yellow.png",
                       70, 70, [], 1, 1)
        change_projections(-3, 1)
        speed = math.sqrt(
            self.ball.x_projection ** 2 + self.ball.y_projection ** 2)
        self.ball.change_direction(title1, "title")
        self.assertAlmostEqual(math.sqrt(
            self.ball.x_projection ** 2 + self.ball.y_projection ** 2), speed)
        title2 = Title(1, self.images_path + "Yellow.png",
                       70, 70, [], 1, 1)
        change_projections(3, 1)
        speed = math.sqrt(
            self.ball.x_projection ** 2 + self.ball.y_projection ** 2)
        self.ball.change_direction(title2, "title")
        self.assertAlmostEqual(math.sqrt(
            self.ball.x_projection ** 2 + self.ball.y_projection ** 2), speed)
        title3 = Title(1, self.images_path + "Yellow.png",
                       70, 70, [], 1, 1)
        change_projections(-3, -1)
        self.ball.current_y = 50
        speed = math.sqrt(
            self.ball.x_projection ** 2 + self.ball.y_projection ** 2)
        self.ball.change_direction(title3, "title")
        self.assertAlmostEqual(math.sqrt(
            self.ball.x_projection ** 2 + self.ball.y_projection ** 2), speed)
        title4 = Title(1, self.images_path + "Yellow.png",
                       70, 70, [], 1, 1)
        change_projections(3, -1)
        self.ball.current_y = 50
        self.ball.current_y = 100
        speed = math.sqrt(
            self.ball.x_projection ** 2 + self.ball.y_projection ** 2)
        self.ball.change_direction(title4, "title")
        self.assertAlmostEqual(math.sqrt(
            self.ball.x_projection ** 2 + self.ball.y_projection ** 2), speed)

    def test_game_ball_update(self):
        self.ball.active_move(5)
        self.ball.update()
        self.assertEqual(self.ball.start_x - 3, self.ball.current_x)
        self.assertEqual(self.ball.start_y - 4, self.ball.current_y)

    def test_game_change_volume(self):
        self.game.start_music()
        for i in range(10):
            self.game.change_volume('+')
        self.assertGreater(pg.mixer.music.get_volume(), 0.9)
        for i in range(10):
            self.game.change_volume('-')
        self.assertGreater(0.1, pg.mixer.music.get_volume())

    def test_game_reload_charactetrs(self):
        self.ball.is_moving = True
        self.deck.move(400)
        self.game.reload_characters(self.ark, self.ball, self.deck)
        self.assertEqual(self.ark.lives, 3)
        self.assertEqual(self.ball.is_moving, False)
        self.assertEqual(self.ball.current_x, self.ball.start_x)
        self.assertEqual(self.ball.current_y, self.ball.start_y)
        self.assertEqual(self.deck.x, self.deck.start_x)

    def test_game_create_conflicted(self):
        self.ball.current_x = 181
        self.ball.current_y = 384
        self.ball.update()
        modules = pg.sprite.Group()
        modules.add(self.ball, self.deck)
        titles = pg.sprite.Group()
        for title in self.map.titles:
            titles.add(title)
        self.assertEqual(len(modules), 2)
        self.assertEqual(len(titles), 109)
        conflicted = self.game.create_conflicted(modules, titles, self.ball)
        self.assertNotEqual(conflicted, None)

    def test_game_switch_level(self):
        self.game.difficulty = "Medium"
        ark, lines_list, lines_list_copy, map = self.game.switch_level(3, None)
        self.assertEqual(ark.lives, 3)
        self.assertEqual(len(lines_list), 20)

    def test_map_initialize(self):
        self.assertEqual(self.map.count_titles, 52)

    def test_map_reestablish(self):
        self.map.map_list.clear()
        self.map.reestablish()
        self.assertEqual(len(self.map.map_list), 20)

    def test_map_build_map(self):
        self.assertEqual(len(self.map.titles), 109)
        self.assertEqual(self.map.titles[0].up, None)
        self.assertEqual(self.map.titles[47].power, 1)
        self.assertEqual(self.map.titles[47].left.power, 2)
        self.assertEqual(self.map.titles[47].right.power, 3)


if __name__ == '__main__':
    unittest.main()
