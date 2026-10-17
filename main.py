import json  # Import de la librairie json, permettant de lire et modifier les fichiers du même langage
import time  # Import de la librairie time, permettant la création de notre chronomètre en jeu
from tkinter import *  # Import de tkinter, pour créer notre interface graphique
from tkinter import messagebox  # Import de messagebox depuis tkinter

import player  # Import de player.py, et de ses classes
from bot import Bot  # Import de la classe Bot depuis bot.py
from maze import generate_maze  # Import de la fonction generate_maze() depuis maze.py
from player import (
    Direction,
    Player,
)  # Import des classes Direction et Player depuis player.py
from utils import (
    clear_console,
    import_config,
)  # Import des fonctions clear_console() et import_config() depuis utils.py

config = import_config()  # Initiation de la configuration du labyrinthe

last_time = time.perf_counter()  # Iinitation de
start_time = time.perf_counter()  # deux compteurs
fps_counter = 0
fps_timer = 0
current_fps = 0
bot_timer = 0
screen_width = 0
screen_height = 0


def get_largest_odd(value):
    """Renvoie le plus grand nombre impair inférieur ou égal à value."""
    value = int(value)
    return value if value % 2 == 1 else value - 1


def get_screen_limits(width, height):
    """Calcule les dimensions maximales impaires en cases."""
    max_width = get_largest_odd((width - 20) // 20)
    max_height = get_largest_odd((height - 20) // 20)

    return max_width, max_height


def draw_maze(canvas, maze):
    """Affichage du labyrinthe dans le canvas."""
    for y, ligne in enumerate(
        maze
    ):  # Pour chaque ligne du labyrinthe, on récupère l'index y et la ligne
        for x, tile in enumerate(
            ligne
        ):  # Pour chaque colonne du labyrinthe, on récupère l'index x et la case
            x1 = 10 + x * 20
            y1 = 10 + y * 20
            x2 = x1 + 20
            y2 = y1 + 20

            if tile == 1:
                color = config["colors"]["wall"]
            else:
                color = config["colors"]["floor"]

            canvas.create_rectangle(
                x1, y1, x2, y2, fill=color, outline=color
            )  # On dessine la case dans le canvas avec la couleur correspondante


def win(root):
    """Fonction appelée lorsque le joueur atteint la sortie du labyrinthe."""
    now = time.perf_counter()
    elapsed = round(now - start_time, 2)
    
    # messagebox.showinfo(
    #     "Victoire !", f"Tu as triomphé du labyrinthe en {elapsed} secondes !"
    # )

    with open("config.json", "r", encoding="utf-8") as file:
        config = json.load(file)
    # On recharge la configuration du labyrinthe

    windowWin = Toplevel(root)
    windowWin.grab_set()
    windowWin.lift()
    windowWin.focus_force()
    windowWin.title("Victoire !")
    windowWin.geometry("380x450")
    windowWin.resizable(False, False)

    # On crée un nouveau menu pour la victoire

    Label(windowWin, text=f"Vous avez triomphé du Labyrinthe en {elapsed}s !", font=("Arial", 12, "bold")).pack(pady=10) # Message de victoire

    Button(
        windowWin,
        text="Réessayer le labyrinthe",
        font=("Arial", 8, "bold"),
        command=lambda: restart(root),
    ).pack(fill="x", padx=15, pady=5) # Bouton pour réessayer un labyrinthe

    Button(
        windowWin,
        text="Modifier les paramètres du Labyrinthe",
        font=("Arial", 8, "bold"),
        command=lambda: changeSettings(root, config)
    ).pack(fill="x", padx=15, pady=5) # Bouton pour modifier les paramètres du labyrinthe

    Button(
        windowWin,
        text="Quitter le jeu",
        font=("Arial", 8, "bold"),
        command=lambda: windowWin.quit(),
    ).pack(fill="x", padx=15, pady=5) # Bouton pour quitter le jeu

    # root.destroy()  # Détruit la fenêtre donc ferme le jeu

def intro():
    """Affiche l'introduction du jeu dans la console."""
    clear_console()

    # Purement esthétique,affiche en violet si le mode aveugle est activé
    if config["blind"]["enabled"]:
        logo_color = config["console"]["purple"]
    else:
        logo_color = config["console"]["yellow"]

    print(
        logo_color
        + r""" /$$                 /$$                           /$$             /$$     /$$                
| $$                | $$                          |__/            | $$    | $$                
| $$        /$$$$$$ | $$$$$$$  /$$   /$$  /$$$$$$  /$$ /$$$$$$$  /$$$$$$  | $$$$$$$   /$$$$$$ 
| $$       |____  $$| $$__  $$| $$  | $$ /$$__  $$| $$| $$__  $$|_  $$_/  | $$__  $$ /$$__  $$
| $$        /$$$$$$$| $$  \ $$| $$  | $$| $$  \__/| $$| $$  \ $$  | $$    | $$  \ $$| $$$$$$$$
| $$       /$$__  $$| $$  | $$| $$  | $$| $$      | $$| $$  | $$  | $$    | $$  | $$| $$_____/
| $$$$$$$$|  $$$$$$$| $$$$$$$/|  $$$$$$$| $$      | $$| $$  | $$  |  $$$$/| $$  | $$|  $$$$$$$
|________/ \_______/|_______/  \____  $$|__/      |__/|__/  |__/   \___/  |__/  |__/ \_______/
                               /$$  | $$                                                      
By Toraishi, Tahitiboss1,     |  $$$$$$/                                                       
lirÿsm & roubain.              \______/"""
        + config["console"]["reset"]
    )

    print(
        config["console"]["blue"]
        + "◈══════════════════════════════════════════════════════◈"
        + config["console"]["reset"]
    )
    print(
        config["console"]["blue"]
        + "|                                                      |"
        + config["console"]["reset"]
    )
    print(
        config["console"]["blue"]
        + "|"
        + config["console"]["reset"]
        + "      Bienvenue dans le labyrinthe, aventurier !      "
        + config["console"]["blue"]
        + "|"
        + config["console"]["reset"]
    )
    print(
        config["console"]["blue"]
        + "|"
        + config["console"]["gray"]
        + " Pour plus d'informations, rendez-vous dans README.md "
        + config["console"]["blue"]
        + "|"
        + config["console"]["reset"]
    )
    print(
        config["console"]["blue"]
        + "|                                                      |"
        + config["console"]["reset"]
    )
    print(
        config["console"]["blue"]
        + "◈══════════════════════════════════════════════════════◈"
        + config["console"]["reset"]
    )


def game_loop(root, bot, labelStats):
    """Boucle principale du jeu qui sert à compter le temps, les FPS et à faire bouger le bot s'il y en a un."""
    global last_time, fps_counter, fps_timer, current_fps, bot_timer, game_loop_id

    now = time.perf_counter()
    delta_time = now - last_time
    last_time = now
    elapsed = round(now - start_time, 2)

    # Si le joueur est un bot, on appellela logique de mouvement du bot toutes les x secondes, selon la configuration
    if config["player"]["type"] != "human":
        bot_timer += delta_time

        if bot_timer >= config["player"]["move_time"]:
            bot.bot_move()
            bot_timer = 0

    # On ajoute 1 au nombre de frames et on ajoute le temps écoulé depuis la dernière frame
    fps_counter += 1
    fps_timer += delta_time

    # Si une seconde s'est écoulée, on met à jour le compteur de FPS et le temps écoulé
    if fps_timer >= 1:
        current_fps = fps_counter
        fps_counter = 0
        fps_timer = 0

        labelStats.config(text=f"FPS : {current_fps}   |   Temps : {elapsed}s")

    # On rappelle la fonction game_loop() après un certain temps, selon la configuration
    game_loop_id = root.after(
        1000 // config["utils"]["fps"], game_loop, root, bot, labelStats
    )


def changeSettings(root, config):
    """Affiche la fenêtre qui permet de modifier les paramètres du jeu en modifiant directement le fichier config.json."""
    # Création de la fenêtre volante
    windowSettings = Toplevel(root)
    windowSettings.grab_set()
    windowSettings.lift()
    windowSettings.focus_force()
    windowSettings.title("Configurer votre Labyrinthe")
    windowSettings.geometry("380x700")
    windowSettings.resizable(False, False)

    max_width, max_height = get_screen_limits(
        screen_width, screen_height
    )  # Calcul de la taille maximale en fonction de la résolution de l'écran

    fields = {}  # Dictionnaire qui contiendra les champs de saisie pour chaque paramètre modifiable

    Label(
        windowSettings,
        text="Modifiez les paramètres du Labyrinthe :",
        font=("Arial", 10, "bold"),
    ).pack(pady=10)  # Affichage du titre

    frameSettings = Frame(windowSettings)
    frameSettings.pack(fill=BOTH, expand=True, padx=10, pady=5)

    def add_entry(parent, label, value):
        """Ajoute un champ de texte pour un paramètre modifiable."""
        frame = Frame(parent)
        frame.pack(fill="x", padx=5, pady=3)

        Label(frame, text=label, anchor="w").pack(side=LEFT)

        entry = Entry(frame, width=15)
        entry.insert(0, str(value))
        entry.pack(side=RIGHT)

        return entry

    def add_slider(parent, label, value, from_, to):
        """Ajoute un curseur pour un paramètre modifiable."""
        frame = Frame(parent)
        frame.pack(fill="x", padx=5, pady=3)

        Label(frame, text=label, anchor="w").pack(anchor="w")

        slider = Scale(
            frame,
            from_=from_,
            to=to,
            orient=HORIZONTAL,
            resolution=2,
            showvalue=True,
            length=300,
        )
        slider.set(value)
        slider.pack(fill="x")

        return slider

    # Taille du labyrinthe
    frameWindow = LabelFrame(frameSettings, text="Labyrinthe")
    frameWindow.pack(fill="x", pady=4)

    fields["window.width"] = add_slider(
        frameWindow,
        "Largeur de la fenêtre en cases (-14 pour la taille du labyrinthe)",
        config["window"]["width"],
        19,
        max_width,
    )
    fields["window.height"] = add_slider(
        frameWindow,
        "Hauteur de la fenêtre en cases (-14 pour la taille du labyrinthe)",
        config["window"]["height"],
        21,
        max_height,
    )

    # Couleurs
    frameColors = LabelFrame(frameSettings, text="Couleurs (hexadecimal)")
    frameColors.pack(fill="x", pady=4)

    color_names = {
        "player": "Joueur",
        "wall": "Murs",
        "floor": "Sol",
        "light": "Lumière",
        "darkness": "Obscurité",
    }

    for key, label in color_names.items():
        fields[f"colors.{key}"] = add_entry(frameColors, label, config["colors"][key])

    # Mode aveugle
    frameBlind = LabelFrame(frameSettings, text="Mode aveugle")
    frameBlind.pack(fill="x", pady=4)

    blindEnabled = BooleanVar(value=config["blind"]["enabled"])

    Checkbutton(
        frameBlind,
        text="Activer le mode aveugle",
        variable=blindEnabled,
    ).pack(anchor="w", padx=5, pady=3)

    fields["blind.light_power"] = add_entry(
        frameBlind,
        "Puissance de la lampe",
        config["blind"]["light_power"],
    )

    # Joueur
    framePlayer = LabelFrame(frameSettings, text="Joueur")
    framePlayer.pack(fill="x", pady=4)

    Label(framePlayer, text="Type de joueur").pack(anchor="w", padx=5, pady=3)

    playerType = StringVar(value=config["player"]["type"])

    OptionMenu(
        framePlayer,
        playerType,
        "human",
        "bot_left",
        "bot_right",
        "bot_random",
    ).pack(fill="x", padx=5, pady=3)

    fields["player.move_time"] = add_entry(
        framePlayer,
        "Temps de déplacement du bot",
        config["player"]["move_time"],
    )

    # Utilitaires
    frameUtils = LabelFrame(frameSettings, text="Utilitaires")
    frameUtils.pack(fill="x", pady=4)

    fields["utils.fps"] = add_entry(frameUtils, "FPS maximum", config["utils"]["fps"])

    def saveSettings():
        """Sauvegarde les paramètres modifiés dans le fichier config.json et redémarre le jeu."""
        try: # Permet d'essayer la sauvegarde et de gérer les potentielles erreurs
            updated = json.loads(json.dumps(config)) # Crée une copie de la configuration actuelle

            # On récupère les valeurs des champs de saisie et on les stocke dans la copie de la configuration
            updated["window"]["width"] = int(fields["window.width"].get())
            updated["window"]["height"] = int(fields["window.height"].get())

            # On stocke les dimensions dans des variables pour les vérifier plus facilement
            width = updated["window"]["width"]
            height = updated["window"]["height"]

            # On vérifie que la largeur et la hauteur sont impaires
            if width % 2 == 0 or height % 2 == 0:
                raise ValueError("La largeur et la hauteur doivent être impaires.")

            # On vérifie que la largeur et la hauteur sont dans les limites
            if not (19 <= width <= max_width and 21 <= height <= max_height):
                raise ValueError(
                    f"Taille invalide. Limites : "
                    f"19 à {max_width} en largeur et "
                    f"21 à {max_height} en hauteur."
                )

            # On vérifie que les couleurs sont valides en hexadécimal
            for key in color_names:
                color = fields[f"colors.{key}"].get().strip()

                if (
                    len(color)
                    != 7  # Longueur de 7 caractères, le # et les 6 caractères hexadécimaux
                    or not color.startswith("#")  # Commence par #
                    or any(
                        c not in "0123456789abcdefABCDEF" for c in color[1:]
                    )  # Les 6 caractères suivants sont des chiffres hexadécimaux
                ):
                    raise ValueError(f"Couleur invalide : {color}")

                updated["colors"][key] = color

            # On récupère les autres paramètres et on les stocke dans la copie de la configuration
            updated["blind"]["enabled"] = blindEnabled.get()
            updated["blind"]["light_power"] = int(fields["blind.light_power"].get())

            updated["player"]["type"] = playerType.get()
            updated["player"]["move_time"] = float(fields["player.move_time"].get())

            updated["utils"]["fps"] = int(fields["utils.fps"].get())

            # On vérifie que les valeurs numériques sont valides
            if (
                updated["blind"]["light_power"] < 1
                or updated["player"]["move_time"] <= 0
                or updated["utils"]["fps"] < 1
            ):
                raise ValueError("Une valeur numérique est invalide.")

            # On ouvre le fichier config.json et on met à jour les paramètres modifiés
            with open("config.json", "r", encoding="utf-8") as file:
                original = json.load(file)

            for section in ("window", "colors", "blind", "player", "utils"):
                original[section] = updated[section]

            # On sauvegarde les modifications dans le fichier config.json
            with open("config.json", "w", encoding="utf-8") as file:
                json.dump(original, file, indent=2, ensure_ascii=False)
                file.write("\n")

            messagebox.showinfo(
                "Configuration",
                "Paramètres enregistrés dans config.json.",
                parent=windowSettings,
            )
            windowSettings.destroy()

            restart(root)

        except (ValueError, TypeError, OSError) as error: # Si une erreur survient dans le bloc try, on affiche un message d'erreur
            messagebox.showerror(
                "Erreur",
                f"Impossible d'enregistrer les paramètres :\n{error}",
                parent=windowSettings,
            )

    Button(
        windowSettings,
        text="Enregistrer les paramètres (redémarre le jeu)",
        command=saveSettings,
    ).pack(fill="x", padx=15, pady=10) # Bouton pour sauvegarder les paramètres et redémarrer le jeu


def displayHelp(root):
    """Affiche la fenêtre d'aide"""
    # Création de la fenêtre volante
    windowHelp = Toplevel(root)
    windowHelp.title("Aide")
    windowHelp.geometry("300x640")

    # Affichage du titre
    Label(
        windowHelp,
        text="Bienvenue dans le labyrinthe, aventurier !",
        fg=config["colors"]["player"],
        font=("Arial", 10, "bold"),
    ).pack(pady=4)
    Label(windowHelp, text="Ton objectif sera de t'échapper du labyrinthe").pack(pady=4)

    frameDirections = LabelFrame(
        windowHelp, text="Directions", font=("Arial", 10, "bold")
    )
    frameDirections.pack(padx=10, pady=4)
    frameDirections.pack(side=TOP, fill="x")

    Label(frameDirections, text="Z/↑ : Aller en haut", anchor="w").pack(
        fill="x", padx=4, pady=2
    )
    Label(frameDirections, text="Q/← : Aller à gauche", anchor="w").pack(
        fill="x", padx=4, pady=2
    )
    Label(frameDirections, text="S/↓ : Aller en bas", anchor="w").pack(
        fill="x", padx=4, pady=2
    )
    Label(frameDirections, text="D/→ : Aller à droite", anchor="w").pack(
        fill="x", padx=4, pady=2
    )

    frameHelpConfig = LabelFrame(
        windowHelp, text="Configuration possible", font=("Arial", 10, "bold")
    )
    frameHelpConfig.pack(padx=10, pady=4)
    frameHelpConfig.pack(side=TOP, fill="x")

    frameLabyrinthe = LabelFrame(
        frameHelpConfig, text="Taille du labyrinthe", font=("Arial", 9, "bold")
    )
    frameLabyrinthe.pack(padx=10, pady=4)
    frameLabyrinthe.pack(side=TOP, fill="x")

    Label(frameLabyrinthe, text="Largeur", anchor="w").pack(fill="x", padx=4, pady=1)
    Label(frameLabyrinthe, text="Hauteur", anchor="w").pack(fill="x", padx=4, pady=1)

    frameColors = LabelFrame(
        frameHelpConfig, text="Couleurs modifiables", font=("Arial", 9, "bold")
    )
    frameColors.pack(padx=10, pady=4)
    frameColors.pack(side=TOP, fill="x")

    Label(frameColors, text="Joueur", anchor="w").pack(fill="x", padx=4, pady=1)
    Label(frameColors, text="Murs", anchor="w").pack(fill="x", padx=4, pady=1)
    Label(frameColors, text="Sol", anchor="w").pack(fill="x", padx=4, pady=1)
    Label(frameColors, text="Lumière", anchor="w").pack(fill="x", padx=4, pady=1)
    Label(frameColors, text="Obscurité", anchor="w").pack(fill="x", padx=4, pady=1)
    Label(frameColors, text="Menu", anchor="w").pack(fill="x", padx=4, pady=1)

    frameBlind = LabelFrame(
        frameHelpConfig, text="Mode aveugle", font=("Arial", 9, "bold")
    )
    frameBlind.pack(padx=10, pady=4)
    frameBlind.pack(side=TOP, fill="x")

    Label(frameBlind, text="Activé/Désactivé", anchor="w").pack(
        fill="x", padx=4, pady=1
    )
    Label(frameBlind, text="Puissance de la lampe torche", anchor="w").pack(
        fill="x", padx=4, pady=1
    )

    framePlayer = LabelFrame(
        frameHelpConfig, text="Type de joueur", font=("Arial", 9, "bold")
    )
    framePlayer.pack(padx=10, pady=4)
    framePlayer.pack(side=TOP, fill="x")

    Label(framePlayer, text="Humain / Robot", anchor="w").pack(fill="x", padx=4, pady=1)
    Label(framePlayer, text="Temps de déplacement (Robot)", anchor="w").pack(
        fill="x", padx=4, pady=1
    )

    Button(
        windowHelp,
        text="Quitter le menu d'aide",
        font=("Arial", 9, "bold"),
        command=lambda: windowHelp.destroy(),
    ).pack(fill="x", padx=15, pady=5)


def restart(root):
    global game_loop_id, start_time, config

    config = import_config()

    player.config = config

    start_time = time.perf_counter()

    if game_loop_id is not None:
        root.after_cancel(game_loop_id)

        game_loop_id = None

    root.destroy()
    init()


def init():
    global screen_width, screen_height

    intro()

    # Fenêtre et résolution de l'écran
    root = Tk()
    root.title("Labyrinthe")
    root.resizable(False, False)

    root.update_idletasks()

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    max_width, max_height = get_screen_limits(screen_width, screen_height)

    # Vérifier que la résolution permet la taille minimale
    if max_width < 19 or max_height < 21:
        messagebox.showerror(
            "Résolution insuffisante",
            "La résolution de l'écran est trop petite "
            "pour afficher correctement le jeu.",
            parent=root,
        )
        root.destroy()
        return

    # Corriger les dimensions chargées depuis la configuration
    config["window"]["width"] = min(
        get_largest_odd(config["window"]["width"]),
        max_width,
    )
    config["window"]["height"] = min(
        get_largest_odd(config["window"]["height"]),
        max_height,
    )

    # Génération du labyrinthe
    maze = generate_maze(
        config["window"]["width"] - 14,
        config["window"]["height"],
    )

    # Dimensions de la fenêtre
    window_width = config["window"]["width"] * 20 + 20
    window_height = config["window"]["height"] * 20 + 20

    if (
        config["window"]["width"] == max_width
        and config["window"]["height"] == max_height
    ):
        root.attributes("-fullscreen", True)
    else:
        root.geometry(f"{window_width}x{window_height}")

    # Canvas
    canvas_width = (config["window"]["width"] - 14) * 20 + 20 - 3
    canvas_height = config["window"]["height"] * 20 + 20 - 3

    bg_color = (
        config["colors"]["darkness"]
        if config["blind"]["enabled"]
        else config["colors"]["floor"]
    )

    canvas = Canvas(
        root,
        width=canvas_width,
        height=canvas_height,
        bg=bg_color,
    )

    canvas.pack(side=LEFT, fill=Y)

    # Menu

    frame_width = window_width - canvas_width
    frame_height = window_height

    frame = Frame(root, width=frame_width, height=frame_height)
    frame.pack(side=RIGHT, fill=BOTH, expand=True)
    frame.pack_propagate(False)

    # Menu - Header (Statistiques)

    frameHeader = LabelFrame(
        frame, width=frame_width, text="Statistiques", font=("Arial", 10, "bold")
    )
    frameHeader.pack(fill="x", padx=10, pady=10)

    labelStats = Label(frameHeader, text="Chargement...", anchor="w", justify=LEFT)
    labelStats.pack(fill="x", padx=5, pady=5)

    # Menu - Aide

    frameAide = LabelFrame(
        frame, width=frame_width, text="Aide", font=("Arial", 10, "bold")
    )
    frameAide.pack(fill="x", padx=10, pady=10)

    buttonAide = Button(
        frameAide, text="Afficher l'aide", command=lambda: displayHelp(root)
    )
    buttonAide.pack(fill="x", padx=15, pady=5)

    # Menu - Config (reset, settings, quitter)

    frameConfig = LabelFrame(
        frame, width=frame_width, text="Configuration", font=("Arial", 10, "bold")
    )
    frameConfig.pack(fill="x", padx=10, pady=10)

    buttonConfig1 = Button(
        frameConfig, text="Réinitialiser le pattern", command=lambda: restart(root)
    )
    buttonConfig1.pack(fill="x", padx=15, pady=5)

    buttonConfig2 = Button(
        frameConfig,
        text="Modifier les paramètres",
        command=lambda: changeSettings(root, config),
    )
    buttonConfig2.pack(fill="x", padx=15, pady=5)

    buttonConfig3 = Button(
        frameConfig, text="Quitter le Labyrinthe", command=lambda: root.quit()
    )
    buttonConfig3.pack(fill="x", padx=15, pady=5)

    # Menu - Credits

    frameCredits = LabelFrame(
        frame, width=frame_width, text="Crédits", font=("Arial", 10, "bold")
    )
    frameCredits.pack(fill="x", padx=10, pady=10)

    labelCredits1 = Label(
        frameCredits,
        text="Chef de Projet : roubain",
        anchor="w",
        font=("Arial", 8, "italic"),
    )
    labelCredits1.pack(fill="x")

    labelCredits2 = Label(
        frameCredits,
        text="Interface HM : lirÿsm",
        anchor="w",
        font=("Arial", 8, "italic"),
    )
    labelCredits2.pack(fill="x")

    labelCredits3 = Label(
        frameCredits, text="Mécaniques : Toraishi", anchor="w", font=("Arial", 8, "italic")
    )
    labelCredits3.pack(fill="x")

    labelCredits4 = Label(
        frameCredits,
        text="Règles du Jeu : Tahitiboss1",
        anchor="w",
        font=("Arial", 8, "italic"),
    )
    labelCredits4.pack(fill="x")

    if config["blind"]["enabled"] == False:
        draw_maze(canvas, maze)

    if config["player"]["type"] == "human":
        # Création du player
        player = Player(canvas, 1, 0, maze, lambda: win(root))
        player.draw()

        # Keybinds pour les flèches et ZQSD
        root.bind("<Up>", lambda event: player.move(Direction.UP))
        root.bind("<z>", lambda event: player.move(Direction.UP))
        root.bind("<Down>", lambda event: player.move(Direction.DOWN))
        root.bind("<s>", lambda event: player.move(Direction.DOWN))
        root.bind("<Left>", lambda event: player.move(Direction.LEFT))
        root.bind("<q>", lambda event: player.move(Direction.LEFT))
        root.bind("<Right>", lambda event: player.move(Direction.RIGHT))
        root.bind("<d>", lambda event: player.move(Direction.RIGHT))
    else:
        player = Bot(canvas, 1, 0, maze, lambda: win(root), config["player"]["type"])

    game_loop(root, player, labelStats)
    root.mainloop()


init()
