import pygame as pg
import sys


def render_title(screen, font, title_text, size, color, coords):
    screen.blit(pg.font.Font(font, size).render(title_text, 1, color), coords)


class Menu:
    def __init__(self, buttons, game):
        self.game = game
        self.buttons = buttons
        if game.difficulty == '':
            self.difficulty = "Light"
        else:
            self.difficulty = game.difficulty
        self.diff_list = ["Light", "Medium", "Hard", "UltraHard"]
        self.name = ''

    def build_records_table(self):
        with open("../GameObjects/RecordsTable.txt") as f:
            lines = [line for line in f]
            lines = sorted(
                lines, key=lambda line: int(line.split()[1]), reverse=True)
            return lines[:10]

    def render(self, screen, font, button_number):
        for i in range(len(self.buttons)):
            button = self.buttons[i]
            if button_number == button.number:
                screen.blit(font.render(
                    button.text, 1, button.active_color), button.coords)
            else:
                screen.blit(font.render(
                    button.text, 1, button.base_color), button.coords)

    def menu(self, screen):
        font_menu = pg.font.Font("../GameObjects/Font.ttf", 50)
        button_number = 0
        difficulty_factor = 0
        bg = pg.Surface((950, 700))
        while True:
            bg.fill((25, 25, 112))
            mouse_pos = pg.mouse.get_pos()
            for but in self.buttons:
                if mouse_pos[0] > but.x > mouse_pos[0] - but.width and \
                   mouse_pos[1] - but.height < but.y < mouse_pos[1]:
                    button_number = but.number
            self.render(bg, font_menu, button_number)
            break_factor = False
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    sys.exit()
                if e.type == pg.KEYDOWN:
                    if e.key == pg.K_ESCAPE:
                        sys.exit()
                if e.type == pg.MOUSEBUTTONUP and e.button == 1:
                    if button_number == 4:
                        sys.exit()
                    if button_number == 2:
                        difficulty_factor += 1
                        if difficulty_factor >= 4:
                            difficulty_factor -= 4
                        self.buttons[button_number].text =\
                            "Difficulty: " + self.diff_list[difficulty_factor]
                        self.difficulty = self.diff_list[difficulty_factor]
                    if button_number == 3:
                        records = self.build_records_table()
                        bg.fill((25, 25, 112))
                        screen.blit(bg, (0, 0))
                        break_factor2 = False
                        while True:
                            for i in range(len(records)):
                                render_title(screen, "Font.ttf", str(
                                    i+1) + '. ' + records[i][:-1], 50, (
                                        244, 164, 96), (100, 70 + i * 60))
                            for ev in pg.event.get():
                                if ev.type == pg.KEYDOWN:
                                    if ev.key == pg.K_ESCAPE:
                                        break_factor2 = True
                                        break
                            if break_factor2:
                                break
                            pg.display.flip()
                    if button_number == 1:
                        break_factor1 = False
                        while True:
                            for ev in pg.event.get():
                                if ev.type == pg.KEYDOWN:
                                    if ev.key == pg.K_BACKSPACE:
                                        self.name = self.name[:-1]
                                    elif ev.key == pg.K_RETURN:
                                        break_factor1 = True
                                        break
                                    else:
                                        self.name += ev.unicode
                            if break_factor1:
                                break
                            screen.blit(bg, (0, 0))
                            render_title(screen, "Font.ttf",
                                         "Choose name: " + self.name, 50,
                                         (244, 164, 96), (400, 250))
                            pg.display.flip()

                    if button_number == 0:
                        self.game.start_music()
                        break_factor = True
                        break
            if break_factor:
                break

            screen.blit(bg, (0, 0))
            pg.display.flip()
