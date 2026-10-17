from enum import Enum

from utils import import_config

config = import_config()

from utils import darken_color, get_position


class Direction(Enum): # On définit une énumération pour les directions possibles du joueur
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class Player: # On définit une classe pour le joueur
    def __init__(self, canvas, x, y, maze, win): 
        """On initialise le joueur avec un canvas, une position (x, y), un labyrinthe et une fonction de victoire."""
        self.canvas = canvas
        self.x = x
        self.y = y
        self.maze = maze
        self.win = win
        self.moves = 0

    def draw(self):
        """Dessine le joueur sur le canvas."""
        x, y = (
            get_position(self.x, self.y)[0] + (20 / 4),
            get_position(self.x, self.y)[1] + (20 / 4),
        )

        # On dessine le joueur sur le canvas avec une couleur spécifique et un rectangle plus petit que la case du labyrinthe
        
        if config["blind"]["enabled"]: 
            bx, by = get_position(self.x, self.y)
            self.canvas.create_rectangle(
                bx,
                by,
                bx + 20 - 1,
                by + 20 - 1,
                fill=config["colors"]["light"],
                outline=config["colors"]["light"],
            )

        self.canvas.create_rectangle(
            x,
            y,
            x + (20 / 2),
            y + (20 / 2),
            fill=config["colors"]["player"],
        )
        # Si le mode aveugle est activé, on dessine aussi la lumière
        if config["blind"]["enabled"]:
            self.draw_light()

    def clear(self):
        """Efface le joueur du canvas"""
        x, y = get_position(self.x, self.y)

        self.canvas.create_rectangle(
            x,
            y,
            x + 20 - 1,
            y + 20 - 1,
            fill=config["colors"]["floor"],
            outline=config["colors"]["floor"],
        )

    def draw_light(self):
        """Dessine la lumière autour du joueur."""
        # On définit les directions possibles pour la lumière
        directions = [
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1),
        ]

        # On utilise une liste pour stocker les positions de lumière à dessiner et un ensemble pour suivre les positions déjà visitées
        light = [(self.x, self.y, 0)]
        visited = {(self.x, self.y)}

        while light: # Tant que la liste de lumière n'est pas vide, on continue à dessiner la lumière
            x, y, distance = light.pop(0)

            # Si la distance est supérieure à la puissance de la lumière, on ne dessine pas la lumière
            if distance >= config["blind"]["light_power"]:
                continue

            for dx, dy in directions:
                nx = x + dx
                ny = y + dy

                if (
                    0 <= nx < len(self.maze[0])
                    and 0 <= ny < len(self.maze)
                    and self.maze[ny][nx] == 0
                    and (nx, ny) not in visited
                ): # Si la nouvelle position est dans les limites du labyrinthe, que c'est un chemin et qu'elle n'a pas été visitée, on dessine la lumière
                    visited.add((nx, ny))

                    bx, by = get_position(nx, ny)

                    factor = 1 - (distance + 1) / config["blind"]["light_power"]

                    color = darken_color(config["colors"]["light"], factor) # On assombrit la couleur de la lumière en fonction de la distance

                    self.canvas.create_rectangle(
                        bx,
                        by,
                        bx + 20 - 1,
                        by + 20 - 1,
                        fill=color,
                        outline=color,
                    )

                    light.append((nx, ny, distance + 1))

    def clear_light(self):
        """Efface la lumière autour du joueur."""
        directions = [
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1),
        ]

        light = [(self.x, self.y, 0)]
        visited = {(self.x, self.y)}

        while light:
            x, y, distance = light.pop(0)

            if distance >= config["blind"]["light_power"]:
                continue

            for dx, dy in directions:
                nx = x + dx
                ny = y + dy

                if (
                    0 <= nx < len(self.maze[0])
                    and 0 <= ny < len(self.maze)
                    and self.maze[ny][nx] == 0
                    and (nx, ny) not in visited
                ):
                    visited.add((nx, ny))

                    bx, by = get_position(nx, ny)

                    self.canvas.create_rectangle(
                        bx,
                        by,
                        bx + 20 - 1,
                        by + 20 - 1,
                        fill=config["colors"]["darkness"],
                        outline=config["colors"]["darkness"],
                    )

                    light.append((nx, ny, distance + 1))

    def can_move(self, direction: Direction):
        """Vérifie si le joueur peut se déplacer dans la direction souhaitée."""
        height = len(self.maze)
        width = len(self.maze[0])

        if direction == Direction.UP:
            return self.y - 1 >= 0 and self.maze[self.y - 1][self.x] == 0

        if direction == Direction.DOWN:
            return self.y + 1 < height and self.maze[self.y + 1][self.x] == 0

        if direction == Direction.LEFT:
            return self.x - 1 >= 0 and self.maze[self.y][self.x - 1] == 0

        if direction == Direction.RIGHT:
            return self.x + 1 < width and self.maze[self.y][self.x + 1] == 0

        return False

        if direction == Direction.UP:
            return self.y - 1 >= 0 and self.maze[self.y - 1][self.x] == 0

        if direction == Direction.DOWN:
            return (
                self.y + 1 < config["window"]["height"]
                and self.maze[self.y + 1][self.x] == 0
            )

        if direction == Direction.LEFT:
            return self.x - 1 >= 0 and self.maze[self.y][self.x - 1] == 0

        if direction == Direction.RIGHT:
            return (
                self.x + 1 < (config["window"]["width"] - 15)
                and self.maze[self.y][self.x + 1] == 0
            )

        return False

    def move(self, direction: Direction):
        """Déplace le joueur dans la direction souhaitée si possible."""
        if direction == Direction.UP and self.can_move(direction):
            if config["blind"]["enabled"]:
                self.clear_light()
            self.clear()
            self.y -= 1
            self.draw()
            self.direction = direction
            self.moves += 1

        elif direction == Direction.DOWN and self.can_move(direction):
            if config["blind"]["enabled"]:
                self.clear_light()
            self.clear()
            self.y += 1
            self.draw()
            self.direction = direction
            self.moves += 1

        elif direction == Direction.LEFT and self.can_move(direction):
            if config["blind"]["enabled"]:
                self.clear_light()
            self.clear()
            self.x -= 1
            self.draw()
            self.direction = direction
            self.moves += 1

        elif direction == Direction.RIGHT and self.can_move(direction):
            if config["blind"]["enabled"]:
                self.clear_light()
            self.clear()
            self.x += 1
            self.draw()
            self.direction = direction
            self.moves += 1

        # Vérifie si le joueur a atteint la sortie du labyrinthe
        if self.x == len(self.maze[0]) - 2 and self.y == len(self.maze) - 1: 
            self.win()
