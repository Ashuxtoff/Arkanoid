import pygame as pg
import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))
from GameObjects.Menu import Menu
from GameObjects.Arkanoid import Arkanoid
from GameObjects.Button import Button
from GameObjects.Map import Map
from GameObjects.Deck import Deck
from GameObjects.Ball import Ball


RADIUS = 15


class Game:
    def __init__(self):
        pg.init()
        self.size = (950, 700)
        self.background = pg.Surface(self.size)
        self.background.fill((60, 0, 60))
        self.buttons = [Button((400, 150), (150, 50),
                        "Start", (255, 255, 255), (186, 85, 211), 0),
                        Button((400, 250), (150, 50),
                        "Choose name", (255, 255, 255), (155, 10, 170), 1),
                        Button((400, 350), (150, 50),
                        "Difficulty : Light", (255, 255, 255),
                               (148, 0, 211), 2),
                        Button((400, 450), (150, 50),
                        "Records Table", (255, 255, 255), (139, 0, 139), 3),
                        Button((400, 550), (150, 50),
                        "Quit", (255, 255, 255), (128, 0, 128), 4)]
        self.difficulty = ""
        self.difficulty_dict = {"Light": (6, 4),
                                "Medium": (8, 3),
                                "Hard": (10, 2),
                                "UltraHard": (10, 1)}
        self.levels = ['Level1.txt', 'Level2.txt', 'Level3.txt',
                       'Level4.txt', 'Level5.txt']
        self.level_path = "../Levels/"
        self.current_level = 0

    def start_music(self):
        pg.mixer.music.load("../Sounds/sound.mp3")
        pg.mixer.music.play(30)

    def draw_all(self, screen, map, deck, ball):
        map.draw(screen)
        deck.draw(screen)
        ball.draw(screen)

    def reestablish(self, ark, map):
        ark.reestablish()
        map.reestablish()

    def change_volume(self, mode):
        volume = pg.mixer.music.get_volume()
        if mode == "+":
            pg.mixer.music.set_volume(min(1, volume + 0.1))
        if mode == '-':
            pg.mixer.music.set_volume(max(0, volume - 0.1))

    def reload_characters(self, ark,  ball, deck):
        ark.lives -= 1
        ball.is_moving = False
        ball.current_x = ball.start_x
        ball.current_y = ball.start_y
        deck.x = deck.start_x

    def create_conflicted(self, modules, titles, ball):
        modules.update()
        titles.update()
        start_conflicted = pg.sprite.spritecollide(ball, titles, False)
        conflicted = []
        for title in start_conflicted:
            if not title.is_diaphanous:
                conflicted.append(title)
        if conflicted:
            if len(conflicted) > 1:
                conflicted_title = ball.choose_title(conflicted)
            else:
                conflicted_title = conflicted[0]
            conflicted.clear()
            return conflicted_title

    def switch_level(self, lives, pic):
        ark = Arkanoid(self.levels[self.current_level],
                       self.difficulty_dict[self.difficulty][0], lives)
        ark.difficulty = self.difficulty
        level = open(self.level_path + ark.file)
        lines_list = [line for line in level]
        lines_list_copy = lines_list.copy()
        map = Map(lines_list, lines_list_copy, pic)
        return ark, lines_list, lines_list_copy, map

    def render_title(self, screen, font, title_text, size, color, coords):
        screen.blit(pg.font.Font(font, size).render(
            title_text, 1, color), coords)

    def game(self):
        screen = pg.display.set_mode(self.size)
        power_pic_dict = {'1': pg.image.load("../Images/Yellow.png").convert(),
                          '2': pg.image.load("../Images/Orange.png").convert(),
                          '3': pg.image.load("../Images/Red.png").convert(),
                          '-': pg.image.load("../Images/Grey.png").convert()}
        pg.display.set_caption('Arkanoid')
        menu = Menu(self.buttons, self)
        menu.menu(screen)
        self.difficulty = menu.difficulty
        ark, lines_list, lines_list_copy, map =\
            self.switch_level(self.difficulty_dict[self.difficulty][1],
                              power_pic_dict)
        deck = Deck(20, 90, self.size[0] // 2 - 45, self.size[1] - 50,
                    pg.image.load("../Images/Deck.png").convert())
        ball = Ball(deck.start_x + deck.width // 2 - RADIUS,
                    deck.start_y - 2*RADIUS, ark.speed,
                    pg.image.load("../Images/Ball.png").convert())
        ball.image.set_colorkey((255, 255, 255))
        if menu.name != '':
            ark.username = menu.name
        self.start_music()
        self.draw_all(screen, map, deck, ball)
        modules = pg.sprite.Group()
        modules.add(ball, deck)
        titles = pg.sprite.Group()
        for title in map.titles:
            titles.add(title)
        while True:
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    raise SystemExit("QUIT")
                if e.type == pg.MOUSEMOTION:
                    if e.pos[0] < self.size[0] - deck.width - 56 or\
                            e.pos[0] > 56:
                        deck.move(e.pos[0])
                    if not ball.is_moving:
                        ball.passive_move(e.pos[0])
                if e.type == pg.MOUSEBUTTONUP:
                    ball.active_move(ark.speed)
                if ark.lives == 0:
                    with open("RecordsTable.txt", 'a') as f:
                        if not ark.was_result_recorded:
                            f.write(ark.username + '     ' + str(
                                ark.current_score) + '\n')
                            ark.was_result_recorded = True
                    if e.type == pg.KEYDOWN:
                        self.reestablish(ark, map)
                        self.current_level = 0
                        self.game()
                if e.type == pg.KEYDOWN:
                    if e.key == pg.K_DOWN:
                        self.change_volume('-')
                    if e.key == pg.K_UP:
                        self.change_volume('+')
                    if e.key == pg.K_c:
                        ark.cheats = True
                    if ark.cheats:
                        if e.key == pg.K_s:
                            ark.speed //= 2
                        if e.key == pg.K_f:
                            ark.speed *= 2
                        if e.key == pg.K_d:
                            ark.hit_score *= 2
                        if e.key == pg.K_l:
                            ark.lives += 1
            if map.count_titles == 0:
                self.reload_characters(ark, ball, deck)
                self.current_level += 1
                score = ark.current_score
                ark, lines_list, lines_list_copy, map =\
                    self.switch_level(ark.lives + 1, power_pic_dict)
                ark.current_score += score
                map.draw(screen)
                modules = pg.sprite.Group()
                modules.add(ball, deck)
                titles = pg.sprite.Group()
                for title in map.titles:
                    titles.add(title)
            if ball.current_y > self.size[1]:
                self.reload_characters(ark, ball, deck)
            if ball.is_moving:
                if pg.sprite.collide_rect(ball, deck):
                    ball.change_direction(deck, 'deck')
                ball.active_move(ark.speed)
            conflicted_title = self.create_conflicted(modules, titles, ball)
            if conflicted_title is not None:
                ball.change_direction(conflicted_title, 'title')
                if conflicted_title.power <= 3:
                    ark.current_score += ark.hit_score
                conflicted_title.hit()
                screen.blit(self.background, (0, 0))
                map = Map(lines_list, lines_list_copy, power_pic_dict)
            screen.blit(self.background, (0, 0))
            if ark.lives > 0:
                map.draw(screen)
            self.render_title(screen, "Font.ttf",
                              "LIVES: " + str(ark.lives),
                              50, (220, 20, 60), (10, -2))
            self.render_title(screen, "Font.ttf",
                              "SCORE: " + str(ark.current_score),
                              50, (255, 255, 0),
                              (self.size[0] - 250, -2))
            deck.draw(screen)
            ball.draw(screen)
            if ark.lives == 0:
                self.background.fill((60, 0, 60))
                screen.blit(self.background, (0, 0))
                pg.mixer.music.pause()
                self.render_title(screen, "Font.ttf", "GAME OVER",
                                  130, (0, 0, 139),
                                  (200, 300))
                self.render_title(screen, "Font.ttf",
                                  "YOUR SCORE: " + str(ark.current_score), 100,
                                  (255, 69, 0), (170, 500))
            pg.display.update()


if __name__ == '__main__':
    game = Game()
    game.game()
