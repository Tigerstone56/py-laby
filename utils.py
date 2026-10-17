import json  # Import de la librairie json
import os  # Import de la librairie os
import subprocess  # Import de la librairie subprocess

# Ces deux dernières librairies sont nécessaires pour faire fonctionner les redémarrages du labyrinthe


def import_config():
    """Ouvre notre fichier de config, et en renvoie son contenu."""
    with open("config.json", "r") as file:
        config = json.load(file)
    return config


config = import_config()


def get_position(x, y):
    """Renvoie la position en pixels d'une case du labyrinthe."""
    return (10 + x * 20, 10 + y * 20)


def darken_color(color, factor):
    """Assombrit une couleur donnée par un facteur."""
    color = color.lstrip("#")

    r, g, b = int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16)
    r, g, b = int(r * factor), int(g * factor), int(b * factor)

    return f"#{r:02x}{g:02x}{b:02x}"


def clear_console():
    """Clear la console."""
    subprocess.run("cls" if os.name == "nt" else "clear", shell=True, check=False)
