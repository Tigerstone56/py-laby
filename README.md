# Labyrinthe - Mini-projet n°1 - NSI

Un simple jeu de labyrinthe développé en ***Python*** avec **Tkinter** dans le cadre d'un mini-projet en **spécialité NSI**.

## ✨ Fonctionnalités

* Génération procédurale de labyrinthes **aléatoires** et **résolvables**
* Contrôle des déplacements au **clavier**
* Mode **obscur** avec une **lampe personnalisable**
* Plusieurs **bots** simples
* Affichage des **FPS**
* **Configuration** centralisée

## ⚙️ Configuration

> La configuration se trouve dans le fichier `config.json`.

## 🎮 Contrôles

| Touche    | Direction |
|-----------|-----------|
| `↑` / `Z` | Haut      |
| `↓` / `S` | Bas       |
| `←` / `Q` | Gauche    |
| `→` / `D` | Droite    |

## 🤖 Bots

### `bot_left`

Le bot longe les murs de gauche jusqu'à trouver la sortie du labyrinthe. Il suit le pattern `LEFT, UP, RIGHT, DOWN`.

### `bot_right`

Le bot longe les murs de droite jusqu'à trouver la sortie du labyrinthe. Il suit le pattern `RIGHT, UP, LEFT, DOWN`.

### `bot_random`

Le bot choisit aléatoirement parmi les directions accessibles, tout en évitant autant que possible de faire immédiatement demi-tour.

## 📁 Structure

```text
laby/
│
├── main.py          # Lancement du jeu et boucle du jeu
├── maze.py          # Génération du labyrinthe
├── player.py        # Gestion du joueur et des déplacements
├── bot.py           # Gestion des bots basée sur player.py
├── config.json      # Configuration du jeu
├── utils.py         # Fonctions utiles pour plusieurs fichiers
│
└── README.md
```

## 🛠️ Installation

### Prérequis

* Python 3
* Tkinter

## 📦 Lancement

À la racine du projet :

```bash
python main.py
```

## ✏️ Contributions

Si ça vous intérresse ou ça vous amuse, n'hésitez pas à *fork* le repos et proposer une *pull request* pour ajouter vos nouvelles fonctionnalités. Attention toutefois à respecter la consigne initiale : un labyrinthe en Python avec Tkinter.

## 👨‍💻 Auteurs

**[Toraishi](https://github.com/Tigerstone56), [lirÿsm](https://github.com/lirysm), Tahitiboss1 & roubain**