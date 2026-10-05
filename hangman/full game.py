import pygame
import random
from pathlib import Path

# -----------------------------
# INITIALISATION
# -----------------------------

pygame.init()
WORD_LIST_FILE = Path("my_wordlist.txt")

# -----------------------------
# LIRE LE FICHIER ET CHOISIR UN MOT
# -----------------------------

def choose_word():

    words = []

    with WORD_LIST_FILE.open("r", encoding="utf-8") as file:

        for line in file:

            word = line.strip().upper()

            if word.isalpha():

                words.append(word)

    if not words:
        raise ValueError("La liste de mots est vide.")

    return random.choice(words)

# -----------------------------
# POLICE
# -----------------------------

font = pygame.font.Font(None, 32)
big_font = pygame.font.Font(None, 64)

# -----------------------------
# FENÊTRE
# -----------------------------

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman")

# -----------------------------
# HORLOGE
# -----------------------------

clock = pygame.time.Clock()

used_letters = []
secret_word = choose_word()
wrong_guesses = 0

KEY_WIDTH = 40
KEY_HEIGHT = 40
KEY_SPACING = 5

# -----------------------------
# DÉCOR
# -----------------------------

def draw_background():

    # Ciel
    screen.fill((135, 206, 235))

    # Sol
    pygame.draw.rect(
        screen,
        (90, 180, 80),
        (0, 500, WIDTH, 100)
    )

# -----------------------------
# POTENCE
# -----------------------------

def draw_gallows():

    wood_color = (120, 70, 30)

    # Poteau vertical
    pygame.draw.line(
        screen,
        wood_color,
        (600, 500),
        (600, 100),
        15
    )

    # Barre horizontale
    pygame.draw.line(
        screen,
        wood_color,
        (600, 100),
        (750, 100),
        15
    )

    # Barre diagonale
    pygame.draw.line(
        screen,
        wood_color,
        (600, 160),
        (660, 100),
        10
    )

    # Corde
    pygame.draw.line(
        screen,
        (230, 220, 180),
        (700, 100),
        (700, 150),
        5
    )

# -----------------------------
# PERSONNAGE
# -----------------------------

def draw_character():

    skin_color = (255, 220, 180)
    clothes_color = (50, 50, 50)

    # Tête
    if wrong_guesses >= 1:    
        pygame.draw.circle(
        screen,
        skin_color,
        (700, 180),
        30
    )

    # Corps
    if wrong_guesses >= 2:
        pygame.draw.line(
            screen,
            clothes_color,
            (700, 210),
            (700, 300),
            8
    )

    # Bras gauche
    if wrong_guesses >= 3:
        pygame.draw.line(
            screen,
            clothes_color,
            (700, 230),
            (660, 270),
            8
        )

    # Bras droit
    if wrong_guesses >= 4:
        pygame.draw.line(
        screen,
        clothes_color,
        (700, 230),
        (740, 270),
        8
    )

    # Jambe gauche
    if wrong_guesses >= 5:
        pygame.draw.line(
        screen,
        clothes_color,
        (700, 300),
        (670, 350),
        8
    )

    # Jambe droite
    if wrong_guesses >= 6:
        pygame.draw.line(
            screen,
        clothes_color,
        (700, 300),
        (730, 350),
        8
    )

# -----------------------------
# CLAVIER
# -----------------------------

def draw_keyboard():

    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    x = 30
    y = 30

    for i, letter in enumerate(letters):
        rect = pygame.Rect(x, y, KEY_WIDTH, KEY_HEIGHT)

        # Couleur de la touche
        if letter in used_letters:
            button_color = (150, 150, 150)
        else:
            button_color = (220 ,220 ,220)

        # Dessiner le bouton
        pygame.draw.rect(screen, button_color, rect)

        # Dessiner le contour
        pygame.draw.rect(screen, (0, 0, 0), rect, 2)

        # Dessiner la lettre
        text = font.render(letter, True, (0, 0, 0))

        text_rect = text.get_rect(center=rect.center)

        screen.blit(text, text_rect)

        x += KEY_WIDTH + KEY_SPACING

        if (i+1)%7 == 0:
            x = 30
            y += KEY_HEIGHT + KEY_SPACING
        
