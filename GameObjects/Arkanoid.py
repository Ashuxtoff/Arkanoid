RADIUS = 15
LINING_CONST = 10


class Arkanoid:
    def __init__(self, file, speed, lives):
        self.file = file
        self.speed = speed
        self.cheats = False
        self.lives = lives
        self.current_score = 0
        self.hit_score = 20
        self.username = 'Player'
        self.was_result_recorded = False

    def reestablish(self):
        self.username = 'Player'
        self.current_score = 0
        self.lives = 1
        self.was_result_recorded = False
        self.cheats = False
