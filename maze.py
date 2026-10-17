from random import shuffle


def generate_maze(width, height):
    """Génère un labyrinthe aléatoire sous la forme d'une matrice."""
    maze = [[1 for x in range(width)] for y in range(height)] # Création d'une matrice remplie de 1 (murs)

    def carve(x, y):
        """Fonction récursive pour creuser le labyrinthe."""
        stack = [(x, y)] # On crée une pile pour stocker les positions à explorer
        maze[y][x] = 0 # On transforme la case de départ en 0 (chemin)

        while stack: # Tant que la pile n'est pas vide, on continue à explorer
            x, y = stack[-1] # On récupère la dernière position de la pile

            directions = [(2, 0), (-2, 0), (0, 2), (0, -2)] # On définit les directions possibles pour creuser le labyrinthe
            shuffle(directions) # On mélange les directions pour rendre le labyrinthe aléatoire

            for dx, dy in directions: # On essaye chaque direction
                nx, ny = x + dx, y + dy # On calcule les nouvelles coordonnées

                if 0 < nx < width - 1 and 0 < ny < height - 1 and maze[ny][nx] == 1: # Si la nouvelle position est dans les limites du labyrinthe et que c'est un mur
                    maze[y + dy // 2][x + dx // 2] = 0 # On transforme la case entre les deux en 0 (chemin)
                    maze[ny][nx] = 0 # On transforme la nouvelle case en 0 (chemin)
                    stack.append((nx, ny)) # On ajoute la nouvelle position à la pile pour continuer à explorer
                    break
            else:
                stack.pop() # Sinon on retire la position de la pile pour revenir en arrière

    carve(1, 1) # On commence à creuser le labyrinthe à partir de la position (1, 1)
    maze[0][1], maze[height - 1][width - 2] = 0, 0 # On crée une entrée et une sortie pour le labyrinthe

    return maze