# -----------------------------
# AFFICHAGE DU MOT SECRET
# -----------------------------

def draw_word():

    display_word = ""

    for letter in secret_word:

        if letter in used_letters:
            display_word+= letter + " "
        else:
            display_word += "_ "

    text = font.render(display_word, True, (0, 0, 0))

    screen.blit(text, (300, 300))

# -----------------------------
# CLICS SUR LE CLAVIER
# -----------------------------

def check_game_status():

    if wrong_guesses >= 6:
        return "lose"

    for letter in secret_word:

        if letter not in used_letters:
            return "playing"

    return "win"

# -----------------------------
# AFFICHAGE FIN DE PARTIE
# -----------------------------

def draw_game_status(game_status):

    if game_status == "win":

        text = big_font.render("VICTOIRE !", True, (0, 120, 0))

        text_rect = text.get_rect(center=(400, 380))
        screen.blit(text, text_rect)

    elif game_status == "lose":

        text = big_font.render("DEFAITE !", True, (180, 0, 0))

        text_rect = text.get_rect(center=(400, 380))
        screen.blit(text, text_rect)

        word_text = font.render("Le mot etait : " + secret_word, True, (0, 0, 0))

        word_rect = word_text.get_rect(center=(400, 440))      
        screen.blit(word_text, word_rect)
# -----------------------------
# BOUTON REJOUER
# -----------------------------

def draw_restart_button():

    button_rect = pygame.Rect(300, 500, 200, 50)

    pygame.draw.rect(screen, (220, 220, 220), button_rect)

    pygame.draw.rect(screen, (0, 0, 0), button_rect, 2)

    text = font.render("Rejouer", True, (0, 0, 0))

    text_rect = text.get_rect(center=button_rect.center)

    screen.blit(text, text_rect)

# -----------------------------
# CLICS SUR REJOUER
# -----------------------------

def check_restart_click(position):
    button_rect = pygame.Rect(300, 500, 200, 50)

    if button_rect.collidepoint(position):

        restart_game()

# -----------------------------
# REINITIALISER LA PARTIE
# -----------------------------

def restart_game():

    global used_letters
    global wrong_guesses
    global game_status
    global secret_word

    used_letters = []
    wrong_guesses = 0
    game_status = "playing"
    secret_word = choose_word()

# -----------------------------
# CLICS SUR LE CLAVIER
# -----------------------------

def check_keyboard_click(position):

    global wrong_guesses

    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    x = 30
    y = 30

    for i, letter in enumerate(letters):

        rect = pygame.Rect(x, y, KEY_WIDTH, KEY_HEIGHT)

        if rect.collidepoint(position):
            if letter not in used_letters:
                used_letters.append(letter)
                if letter in secret_word:
                    print("Bonne lettre :", letter)
                else:
                    wrong_guesses += 1
                    print("Mauvaise lettre :", letter)
                    print("Erreurs :", wrong_guesses)

        x += KEY_WIDTH + KEY_SPACING

        if (i + 1) % 7 == 0:

            x = 30
            y += KEY_HEIGHT + KEY_SPACING

# -----------------------------
# BOUCLE DU JEU
# -----------------------------

game_status = "playing"

running = True

while running:

    # Récupérer les événements
    for event in pygame.event.get():

        # Si on clique sur la croix
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            if game_status == "playing":
                check_keyboard_click(event.pos)
            else:
                check_restart_click(event.pos)

    # Afficher le résultat du jeu
    game_status = check_game_status()

    # Dessiner le décor
    draw_background()

    # Dessiner la potence
    draw_gallows()

    # Dessiner le personnage
    draw_character()

    # Dessiner le clavier
    draw_keyboard()

    # Dessiner le mot secret
    draw_word()

    # Dessiner le statut du jeu
    draw_game_status(game_status)

    if game_status != "playing":
        draw_restart_button()

    # Afficher l'écran
    pygame.display.flip()

    # 60 images par seconde
    clock.tick(60)


# -----------------------------
# FERMETURE
# -----------------------------

pygame.quit()