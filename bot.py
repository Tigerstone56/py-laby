import random

from player import Direction, Player

DIRECTIONS = [ # On définit les directions possibles du bot
    Direction.LEFT,
    Direction.UP,
    Direction.RIGHT,
    Direction.DOWN,
]


class Bot(Player): # On définit une classe pour le bot qui hérite de la classe Player
    def __init__(self, canvas, x, y, maze, win, type):
        """On initialise le bot avec un canvas, une position (x, y), un labyrinthe, une fonction de victoire et un type de bot."""
        super().__init__(canvas, x, y, maze, win)
        self.type = type
        self.direction = Direction.DOWN

    def hand_move(self):
        """Déplace le bot en suivant la main gauche ou droite selon son type."""
        index = DIRECTIONS.index(self.direction)
        offsets = [-1, 0, 1, 2] if self.type == "bot_left" else [1, 0, -1, -2]

        for offset in offsets:
            direction = DIRECTIONS[(index + offset) % 4]

            if self.can_move(direction):
                self.move(direction)
                return

    def random_move(self):
        """Déplace le bot dans une direction aléatoire, en évitant de revenir sur ses pas."""
        possible_directions = [
            direction for direction in DIRECTIONS if self.can_move(direction)
        ]

        if len(possible_directions) > 1:
            opposite = {
                Direction.UP: Direction.DOWN,
                Direction.DOWN: Direction.UP,
                Direction.LEFT: Direction.RIGHT,
                Direction.RIGHT: Direction.LEFT,
            }

            possible_directions = [
                direction
                for direction in possible_directions
                if direction != opposite[self.direction]
            ]

        direction = random.choice(possible_directions)
        self.move(direction)

    def bot_move(self):
        """Déplace le bot selon son type."""
        if self.type == "bot_left" or self.type == "bot_right":
            self.hand_move()
        if self.type == "bot_random":
            self.random_move()
