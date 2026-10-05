import sys
import argparse
import random
from pathlib import Path
from datetime import date


HIGH_SCORE_FILE = Path("highscore.txt")


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Play a customizable hangman game."
    )

    parser.add_argument(
        "word_list",
        type=Path,
        help="text file containing one word per line",
    )

    parser.add_argument(
        "--penalties",
        type=int,
        default=12,
        help="maximum number of penalties (default: 12)",
    )

    parser.add_argument(
        "--length",
        type=int,
        help="required length of the secret word",
    )

    parser.add_argument(
        "--theme",
        default="general",
        help="theme displayed when the game starts",
    )

    arguments = parser.parse_args()

    # Vérification du nombre maximum de pénalités
    if arguments.penalties < 1:
        parser.error("--penalties must be at least 1")

    # Vérification de la longueur demandée
    if arguments.length is not None and arguments.length < 1:
        parser.error("--length must be at least 1")

    # Vérification du thème
    if not arguments.theme.strip():
        parser.error("--theme cannot be empty")

    return arguments


def choose_word(arguments):
    """
    Lit le fichier de mots et sélectionne un mot valide au hasard.
    """

    # Vérifier que le chemin existe
    if not arguments.word_list.exists():
        raise SystemExit("Error: file not found")

    # Vérifier qu'il s'agit bien d'un fichier
    if not arguments.word_list.is_file():
        raise SystemExit("Error: the word list is not a file")

    try:
        content = arguments.word_list.read_text(
            encoding="utf-8"
        )

    except PermissionError:
        raise SystemExit(
            "Error: permission denied when reading the word list"
        )

    except UnicodeDecodeError:
        raise SystemExit(
            "Error: the word list is not valid UTF-8"
        )

    except OSError as error:
        raise SystemExit(
            f"Error: cannot read file: {error}"
        )

    words = []

    for line in content.splitlines():

        word = line.strip().upper()

        # Ignorer les lignes vides
        if not word:
            continue

        # Autoriser uniquement A-Z
        if not word.isascii() or not word.isalpha():
            continue

        words.append(word)

    # Filtrer par longueur si --length est utilisé
    if arguments.length is not None:
        words = [
            word
            for word in words
            if len(word) == arguments.length
        ]

    if not words:
        raise SystemExit(
            "Error: no suitable word was found in the word list."
        )

    return random.choice(words)


def display_word():
    return " ".join(
        letter if letter in found_letters else "_"
        for letter in word
    )


def display_penalties():
    if penalties == 1:
        print(f"/ {penalties} penalty")
    else:
        print(f"/ {penalties} penalties")

    print(display_word())


def get_high_score():
    """
    Lit highscore.txt et retourne le meilleur score.
    """

    if not HIGH_SCORE_FILE.exists():
        return None, None

    if not HIGH_SCORE_FILE.is_file():
        return None, None

    try:
        lines = HIGH_SCORE_FILE.read_text(
            encoding="utf-8"
        ).splitlines()

    except (OSError, UnicodeDecodeError):
        # Si le fichier est corrompu ou illisible,
        # on ignore simplement le high score.
        return None, None

    best_attempts = None
    best_date = None

    for line in lines:

        parts = line.split(";")

        # Une ligne valide doit être :
        # nombre;date
        if len(parts) != 2:
            continue

        try:
            attempts = int(parts[0])
        except ValueError:
            continue

        # Un score négatif est impossible
        if attempts < 1:
            continue

        record_date = parts[1].strip()

        # Vérifier que la date possède le bon format
        try:
            date.fromisoformat(record_date)
        except ValueError:
            continue

        if best_attempts is None or attempts < best_attempts:
            best_attempts = attempts
            best_date = record_date

    return best_attempts, best_date


def save_high_score(attempts):
    """
    Ajoute un nouveau score dans highscore.txt.
    """

    # Protection supplémentaire
    if attempts < 1:
        return

    today = date.today().isoformat()

    try:
        with HIGH_SCORE_FILE.open(
            "a",
            encoding="utf-8"
        ) as file:
            file.write(f"{attempts};{today}\n")

    except PermissionError:
        print(
            "Warning: permission denied. "
            "High score could not be saved."
        )

    except OSError as error:
        print(
            f"Warning: unable to save high score: {error}"
        )


def check_high_score(attempts):
    """
    Compare le score actuel au meilleur score enregistré.
    """

    best_attempts, best_date = get_high_score()

    if best_attempts is None or attempts < best_attempts:

        save_high_score(attempts)

        print(
            f"Best ever! You guessed '{word}' "
            f"in {attempts} attempts."
        )

    else:

        print(
            f"You guessed '{word}' in {attempts} attempts, "
            f"but the record from {best_date} is "
            f"{best_attempts} attempts."
        )


# --------------------------------------------------
# PROGRAMME PRINCIPAL
# --------------------------------------------------

# Vérification supplémentaire des arguments
if len(sys.argv) < 2:
    print("Error: missing argument")
    sys.exit(1)


try:
    arguments = parse_arguments()

except KeyboardInterrupt:
    print("\nGame interrupted.")
    sys.exit(1)


MAX_PENALTIES = arguments.penalties

word = choose_word(arguments)

found_letters = set()
penalties = 0
attempts = 0


print(f"Theme: {arguments.theme}")
print(display_word())
print(f"/ {penalties} penalty")


while penalties < MAX_PENALTIES:

    # ----------------------------------------------
    # Lecture de l'entrée utilisateur
    # ----------------------------------------------

    try:
        guess = input("$> ").strip().upper()

    except KeyboardInterrupt:
        print("\nGame interrupted.")
        break

    except EOFError:
        print("\nInput closed. Game interrupted.")
        break

    # ----------------------------------------------
    # Vérification d'une entrée vide
    # ----------------------------------------------

    if not guess:
        print("Please enter a letter or a word.")
        continue

    # ----------------------------------------------
    # Une tentative est comptée
    # ----------------------------------------------

    attempts += 1

    # ----------------------------------------------
    # Le joueur propose une lettre
    # ----------------------------------------------

    if len(guess) == 1:

        # Uniquement A-Z
        if not guess.isascii() or not guess.isalpha():
            print(
                "Invalid character. "
                "Please enter a letter from A to Z."
            )
            continue

        if guess in word:

            if guess in found_letters:
                print(f"'{guess}' has already been found")

            else:
                found_letters.add(guess)
                print(f"Found one '{guess}'")

        else:
            penalties += 1
            print(f"No '{guess}' found")

    # ----------------------------------------------
    # Le joueur propose un mot complet
    # ----------------------------------------------

    elif len(guess) > 1:

        # Chiffres uniquement
        if guess.isdigit():
            print(
                "Numbers don't work. "
                "Please enter a letter or a word."
            )
            continue

        # Caractères non alphabétiques
        if not guess.isascii() or not guess.isalpha():
            print(
                "Special characters don't work. "
                "Please enter letters only."
            )
            continue

        # Le joueur a trouvé le mot
        if guess == word:

            print(
                f"{guess}: correct guess - "
                f"{penalties} penalties"
            )

            check_high_score(attempts)
            break

        # Mauvais mot
        penalties = min(
            penalties + 5,
            MAX_PENALTIES
        )

        print(f"{guess}: incorrect guess")

    # ----------------------------------------------
    # Affichage après chaque tentative valide
    # ----------------------------------------------

    display_penalties()

    # ----------------------------------------------
    # Vérifier si toutes les lettres ont été trouvées
    # ----------------------------------------------

    if all(
        letter in found_letters
        for letter in word
    ):

        print(
            f"{word}: correct guess - "
            f"{penalties} penalties"
        )

        check_high_score(attempts)
        break

else:

    print("You lose!")
    print(f"The word was: {word}")
    print(f"Attempts: {attempts}")